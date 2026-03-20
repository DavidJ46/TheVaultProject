"""
mock_data.py

Purpose:
Populate the database with mock data for development and testing.

This script inserts sample:
- users
- storefronts
- listings
- listing images
- listing sizes

This allows us to quickly test API endpoints

"""

from db import get_connection


TEST_USER_EMAIL = "TheVaultTester@hamptonu.edu"
ADMIN_EMAIL = "VaultAdmin@hamptonu.edu"


def seed_mock_data():
    conn = get_connection()
    cur = conn.cursor()

    try:
        # -------------------------------------------------------
        # USERS
        # -------------------------------------------------------
        cur.execute(
            """
            INSERT INTO users (username, password, email, role)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
            """,
            ("TheVaultTester", "testpassword", TEST_USER_EMAIL, "user"),
        )

        cur.execute(
            """
            INSERT INTO users (username, password, email, role)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
            """,
            ("VaultAdmin", "adminpassword", ADMIN_EMAIL, "admin"),
        )

        # Get tester user_id
        cur.execute("SELECT id FROM users WHERE email = %s;", (TEST_USER_EMAIL,))
        tester_id = cur.fetchone()[0]

        # -------------------------------------------------------
        # STOREFRONT (one per user)
        # -------------------------------------------------------
        cur.execute(
            """
            INSERT INTO storefronts
                (owner_id, brand_name, bio, logo_url, banner_url, instagram_handle, is_active)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (owner_id) DO NOTHING;
            """,
            (
                tester_id,
                "The Vault Test Brand",
                "Sample storefront used for testing The Vault marketplace system.",
                "https://example.com/logo.png",
                "https://example.com/banner.png",
                None,   # instagram_handle (not required)
                True,
            ),
        )

        # Get storefront_id
        cur.execute("SELECT id FROM storefronts WHERE owner_id = %s;", (tester_id,))
        storefront_id = cur.fetchone()[0]

        # -------------------------------------------------------
        # LISTING
        # -------------------------------------------------------
        cur.execute(
            """
            INSERT INTO listings
                (storefront_id, title, description, price, fulfillment_type, quantity_on_hand, sizes_available, status)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                storefront_id,
                "Vault Hoodie",
                "Official test hoodie used for system testing.",
                45.00,
                "IN_STOCK",
                10,
                '["S","M","L","XL"]',
                "ACTIVE",
            ),
        )

        row = cur.fetchone()
        if row:
            listing_id = row[0]
        else:
            # Fallback (should rarely happen): select an existing listing
            cur.execute(
                """
                SELECT id FROM listings
                WHERE storefront_id = %s AND title = %s
                ORDER BY created_at DESC
                LIMIT 1;
                """,
                (storefront_id, "Vault Hoodie"),
            )
            listing_id = cur.fetchone()[0]

        # -------------------------------------------------------
        # LISTING IMAGE (primary)
        # -------------------------------------------------------
        cur.execute(
            """
            INSERT INTO listing_images (listing_id, image_url, is_primary)
            VALUES (%s, %s, %s);
            """,
            (listing_id, "https://example.com/vault-hoodie.png", True),
        )

        # -------------------------------------------------------
        # LISTING SIZES (inventory per size)
        # -------------------------------------------------------
        sizes = [("S", 2), ("M", 3), ("L", 3), ("XL", 2)]
        for size, qty in sizes:
            cur.execute(
                """
                INSERT INTO listing_sizes (listing_id, size, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (listing_id, size)
                DO UPDATE SET quantity = EXCLUDED.quantity;
                """,
                (listing_id, size, qty),
            )

        conn.commit()
        print("Mock data inserted successfully.")
        print(f"Tester user_id: {tester_id}")
        print(f"Storefront id: {storefront_id}")
        print(f"Listing id: {listing_id}")

    except Exception as e:
        conn.rollback()
        print("Error inserting mock data:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed_mock_data()
