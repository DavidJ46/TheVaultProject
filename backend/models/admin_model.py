# models/admin_model.py
# File created by David Jackson

"""
Admin Model

This file contains all database-level operations related to admin actions.
The model layer is responsible for executing SQL queries and returning data
from the PostgreSQL database.

Architecture Role:
Controller → Service → Model → Database

The model should ONLY handle database operations and should not contain
business logic.
"""

# Import the database connection function
from db import get_connection


def get_all_users():
    """
    Retrieves every user in the system.

    Returns:
        list: A list of user records from the database.
              Each record contains:
              - user_id
              - username
              - email
              - created_at
    """

    # Establish connection to PostgreSQL
    conn = get_connection()

    # Create cursor to execute SQL queries
    cur = conn.cursor()

    # Execute SQL query
    cur.execute("""
        SELECT user_id, username, email, created_at
        FROM users
        ORDER BY created_at DESC
    """)

    # Fetch all results from the query
    users = cur.fetchall()

    # Close database resources
    cur.close()
    conn.close()

    return users


def delete_user(user_id):
    """
    Removes a user from the system.

    Parameters:
        user_id (int): The unique identifier for the user.

    Behavior:
        Permanently deletes the user record from the users table.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE user_id = %s
    """, (user_id,))

    # Commit the transaction to make the deletion permanent
    conn.commit()

    cur.close()
    conn.close()


def get_all_listings():
    """
    Retrieves every listing in the marketplace.

    Returns:
        list: Listing records including:
              - listing_id
              - title
              - price
              - status
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT listing_id, title, price, status
        FROM listings
        ORDER BY listing_id DESC
    """)

    listings = cur.fetchall()

    cur.close()
    conn.close()

    return listings


def delete_listing(listing_id):
    """
    Deletes a listing from the marketplace.

    Parameters:
        listing_id (int): Unique ID of the listing.

    This allows admins to remove inappropriate or expired listings.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM listings
        WHERE listing_id = %s
    """, (listing_id,))

    conn.commit()

    cur.close()
    conn.close()


def get_all_storefronts():
    """
    Retrieves all storefronts created by users.

    Returns:
        list: Storefront records including:
              - storefront_id
              - name
              - owner_user_id
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT storefront_id, name, owner_user_id
        FROM storefronts
    """)

    stores = cur.fetchall()

    cur.close()
    conn.close()

    return stores
