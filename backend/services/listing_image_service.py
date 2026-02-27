# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
services/listing_image_service.py

Purpose:
This file enforces system rules for listing imaged before DB is updated.

This file handles:
- Input vlidation
- Permission checks (only listing owner or admin can modify images)
- Multistep actions 
- Calls model functions to run SQL queries

Rules enforced:
- Only the storefront owner (or admin) can add/remove/set primary images for a listing.
- Images are stored as URLs (typically AWS S3 links) in the database.

"""

from models.listing_model import get_listing_by_id
from models.storefront_model import get_storefront_by_id
from models.listing_image_model import (
    add_listing_image,
    get_images_for_listing,
    set_primary_image,
    delete_listing_image
)


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
