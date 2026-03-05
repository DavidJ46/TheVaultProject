# services/admin_service.py
# File created by David Jackson

"""
Admin Service

The service layer contains business logic for admin operations.

Responsibilities:
• Validate input
• Enforce rules
• Call model functions
• Return results to controllers

Architecture Flow:
Controller → Service → Model → Database
"""

# Import model functions
from models.admin_model import (
    get_all_users,
    delete_user,
    get_all_listings,
    delete_listing,
    get_all_storefronts
)


def fetch_users():
    """
    Retrieves all users in the system.

    Returns:
        list: User records returned from the model layer.
    """

    return get_all_users()


def remove_user(user_id):
    """
    Deletes a user after validating the request.

    Parameters:
        user_id (int): ID of the user to delete

    Returns:
        dict: Confirmation message
    """

    # Basic validation to ensure a user ID is provided
    if not user_id:
        raise ValueError("User ID required")

    # Call the model to delete the user
    delete_user(user_id)

    return {"message": "User deleted successfully"}


def fetch_listings():
    """
    Retrieves all marketplace listings.

    Returns:
        list: Listings from the database.
    """

    return get_all_listings()


def remove_listing(listing_id):
    """
    Deletes a listing from the system.

    Parameters:
        listing_id (int): Listing identifier

    Returns:
        dict: Success message
    """

    if not listing_id:
        raise ValueError("Listing ID required")

    delete_listing(listing_id)

    return {"message": "Listing removed successfully"}


def fetch_storefronts():
    """
    Retrieves all storefronts created by users.

    Returns:
        list: Storefront data
    """

    return get_all_storefronts()
