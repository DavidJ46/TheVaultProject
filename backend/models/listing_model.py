"""
listing_model.py file
Created by: Day Ekoi 

Purpose: This file handles all direct database operations related to the 'listings' table
in PostgreSQL using psycopg2.

IT will:
- Insert new listing records 
- Retrieve listing data
- Update listing data
- soft Delete listings (status = 'DELETED')
- Return results as dictionaries 

"""

from db import get_connection()

def create_listing(storefront_id, title, description, price, 
                   fullfillment_type, quanitity_on_hand=None,
                   sizes_available=None, status="ACTIVE"):

"""
This inserts a new listing and returns the created listing as a dictionary.
"""

conn = get_connection()
cur - conn.cursor()

query =  """
        INSERT INTO listings
        (storefront_id, title, description, price, fulfillment_type, quantity_on_hand, sizes_available, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, storefront_id, title, description, price,
                  fulfillment_type, quantity_on_hand, sizes_available,
                  status, created_at, updated_at;
    """
cur.execute(query, (
    storefront_id, title, description, price,
    fulfillment_type, quantity_on_hand, sizes_available, status
 ))

row = cur.fetchone()
conn.commit()

cur.close()
conn.close()

return {
        "id": row[0],
        "storefront_id": row[1],
        "title": row[2],
        "description": row[3],
        "price": float(row[4]),
        "fulfillment_type": row[5],
        "quantity_on_hand": row[6],
        "sizes_available": row[7],
        "status": row[8],
        "created_at": row[9],
        "updated_at": row[10],
    }

def get_listing_by_id(listing_id):
  """
  Retrieves a listing by its PK (id). Returns none if not found
  """

conn = get_connection()
cur = conn.cursor()

query = """
        SELECT id, storefront_id, title, description, price,
               fulfillment_type, quantity_on_hand, sizes_available,
               status, created_at, updated_at
        FROM listings
        WHERE id = %s;
    """

    cur.execute(query, (listing_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "storefront_id": row[1],
        "title": row[2],
        "description": row[3],
        "price": float(row[4]),
        "fulfillment_type": row[5],
        "quantity_on_hand": row[6],
        "sizes_available": row[7],
        "status": row[8],
        "created_at": row[9],
        "updated_at": row[10],
    }


def get_listings_by_storefront_id(storefront_id):
    """
    Retrieves all listings for a storefront (used for a storefront page).
    Returns a list of listing dictionaries.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, storefront_id, title, description, price,
               fulfillment_type, quantity_on_hand, sizes_available,
               status, created_at, updated_at
        FROM listings
        WHERE storefront_id = %s
          AND status != 'DELETED'
        ORDER BY created_at DESC;
    """

    cur.execute(query, (storefront_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    listings = []
    for row in rows:
        listings.append({
            "id": row[0],
            "storefront_id": row[1],
            "title": row[2],
            "description": row[3],
            "price": float(row[4]),
            "fulfillment_type": row[5],
            "quantity_on_hand": row[6],
            "sizes_available": row[7],
            "status": row[8],
            "created_at": row[9],
            "updated_at": row[10],
        })

    return listings


def update_listing(listing_id, title=None, description=None, price=None,
                   fulfillment_type=None, quantity_on_hand=None,
                   sizes_available=None, status=None):
    """
    Updates editable listing fields using COALESCE, returns updated listing.
    Returns None if listing does not exist.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE listings
        SET title = COALESCE(%s, title),
            description = COALESCE(%s, description),
            price = COALESCE(%s, price),
            fulfillment_type = COALESCE(%s, fulfillment_type),
            quantity_on_hand = COALESCE(%s, quantity_on_hand),
            sizes_available = COALESCE(%s, sizes_available),
            status = COALESCE(%s, status),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, storefront_id, title, description, price,
                  fulfillment_type, quantity_on_hand, sizes_available,
                  status, created_at, updated_at;
    """

    cur.execute(query, (
        title, description, price,
        fulfillment_type, quantity_on_hand,
        sizes_available, status,
        listing_id
    ))

    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "storefront_id": row[1],
        "title": row[2],
        "description": row[3],
        "price": float(row[4]),
        "fulfillment_type": row[5],
        "quantity_on_hand": row[6],
        "sizes_available": row[7],
        "status": row[8],
        "created_at": row[9],
        "updated_at": row[10],
    }


def soft_delete_listing(listing_id):
    """
    Soft deletes a listing by setting status = 'DELETED'.
    """

    return update_listing(listing_id, status="DELETED")
