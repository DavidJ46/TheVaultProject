# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
services/listing_size_service.py

Purpose:
This file enforces system rules for size-based inventory before the database is updated.

What this file handles:
- Input validation (size required, quantity must be int >= 0)
- Permission checks (only listing owner or admin can change inventory)
- Inventory updates at the size level (S/M/L/XL/ONE_SIZE)
- Calls model functions to run the SQL queries
"""

from models.listing_model import get_listing_by_id
from models.storefront_model import get_storefront_by_id
from models.listing_size_model import (
    upsert_listing_size,
    get_sizes_for_listing,
    delete_listing_size
)


def is_admin(current_user):
    """Returns True if the user has admin privileges."""
    return current_user.get("role") == "admin"


def _assert_can_manage_listing(current_user, listing):
    """
    Permission rule:
    Only the listing's storefront owner OR an admin can manage listing size inventory.
    """
    storefront = get_storefront_by_id(listing["storefront_id"])
    if storefront is None:
        raise Exception("Storefront not found for this listing.")

    is_owner = storefront["owner_id"] == current_user["id"]
    if not is_owner and not is_admin(current_user):
        raise Exception("Unauthorized action.")


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
