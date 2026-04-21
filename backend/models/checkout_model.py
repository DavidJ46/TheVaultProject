# The Vault Campus Marketplace
# CSC 405 Sp 26'

"""
models/checkout_model.py

Purpose:
This file is responsible for direct communication with checkout-related
database tables using psycopg2.

This file will:
- Retrieve saved checkout/user information
- Retrieve cart items for a user
- Insert order records
- Insert order item records
- Clear cart items after successful checkout
- Return database results in structured dictionary format
"""

from db import get_connection


def get_checkout_user_info(user_id):
    """
    Retrieves saved checkout information for a user.
    Returns None if user is not found.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT id, first_name, last_name, email, phone_number,
               address_line_1, address_line_2, city, state, zip_code
        FROM users
        WHERE id = %s;
    """

    cur.execute(query, (user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "email": row[3],
        "phone_number": row[4],
        "address_line_1": row[5],
        "address_line_2": row[6],
        "city": row[7],
        "state": row[8],
        "zip_code": row[9],
    }


def get_cart_items_for_user(user_id):
    """
    Retrieves all cart items for a user, joined with listing/storefront data
    needed for checkout display and pricing.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            ci.id AS cart_item_id,
            ci.user_id,
            ci.listing_id,
            ci.quantity,
            ci.selected_size,

            l.storefront_id,
            l.title,
            l.price,
            l.fulfillment_type,
            l.quantity_on_hand,
            l.status,

            s.brand_name

        FROM cart_items ci
        JOIN listings l ON ci.listing_id = l.id
        JOIN storefronts s ON l.storefront_id = s.id
        WHERE ci.user_id = %s
        ORDER BY ci.id ASC;
    """

    cur.execute(query, (user_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    cart_items = []
    for row in rows:
        cart_items.append({
            "cart_item_id": row[0],
            "user_id": row[1],
            "listing_id": row[2],
            "quantity": row[3],
            "selected_size": row[4],
            "storefront_id": row[5],
            "title": row[6],
            "price": row[7],
            "fulfillment_type": row[8],
            "quantity_on_hand": row[9],
            "status": row[10],
            "brand_name": row[11],
        })

    return cart_items


def create_order(user_id, total_amount, order_status="SUBMITTED"):
    """
    Inserts a new order and returns the created order record.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO orders (user_id, total_amount, order_status)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, total_amount, order_status, created_at;
    """

    cur.execute(query, (user_id, total_amount, order_status))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "user_id": row[1],
        "total_amount": row[2],
        "order_status": row[3],
        "created_at": row[4],
    }


def create_order_item(order_id, listing_id, quantity, price_at_purchase, selected_size=None):
    """
    Inserts a new order item record and returns the created order item.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO order_items (order_id, listing_id, quantity, price_at_purchase, selected_size)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, order_id, listing_id, quantity, price_at_purchase, selected_size;
    """

    cur.execute(query, (order_id, listing_id, quantity, price_at_purchase, selected_size))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "order_id": row[1],
        "listing_id": row[2],
        "quantity": row[3],
        "price_at_purchase": row[4],
        "selected_size": row[5],
    }


def clear_cart_for_user(user_id):
    """
    Deletes all cart items for a user after successful checkout.
    Returns number of rows deleted.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        DELETE FROM cart_items
        WHERE user_id = %s;
    """

    cur.execute(query, (user_id,))
    deleted_count = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return {"deleted_count": deleted_count}


def update_listing_inventory(listing_id, new_quantity, new_status=None):
    """
    Updates listing inventory after checkout.
    If new_status is provided, it will also update listing status.
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE listings
        SET quantity_on_hand = %s,
            status = COALESCE(%s, status),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, quantity_on_hand, status, updated_at;
    """

    cur.execute(query, (new_quantity, new_status, listing_id))
    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "quantity_on_hand": row[1],
        "status": row[2],
        "updated_at": row[3],
    }