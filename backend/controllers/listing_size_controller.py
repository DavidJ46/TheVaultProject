# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
controllers/listing_size_controller.py

Purpose:
Defines API endpoints for managing size-based inventory.
"""

from flask import Blueprint, request, jsonify
from services.listing_size_service import (
    upsert_listing_size_service,
    get_listing_sizes_service,
    delete_listing_size_service
)

listing_size_bp = Blueprint(
    "listing_size_bp",
    __name__,
    url_prefix="/api/listings"
)


def get_current_user():
    user_id = request.headers.get("X-User-Id")
    role = request.headers.get("X-User-Role", "user")

    if not user_id:
        return None

    try:
        return {"id": int(user_id), "role": role}
    except Exception:
        return None


# Add / Update size
@listing_size_bp.post("/<int:listing_id>/sizes")
def upsert_size_route(listing_id):
    current_user = get_current_user()
    data = request.get_json(silent=True) or {}

    try:
        result = upsert_listing_size_service(
            current_user,
            listing_id,
            data.get("size"),
            data.get("quantity")
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Get sizes
@listing_size_bp.get("/<int:listing_id>/sizes")
def get_sizes_route(listing_id):
    try:
        result = get_listing_sizes_service(listing_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Delete size
@listing_size_bp.delete("/<int:listing_id>/sizes/<string:size>")
def delete_size_route(listing_id, size):
    current_user = get_current_user()

    try:
        result = delete_listing_size_service(current_user, listing_id, size)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
