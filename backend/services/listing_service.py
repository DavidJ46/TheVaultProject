# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
services/listing_service.py

Purpose:
This file contains the system rules + validation logic for listings.

Rules enforced:
- Only storefront owner (or admin) can create/update/delete listings
- IN_STOCK listings must have quantity_on_hand
- PREORDER listings ignore quantity_on_hand
- Auto mark SOLD_OUT when quantity hits 0

S3 Integration Notes:
- Image files are uploaded to AWS S3 separately.
- The listing system stores image URLs (S3 links) in the DB.
"""

import json

from models.listing_model import (
    create_listing,
    get_listing_by_id,
    get_listings_by_storefront_id,
    update_listing,
    soft_delete_listing
)

from models.storefront_model import get_storefront_by_id


def is_admin(current_user):
    """Returns True if the user has admin privileges."""
    return current_user.get("role") == "admin"


def create_listing_service(current_user, storefront_id, data):
    """
    Creates a new listing under a storefront.

    Enforces:
    - User must be logged in
    - User must own the storefront OR be admin
    - title, price, fulfillment_type are required
    - fulfillment rules enforced
    """

    # Step 1: User must be logged in
    if current_user is None:
        raise Exception("Error! Unauthorized User.")

    user_id = current_user["id"]

    # Step 2: Storefront must exist
    storefront = get_storefront_by_id(storefront_id)
    if storefront is None:
        raise Exception("Storefront not found.")

    # Step 3: Ownership or admin check
    if storefront["owner_id"] != user_id and not is_admin(current_user):
        raise Exception("Unauthorized action.")

    # Step 4: Validate required fields
    title = data.get("title")
    if title is None or title.strip() == "":
        raise Exception("title is required.")

    price = data.get("price")
    if price is None:
        raise Exception("price is required.")

    try:
        price = float(price)
    except Exception:
        raise Exception("price must be a number.")

    if price < 0:
        raise Exception("price cannot be negative.")

    fulfillment_type = data.get("fulfillment_type")
    if fulfillment_type not in ["IN_STOCK", "PREORDER"]:
        raise Exception("fulfillment_type must be IN_STOCK or PREORDER.")

    # Step 5: Fulfillment rules
    quantity_on_hand = data.get("quantity_on_hand")

    if fulfillment_type == "PREORDER":
        # Preorders do not track inventory
        quantity_on_hand = None
    else:
        # IN_STOCK requires quantity
        if quantity_on_hand is None:
            raise Exception("quantity_on_hand is required for IN_STOCK listings.")

        try:
            quantity_on_hand = int(quantity_on_hand)
        except Exception:
            raise Exception("quantity_on_hand must be an integer.")

        if quantity_on_hand < 0:
            raise Exception("quantity_on_hand cannot be negative.")

    # Step 6: Handling of different sizes
    sizes_available = data.get("sizes_available")

    if sizes_available is not None:
        if isinstance(sizes_available, list):
            sizes_available = json.dumps(sizes_available)
        elif not isinstance(sizes_available, str):
            raise Exception("sizes_available must be a list or string.")

    # Step 7:  status 
    status = (data.get("status") or "ACTIVE").strip()

    # Auto mark SOLD_OUT if inventory hits zero
    if fulfillment_type == "IN_STOCK" and quantity_on_hand == 0:
        status = "SOLD_OUT"

    # Step 8: Save to database
    return create_listing(
        storefront_id=storefront_id,
        title=title.strip(),
        description=data.get("description"),
        price=price,
        fulfillment_type=fulfillment_type,
        quantity_on_hand=quantity_on_hand,
        sizes_available=sizes_available,
        status=status
    )


def get_listing_by_id_service(listing_id):
    """
    Retrieves a listing by ID.
    """
    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")
    return listing


def get_listings_for_storefront_service(storefront_id):
    """
    Returns all listings for a given storefront.
    """
    return get_listings_by_storefront_id(storefront_id)


def update_listing_service(current_user, listing_id, data):
    """
    Updates an existing listing.

    Enforces:
    - Only owner/admin can update
    - Fulfillment rules are rechecked if modified
    """

    if current_user is None:
        raise Exception("Error! Unauthorized User.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    # Permission check
    storefront = get_storefront_by_id(listing["storefront_id"])
    if storefront is None:
        raise Exception("Storefront not found for this listing.")

    if storefront["owner_id"] != current_user["id"] and not is_admin(current_user):
        raise Exception("Unauthorized action.")

    # Determine final fulfillment_type 
    fulfillment_type = data.get("fulfillment_type", listing["fulfillment_type"])
    if fulfillment_type not in ["IN_STOCK", "PREORDER"]:
        raise Exception("fulfillment_type must be IN_STOCK or PREORDER.")

    # Determine final quantity
    quantity_on_hand = data.get("quantity_on_hand", listing["quantity_on_hand"])

    if fulfillment_type == "PREORDER":
        quantity_on_hand = None
    else:
        if quantity_on_hand is None:
            raise Exception("quantity_on_hand is required for IN_STOCK listings.")

        try:
            quantity_on_hand = int(quantity_on_hand)
        except Exception:
            raise Exception("quantity_on_hand must be an integer.")

        if quantity_on_hand < 0:
            raise Exception("quantity_on_hand cannot be negative.")

    # Handle sizes
    sizes_available = None
    if "sizes_available" in data:
        sizes_available = data.get("sizes_available")
        if isinstance(sizes_available, list):
            sizes_available = json.dumps(sizes_available)
        elif sizes_available is not None and not isinstance(sizes_available, str):
            raise Exception("sizes_available must be a list or string.")

    # Validate title
    title = data.get("title")
    if title is not None:
        title = title.strip()
        if title == "":
            raise Exception("title cannot be empty.")

    # Validate price if provided
    price = data.get("price")
    if price is not None:
        try:
            price = float(price)
        except Exception:
            raise Exception("price must be a number.")
        if price < 0:
            raise Exception("price cannot be negative.")

    # status
    status = data.get("status")
    if status is not None:
        status = status.strip()

    # Auto SOLD_OUT logic if they didn't explicitly set status
    if status is None and fulfillment_type == "IN_STOCK" and quantity_on_hand == 0:
        status = "SOLD_OUT"

    return update_listing(
        listing_id=listing_id,
        title=title if title is not None else None,
        description=data.get("description"),
        price=price,
        fulfillment_type=fulfillment_type,
        quantity_on_hand=quantity_on_hand,
        sizes_available=sizes_available,
        status=status
    )


def delete_listing_service(current_user, listing_id):
    """
    Soft deletes a listing (status = 'DELETED').

    Reason for soft-delete:
    - Preservation of data history 
    - Prevents breakage f FK relationships
    - Allows for admin access
    """

    if current_user is None:
        raise Exception(" Error! Unauthorized User.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    storefront = get_storefront_by_id(listing["storefront_id"])
    if storefront is None:
        raise Exception("Storefront not found for this listing.")

    if storefront["owner_id"] != current_user["id"] and not is_admin(current_user):
        raise Exception("Unauthorized action.")

    return soft_delete_listing(listing_id)
