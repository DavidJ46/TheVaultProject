# models/admin_model.py

"""
Database queries used by the admin dashboard.
"""

from db import get_connection
from models.listing_model import soft_delete_listing
from models.return_model import get_all_returns, update_return_status
from models.storefront_model import get_all_storefronts


def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email, role, created_at
        FROM users
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "role": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]


def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_all_listings():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT l.id, l.title, l.price, l.status, l.storefront_id, s.brand_name, l.updated_at
        FROM listings l
        LEFT JOIN storefronts s ON s.id = l.storefront_id
        ORDER BY l.updated_at DESC, l.id DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "price": float(row[2]),
            "status": row[3],
            "storefront_id": row[4],
            "storefront_name": row[5],
            "updated_at": row[6],
        }
        for row in rows
    ]


def delete_listing(listing_id):
    return soft_delete_listing(listing_id)


def get_admin_storefronts():
    return get_all_storefronts()


def get_admin_returns():
    return get_all_returns(include_deleted=False)


def update_admin_return_status(return_id, status):
    return update_return_status(return_id, status)
