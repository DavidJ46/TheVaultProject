"""
mock_data.py

Purpose:
Populate the database with mock data for development and testing.

This script inserts sample:
- users
- storefronts
- listings
- listing images

This allows for quick API endpoints tests

"""

from db import get_connection


def insert_users(cur):
    """Insert mock users"""
    cur.execute("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES
        ('TheVaultTester', 'TheVaultTester@hamptonu.edu', 'hashedpassword', 'user'),
        ('VaultAdmin', 'VaultAdmin@hamptonu.edu', 'hashedpassword', 'admin')
        ON CONFLICT (email) DO NOTHING;
    """)


def insert_storefront(cur):
    """Insert mock storefront"""
    cur.execute("""
        INSERT INTO storefronts (owner_id, brand_name, bio, logo_url, banner_url, is_active)
        VALUES
        (
            1,
            'The Vault Test Brand',
            'Sample storefront used for testing The Vault marketplace system.',
            'https://example.com/logo.png',
            'https://example.com/banner.png',
            TRUE
        )
        ON CONFLICT DO NOTHING;
    """)


def insert_listing(cur):
    """Insert mock listing"""
    cur.execute("""
        INSERT INTO listings (
            storefront_id,
            title,
            description,
            price,
            fulfillment_type,
            quantity_on_hand,
            status
        )
        VALUES
        (
            1,
            'Vault Hoodie',
            'Official test hoodie used for system testing.',
            45.00,
            'IN_STOCK',
            10,
            'ACTIVE'
        )
        ON CONFLICT DO NOTHING;
    """)


def insert_listing_image(cur):
    """Insert mock listing image"""
    cur.execute("""
        INSERT INTO listing_images (
            listing_id,
            image_url,
            is_primary
        )
        VALUES
        (
            1,
            'https://example.com/vault-hoodie.png',
            TRUE
        )
        ON CONFLICT DO NOTHING;
    """)


def seed_mock_data():
    conn = get_connection()
    cur = conn.cursor()

    try:
        insert_users(cur)
        insert_storefront(cur)
        insert_listing(cur)
        insert_listing_image(cur)

        conn.commit()
        print("Mock data inserted successfully.")

    except Exception as e:
        conn.rollback()
        print("Error inserting mock data:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed_mock_data()
