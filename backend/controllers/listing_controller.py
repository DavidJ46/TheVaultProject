# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3 
# Dates: 2/25-2/26

"""
controllers/listing_controller.py

Purpose:
Defines HTTP API endpoints for listing actions.

This layer should stay thin:
- parse request input (JSON, params)
- get current_user (temporary headers until auth is wired)
- call service functions
- return JSON responses

All system rules + permission checks happen in services/listing_service.py.
"""

from flask import Blueprint, request, jsonify

from services.listing_service import (
    create_listing_service,
    get_listing_by_id_service,
    get_listings_for_storefront_service,
    update_listing_service,
    delete_listing_service,
    # listing images services (merged into listing_service.py)
    add_listing_image_service,
    get_listing_images_service,
    set_primary_image_service,
    delete_listing_image_service,
    # listing sizes services (merged into listing_service.py)
    upsert_listing_size_service,
    get_listing_sizes_service,
    delete_listing_size_service
)
from services.storefront_service import get_my_storefront_service

listing_bp = Blueprint("listing_bp", __name__, url_prefix="/api")


def get_current_user():
    """
    Temporary user identity method (until real auth is connected):
    Read user from headers.

    Required header for protected routes:
      X-User-Id: <int>

    """
    user_id = request.headers.get("X-User-Id")
    role = request.headers.get("X-User-Role", "user")

    if not user_id:
        return None

    try:
        return {"id": int(user_id), "role": role}
    except Exception:
        return None


# __________________________________________________________
# CREATE LISTING FROM FORM (with file upload)
# POST /api/listings/create
# Handles form submission from Create Listing page
# __________________________________________________________

@listing_bp.post("/listings/create")
def create_listing_from_form():
    """
    Creates a listing from form data including file upload.
    Expects multipart/form-data with the following fields:
    - storefront_name: name of the storefront (for reference)
    - title: listing title/name
    - quantity_on_hand: quantity available
    - price: listing price
    - fulfillment_type: IN_STOCK or PREORDER
    - status: ACTIVE or INACTIVE
    - sizes_available: JSON string array of sizes ["S", "M", "L"]
    - listing_image: image file upload
    """
    import json
    import os
    from werkzeug.utils import secure_filename
    
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    try:
        # Get user's storefront to validate ownership
        user_storefront = get_my_storefront_service(current_user)
        if user_storefront is None:
            return jsonify({"error": "You must create a storefront before creating listings."}), 400
        
        # Get form fields
        title = request.form.get("title", "").strip()
        storefront_id = user_storefront["id"]
        quantity_on_hand = request.form.get("quantity_on_hand", type=int)
        price = request.form.get("price", type=float)
        fulfillment_type = request.form.get("fulfillment_type", "IN_STOCK").strip()
        status = request.form.get("status", "ACTIVE").strip()
        sizes_json = request.form.get("sizes_available", "[]")

        # Validate required fields
        if not title:
            return jsonify({"error": "title is required."}), 400

        # Parse sizes
        try:
            sizes_available = json.loads(sizes_json)
            if not isinstance(sizes_available, list) or len(sizes_available) == 0:
                return jsonify({"error": "At least one size must be selected."}), 400
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid sizes_available format."}), 400

        # Handle file upload
        image_url = None
        if "listing_image" in request.files and request.files["listing_image"].filename:
            file = request.files["listing_image"]
            
            # Validate file
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                return jsonify({"error": "Image must be PNG, JPG, JPEG, GIF, or WebP."}), 400
            
            # Save file
            try:
                filename = secure_filename(f"listing_{storefront_id}_{os.urandom(8).hex()}_{file.filename}")
                images_dir = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..", "static", "images")
                )
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, filename)
                file.save(file_path)
                image_url = f"/static/images/{filename}"
            except Exception as e:
                return jsonify({"error": f"Error saving image: {str(e)}"}), 500
        else:
            return jsonify({"error": "listing_image is required."}), 400

        # Prepare data for service
        data = {
            "title": title,
            "quantity_on_hand": quantity_on_hand,
            "price": price,
            "fulfillment_type": fulfillment_type,
            "status": status,
            "description": ""  # Can be added later
        }

        # Create listing
        listing = create_listing_service(current_user, storefront_id, data)

        # Add image to listing
        if image_url:
            try:
                add_listing_image_service(current_user, listing["id"], image_url, is_primary=True)
            except Exception as e:
                # Log but don't fail - listing was created
                print(f"Warning: Failed to add image to listing: {str(e)}")

        # Add sizes to listing
        for size in sizes_available:
            try:
                # Split quantity equally among sizes, or use full quantity for each size
                size_quantity = quantity_on_hand  # Could be changed to split quantity
                upsert_listing_size_service(current_user, listing["id"], size, size_quantity)
            except Exception as e:
                print(f"Warning: Failed to add size {size} to listing: {str(e)}")

        return jsonify(listing), 201

    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        return jsonify({"error": str(e)}), 400


#_________________
# LISTING ROUTES
# Purpose:
# Core listing CRUD routes (create/read/update/delete).
#_________________

# __________________________________________________________
# CREATE LISTING (Owner/Admin)
# POST /api/storefronts/<storefront_id>/listings
#___________________________________________________________

@listing_bp.post("/storefronts/<int:storefront_id>/listings")
def create_listing_route(storefront_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    data = request.get_json(silent=True) or {}

    try:
        listing = create_listing_service(current_user, storefront_id, data)
        return jsonify(listing), 201
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# __________________________________________________________
# GET LISTINGS FOR STOREFRONT (Public)
# GET /api/storefronts/<storefront_id>/listings
# ___________________________________________________________

@listing_bp.get("/storefronts/<int:storefront_id>/listings")
def get_storefront_listings_route(storefront_id):
    try:
        listings = get_listings_for_storefront_service(storefront_id)
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# __________________________________________________________
# GET MY LISTINGS (Owner/Admin)
# GET /api/listings/my
# ___________________________________________________________

@listing_bp.get("/listings/my")
def get_my_listings_route():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    try:
        user_storefront = get_my_storefront_service(current_user)
        if user_storefront is None:
            return jsonify([]), 200

        listings = get_listings_for_storefront_service(user_storefront["id"])
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# _________________________________________________________
# GET SINGLE LISTING (Public)
# GET /api/listings/<listing_id>
# _________________________________________________________

@listing_bp.get("/listings/<int:listing_id>")
def get_listing_route(listing_id):
    try:
        listing = get_listing_by_id_service(listing_id)
        return jsonify(listing), 200
    except Exception as e:
        msg = str(e).lower()
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


#__________________________________________________________
# UPDATE LISTING (Owner/Admin)
# PUT /api/listings/<listing_id>
# _________________________________________________________

@listing_bp.put("/listings/<int:listing_id>")
def update_listing_route(listing_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    data = request.get_json(silent=True) or {}

    try:
        updated = update_listing_service(current_user, listing_id, data)
        return jsonify(updated), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# __________________________________________________________
# DELETE LISTING (Owner/Admin)
# DELETE /api/listings/<listing_id>
# ___________________________________________________________

@listing_bp.delete("/listings/<int:listing_id>")
def delete_listing_route(listing_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    try:
        deleted = delete_listing_service(current_user, listing_id)
        return jsonify(deleted), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


#_________________
# LISTING IMAGES ROUTES
# Purpose:
# Routes for adding/removing images and setting the primary image for a listing.
#_________________

# Add image
# POST /api/listings/<listing_id>/images
@listing_bp.post("/listings/<int:listing_id>/images")
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
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# Get images
# GET /api/listings/<listing_id>/images
@listing_bp.get("/listings/<int:listing_id>/images")
def get_images_route(listing_id):
    try:
        result = get_listing_images_service(listing_id)
        return jsonify(result), 200
    except Exception as e:
        msg = str(e).lower()
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# Set primary
# PATCH /api/listings/<listing_id>/images/<image_id>/primary
@listing_bp.patch("/listings/<int:listing_id>/images/<int:image_id>/primary")
def set_primary_route(listing_id, image_id):
    current_user = get_current_user()

    try:
        result = set_primary_image_service(current_user, listing_id, image_id)
        return jsonify(result), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# Delete image
# DELETE /api/listings/<listing_id>/images/<image_id>
@listing_bp.delete("/listings/<int:listing_id>/images/<int:image_id>")
def delete_image_route(listing_id, image_id):
    current_user = get_current_user()

    try:
        result = delete_listing_image_service(current_user, listing_id, image_id)
        return jsonify(result), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


#_________________
# LISTING SIZE ROUTES
# Purpose:
# Routes for managing size-based inventory for a listing.
#_________________

# Add / Update size
# POST /api/listings/<listing_id>/sizes
@listing_bp.post("/listings/<int:listing_id>/sizes")
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
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# Get sizes
# GET /api/listings/<listing_id>/sizes
@listing_bp.get("/listings/<int:listing_id>/sizes")
def get_sizes_route(listing_id):
    try:
        result = get_listing_sizes_service(listing_id)
        return jsonify(result), 200
    except Exception as e:
        msg = str(e).lower()
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# Delete size
# DELETE /api/listings/<listing_id>/sizes/<size>
@listing_bp.delete("/listings/<int:listing_id>/sizes/<string:size>")
def delete_size_route(listing_id, size):
    current_user = get_current_user()

    try:
        result = delete_listing_size_service(current_user, listing_id, size)
        return jsonify(result), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400
