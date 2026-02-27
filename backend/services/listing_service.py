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
    soft_delete_listing,
    # listing_images table ops (now all inside listing_model.py)
    add_listing_image,
    get_images_for_listing,
    set_primary_image,
    delete_listing_image,
    # listing_sizes table ops (now all inside listing_model.py)
    upsert_listing_size,
    get_sizes_for_listing,
    delete_listing_size
)

from models.storefront_model import get_storefront_by_id


#___________________________________________________________________________________
# SHARED HELPERS
# Purpose:
# Shared permission checks + admin helpers used by listing, images, and sizes logic.
#___________________________________________________________________________________

def is_admin(current_user):
    """Returns True if the user has admin privileges."""
    return current_user.get("role") == "admin"


def _assert_can_manage_listing(current_user, listing):
    """
    Permission rule:
    Only the listing's storefront owner OR an admin can manage listing images.
    """
    storefront = get_storefront_by_id(listing["storefront_id"])
    if storefront is None:
        raise Exception("Storefront not found for this listing.")

    is_owner = storefront["owner_id"] == current_user["id"]
    if not is_owner and not is_admin(current_user):
        raise Exception("Unauthorized action.")


#__________________________________________________________________________________________
# LISTING MANAGEMENT SERVICES
# Purpose:
# System rules + validation logic for creating, reading, updating, and deleting listings.
#__________________________________________________________________________________________

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


#__________________________________________________________________________
# LISTING IMAGES SERVICES
# Purpose:
# This section enforces system rules for listing images before DB is updated.
#__________________________________________________________________________

def add_listing_image_service(current_user, listing_id, image_url, is_primary=False):
    """
    Adds an image to a listing.

    Enforces:
    - user logged in
    - listing exists
    - owner/admin permissions
    - image_url must be provided
    """
    if current_user is None:
        raise Exception("Unauthorized.")

    if image_url is None or str(image_url).strip() == "":
        raise Exception("image_url is required.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    _assert_can_manage_listing(current_user, listing)

    return add_listing_image(
        listing_id=listing_id,
        image_url=str(image_url).strip(),
        is_primary=bool(is_primary)
    )


def get_listing_images_service(listing_id):
    """
    Public read:
    Returns all images for a listing (primary first).
    """
    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")
    return get_images_for_listing(listing_id)


def set_primary_image_service(current_user, listing_id, image_id):
    """
    Sets the primary image for a listing.

    Enforces:
    - user logged in
    - listing exists
    - owner/admin permissions
    """
    if current_user is None:
        raise Exception("Unauthorized.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    _assert_can_manage_listing(current_user, listing)

    updated = set_primary_image(listing_id, image_id)
    if updated is None:
        raise Exception("Image not found for this listing.")

    return updated


def delete_listing_image_service(current_user, listing_id, image_id):
    """
    Deletes an image record.

    Enforces:
    - user logged in
    - listing exists
    - owner/admin permissions
    """
    if current_user is None:
        raise Exception("Unauthorized.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    _assert_can_manage_listing(current_user, listing)

    deleted = delete_listing_image(image_id)
    if not deleted:
        raise Exception("Image not found.")

    return {"deleted": True, "image_id": image_id}


#____________________________________________________________________________________________
# LISTING SIZE SERVICES
# Purpose:
# This section enforces system rules for size-based inventory before the database is updated.
#____________________________________________________________________________________________

def upsert_listing_size_service(current_user, listing_id, size, quantity):
    """
    Creates or updates a size inventory row.

    Enforces:
    - user logged in
    - listing exists
    - owner/admin permissions
    - size is required
    - quantity must be int >= 0
    """
    if current_user is None:
        raise Exception("Unauthorized.")

    if size is None or str(size).strip() == "":
        raise Exception("size is required.")

    try:
        quantity = int(quantity)
    except Exception:
        raise Exception("quantity must be an integer.")

    if quantity < 0:
        raise Exception("quantity cannot be negative.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    _assert_can_manage_listing(current_user, listing)

    return upsert_listing_size(
        listing_id=listing_id,
        size=str(size).strip(),
        quantity=quantity
    )


def get_listing_sizes_service(listing_id):
    """
    Public read:
    Returns all size inventory rows for a listing.
    """
    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")
    return get_sizes_for_listing(listing_id)


def delete_listing_size_service(current_user, listing_id, size):
    """
    Deletes a size inventory row for a listing.

    Enforces:
    - user logged in
    - listing exists
    - owner/admin permissions
    """
    if current_user is None:
        raise Exception("Unauthorized.")

    if size is None or str(size).strip() == "":
        raise Exception("size is required.")

    listing = get_listing_by_id(listing_id)
    if listing is None:
        raise Exception("Listing not found.")

    _assert_can_manage_listing(current_user, listing)

    deleted = delete_listing_size(listing_id, str(size).strip())
    if not deleted:
        raise Exception("Size row not found.")

    return {"deleted": True, "listing_id": listing_id, "size": str(size).strip()}
