# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
storefront_controller.py


Purpose: Defines HTTP API endpoints for storefront actions.

Functions:
- parse request input 
- get current_user
- call service functions
- retrun JSON responses 
"""
 ############ THIS FILE NEEDS TO BE UPDATED ######################

from flask import Blueprint, request, jsonify

from services.storefront_service import (
    create_storefront_service,
    get_my_storefront_service,
    update_storefront_service,
    deactivate_storefront_service
)

storefront_bp = Blueprint("storefront_bp", __name__, url_prefix="/api/storefronts")


def get_current_user():
    """
    Temporary user identity method (until real auth is connected):
    Read user from headers.

    Required header for protected routes:
      X-User-Id: <int>

    Optional:
      X-User-Role: user|admin
    """
    user_id = request.headers.get("X-User-Id")
    role = request.headers.get("X-User-Role", "user")

    if not user_id:
        return None

    try:
        return {"id": int(user_id), "role": role}
    except Exception:
        return None


# _________________________________________________________
# CREATE STOREFRONT (User)
# POST /api/storefronts
# _________________________________________________________

@storefront_bp.post("")
def create_storefront_route():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    data = request.get_json(silent=True) or {}

    try:
        storefront = create_storefront_service(current_user, data)
        return jsonify(storefront), 201
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        return jsonify({"error": str(e)}), 400


# _________________________________________________________
# GET MY STOREFRONT (User)
# GET /api/storefronts/me
# _________________________________________________________

@storefront_bp.get("/me")
def get_my_storefront_route():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    try:
        storefront = get_my_storefront_service(current_user)
        if storefront is None:
            return jsonify({"error": "No storefront found for this user."}), 404
        return jsonify(storefront), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# _________________________________________________________
# UPDATE STOREFRONT (Owner/Admin)
# PUT /api/storefronts/<storefront_id>
# _________________________________________________________
@storefront_bp.put("/<int:storefront_id>")
def update_storefront_route(storefront_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    data = request.get_json(silent=True) or {}

    try:
        updated = update_storefront_service(current_user, storefront_id, data)
        return jsonify(updated), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400


# _________________________________________________________
# DEACTIVATE STOREFRONT (Owner/Admin)
# PATCH /api/storefronts/<storefront_id>/deactivate
# _________________________________________________________

@storefront_bp.patch("/<int:storefront_id>/deactivate")
def deactivate_storefront_route(storefront_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "Unauthorized: missing/invalid X-User-Id"}), 401

    try:
        updated = deactivate_storefront_service(current_user, storefront_id)
        return jsonify(updated), 200
    except Exception as e:
        msg = str(e).lower()
        if "unauthorized" in msg:
            return jsonify({"error": str(e)}), 403
        if "not found" in msg:
            return jsonify({"error": str(e)}), 404
        return jsonify({"error": str(e)}), 400
