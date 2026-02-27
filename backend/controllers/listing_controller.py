# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

######### THIS CODE NEEDS TO BE UPDATED. MOST IS A PLACEHOLDER ##############
""" 
listing_controller.py

Purpose:
This file defines HTTP API endpoints for listing actions.

It will:
- parse rquest input 
- get current_user (temp headers until we build AUTH file)
- Call service functions
- return JSON responses 
"""

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
    delete_listing_service
)

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
