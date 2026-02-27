# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
models/listing_image_model.py

Purpose:
Direct DB operations for the listing_images table.

This file will:
- Insert listing image records (S3 URLs)
- Retrieve images for a listing
- Delete an image record
- Set a primary image for a listing

"""

from db import get_connection


def add_listing_image(listing_id, image_url, is_primary=False):
    """
    Adds an image URL to a listing.
    Returns the created image record as a dictionary.
    """
    conn = get_connection()
    cur = conn.cursor()

    # If marking as primary, removes any existing primary image first
    if is_primary:
        cur.execute(
            "UPDATE listing_images SET is_primary = FALSE WHERE listing_id = %s;",
            (listing_id,)
        )

    query = """
        INSERT INTO listing_images (listing_id, image_url, is_primary)
        VALUES (%s, %s, %s)
        RETURNING id, listing_id, image_url, is_primary, created_at;
    """
    cur.execute(query, (listing_id, image_url, is_primary))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "listing_id": row[1],
        "image_url": row[2],
        "is_primary": row[3],
        "created_at": row[4],
    }


def get_images_for_listing(listing_id):
    """
    Returns all images for a listing (primary first).
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, listing_id, image_url, is_primary, created_at
        FROM listing_images
        WHERE listing_id = %s
        ORDER BY is_primary DESC, created_at ASC;
    """
    cur.execute(query, (listing_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    images = []
    for row in rows:
        images.append({
            "id": row[0],
            "listing_id": row[1],
            "image_url": row[2],
            "is_primary": row[3],
            "created_at": row[4],
        })

    return images


def set_primary_image(listing_id, image_id):
    """
    Marks a specific image as the primary image for that listing.
    Returns the updated image record, or None if not found.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Unset old primary
    cur.execute(
        "UPDATE listing_images SET is_primary = FALSE WHERE listing_id = %s;",
        (listing_id,)
    )

    # Set new primary
    query = """
        UPDATE listing_images
        SET is_primary = TRUE
        WHERE id = %s AND listing_id = %s
        RETURNING id, listing_id, image_url, is_primary, created_at;
    """
    cur.execute(query, (image_id, listing_id))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "listing_id": row[1],
        "image_url": row[2],
        "is_primary": row[3],
        "created_at": row[4],
    }


def delete_listing_image(image_id):
    """
    Deletes an image record by image_id.
    Returns True if something was deleted, False otherwise.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM listing_images WHERE id = %s;", (image_id,))
    deleted = cur.rowcount > 0
    conn.commit()

    cur.close()
    conn.close()

    return deleted
