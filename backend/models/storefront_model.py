# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
models/storefront_model.py

Purpose:
This file is responsible for direct communication with the `storefronts` table
in the PostgreSQL database using psycopg2.

This file will:
- Execute SQL queries related to storefronts
- Insert new storefront records
- Retrieve storefront data
- Update storefront data
- Return database results in a structured (dictionary) format
"""

from db import get_connection


def create_storefront(owner_id, brand_name, bio=None, logo_url=None, banner_url=None, instagram_handle=None):
    """
    Inserts a new storefront into the database and returns the newly created storefront
    as a dictionary.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO storefronts (owner_id, brand_name, bio, logo_url, banner_url, instagram_handle)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, owner_id, brand_name, bio, logo_url,
                  banner_url, instagram_handle, is_active,
                  created_at, updated_at;
    """

    cur.execute(query, (owner_id, brand_name, bio, logo_url, banner_url, instagram_handle))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "owner_id": row[1],
        "brand_name": row[2],
        "bio": row[3],
        "logo_url": row[4],
        "banner_url": row[5],
        "instagram_handle": row[6],
        "is_active": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def get_storefront_by_id(storefront_id):
    """
    Retrieves a storefront by its primary key (id).
    Returns None if not found.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, owner_id, brand_name, bio, logo_url,
               banner_url, instagram_handle, is_active,
               created_at, updated_at
        FROM storefronts
        WHERE id = %s;
    """

    cur.execute(query, (storefront_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "owner_id": row[1],
        "brand_name": row[2],
        "bio": row[3],
        "logo_url": row[4],
        "banner_url": row[5],
        "instagram_handle": row[6],
        "is_active": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def get_storefront_by_owner_id(owner_id):
    """
    Retrieves the storefront owned by a specific user (owner_id).
    Used for endpoints like GET /api/storefronts/me.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, owner_id, brand_name, bio, logo_url,
               banner_url, instagram_handle, is_active,
               created_at, updated_at
        FROM storefronts
        WHERE owner_id = %s;
    """

    cur.execute(query, (owner_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "owner_id": row[1],
        "brand_name": row[2],
        "bio": row[3],
        "logo_url": row[4],
        "banner_url": row[5],
        "instagram_handle": row[6],
        "is_active": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def update_storefront(storefront_id, brand_name=None, bio=None, logo_url=None, banner_url=None, instagram_handle=None):
    """
    Updates editable storefront fields.
    Only fields that are not None will overwrite existing values.
    Returns the updated storefront dictionary, or None if the storefront doesn't exist.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE storefronts
        SET brand_name = COALESCE(%s, brand_name),
            bio = COALESCE(%s, bio),
            logo_url = COALESCE(%s, logo_url),
            banner_url = COALESCE(%s, banner_url),
            instagram_handle = COALESCE(%s, instagram_handle),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, owner_id, brand_name, bio, logo_url,
                  banner_url, instagram_handle, is_active,
                  created_at, updated_at;
    """

    cur.execute(query, (brand_name, bio, logo_url, banner_url, instagram_handle, storefront_id))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "owner_id": row[1],
        "brand_name": row[2],
        "bio": row[3],
        "logo_url": row[4],
        "banner_url": row[5],
        "instagram_handle": row[6],
        "is_active": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def set_storefront_active(storefront_id, is_active):
    """
    Activates or deactivates a storefront.
    This is a soft action (preferred over deleting storefront records).
    Often used for admin moderation or temporarily disabling a storefront.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE storefronts
        SET is_active = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, owner_id, brand_name, bio, logo_url,
                  banner_url, instagram_handle, is_active,
                  created_at, updated_at;
    """

    cur.execute(query, (is_active, storefront_id))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "owner_id": row[1],
        "brand_name": row[2],
        "bio": row[3],
        "logo_url": row[4],
        "banner_url": row[5],
        "instagram_handle": row[6],
        "is_active": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }
