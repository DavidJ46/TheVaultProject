# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
controllers/listing_image_controller.py

Purpose:
Defines API endpoints for managing listing images.
"""

from flask import Blueprint, request, jsonify
from services.listing_image_service import (
    add_listing_image_service,
    get_listing_images_service,
    set_primary_image_service,
    delete_listing_image_service
)

listing_image_bp = Blueprint(
    "listing_image_bp",
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


# Add image
@listing_image_bp.post("/<int:listing_id>/images")
def add_image_route(listing_id):
    current_user = get_current_user()
    data = request.get_json(silent=True) or {}

    try:
        result = add_listing_image_service(
            current_user,
            listing_id,
            data.get("image_url"),
            data.get("is_primary", False)
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Get images
@listing_image_bp.get("/<int:listing_id>/images")
def get_images_route(listing_id):
    try:
        result = get_listing_images_service(listing_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Set primary
@listing_image_bp.patch("/<int:listing_id>/images/<int:image_id>/primary")
def set_primary_route(listing_id, image_id):
    current_user = get_current_user()

    try:
        result = set_primary_image_service(current_user, listing_id, image_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Delete image
@listing_image_bp.delete("/<int:listing_id>/images/<int:image_id>")
def delete_image_route(listing_id, image_id):
    current_user = get_current_user()

    try:
        result = delete_listing_image_service(current_user, listing_id, image_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
