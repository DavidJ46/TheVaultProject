# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
models/listing_size_model.py

Purpose:
Direct DB operations for the listing_sizes table.

This file will:
- Insert or update size inventory for a listing
- Retrieve size inventory for a listing
- Delete a size record
"""

from db import get_connection


def upsert_listing_size(listing_id, size, quantity):
    """
    Creates or updates a size row for a listing.

    Updates quantity if (listing_id, size) already exists.
    Returns the upserted row as a dictionary.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO listing_sizes (listing_id, size, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (listing_id, size)
        DO UPDATE SET quantity = EXCLUDED.quantity
        RETURNING id, listing_id, size, quantity, created_at;
    """
    cur.execute(query, (listing_id, size, quantity))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "listing_id": row[1],
        "size": row[2],
        "quantity": row[3],
        "created_at": row[4],
    }


def get_sizes_for_listing(listing_id):
    """
    Returns all size inventory rows for a listing.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, listing_id, size, quantity, created_at
        FROM listing_sizes
        WHERE listing_id = %s
        ORDER BY size ASC;
    """
    cur.execute(query, (listing_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    sizes = []
    for row in rows:
        sizes.append({
            "id": row[0],
            "listing_id": row[1],
            "size": row[2],
            "quantity": row[3],
            "created_at": row[4],
        })

    return sizes


def delete_listing_size(listing_id, size):
    """
    Deletes a size row for a listing.
    Returns True if something was deleted, False otherwise.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM listing_sizes WHERE listing_id = %s AND size = %s;",
        (listing_id, size)
    )
    deleted = cur.rowcount > 0
    conn.commit()

    cur.close()
    conn.close()

    return deleted
