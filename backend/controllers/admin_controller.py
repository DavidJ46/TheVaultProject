# controllers/admin_controller.py
# File created by David Jackson

"""
Admin Controller

The controller layer defines API endpoints used by the frontend.

Responsibilities:
• Receive HTTP requests
• Call service functions
• Return JSON responses

Example Request Flow:
Frontend → Controller → Service → Model → Database
"""

from flask import Blueprint, jsonify, request, session, abort
from flask import render_template  # Added by David Jackson 3/23/2026

# Import service functions
from services.admin_service import (
    fetch_users,
    remove_user,
    fetch_listings,
    remove_listing,
    fetch_storefronts
)

# Create Flask Blueprint for admin routes
# All routes will start with /admin
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def require_admin():
    """
    Authorization helper function.

    This function ensures that the current user
    is logged in and has administrator privileges.

    Behavior:
    • If the user is not logged in → return HTTP 401
    • If the user is logged in but NOT an admin → return HTTP 403

    This prevents normal users from accessing admin-only routes.
    """

    # Check if the user is logged in - updated by David Jackson 3/23/2026
    if "user" not in session:
        abort(401)  # Unauthorized (user not logged in)

    # Check if the user has the admin role
    if session.get("role") != "admin":
        abort(403)  # Forbidden (not an admin)


@admin_bp.route("/users", methods=["GET"])
def get_users():
    """
    GET /admin/users

    Retrieves all users from the system.

    Returns:
        JSON list of users
    """

    # Ensure only admins can access this endpoint
    require_admin()

    users = fetch_users()

    return jsonify(users)


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    """
    DELETE /admin/users/<user_id>

    Removes a specific user from the system.

    URL Parameter:
        user_id: ID of the user to delete
    """

    # Ensure only admins can perform user deletion
    require_admin()

    result = remove_user(user_id)

    return jsonify(result)


@admin_bp.route("/listings", methods=["GET"])
def get_listings():
    """
    GET /admin/listings

    Returns all listings currently in the marketplace.
    """

    # Ensure only admins can view marketplace listings through admin tools
    require_admin()

    listings = fetch_listings()

    return jsonify(listings)


@admin_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing_route(listing_id):
    """
    DELETE /admin/listings/<listing_id>

    Removes a listing from the marketplace.

    Used when:
    • Listings violate rules
    • Listings are fraudulent
    """

    # Ensure only admins can delete listings
    require_admin()

    result = remove_listing(listing_id)

    return jsonify(result)


@admin_bp.route("/storefronts", methods=["GET"])
def get_storefronts():
    """
    GET /admin/storefronts

    Retrieves all storefronts created by users.

    This helps admins monitor marketplace activity.
    """

    # Ensure only admins can access storefront monitoring tools
    require_admin()

    stores = fetch_storefronts()

    return jsonify(stores)
