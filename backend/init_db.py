"""
init_db.py

Purpose:
This file initializes the PostgreSQL database schema for The Vault.
It creates all required database tables if they do not already exist.

Run this file manually when:
- Setting up the project for the first time
- Deploying to a new environment
- Ensuring the database schema is properly initialized
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def create_vault_tables():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()

        # ________________________________________________________
        # USERS TABLE
        # ________________________________________________________
        create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                role VARCHAR(10) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        cur.execute(create_users_table)

        # ________________________________________________________
        # STOREFRONTS TABLE (One storefront per user)
        # Added by Day Ekoi 2/26/26
        # ________________________________________________________
        create_storefronts_table = """
            CREATE TABLE IF NOT EXISTS storefronts (
                id SERIAL PRIMARY KEY,
                owner_id INTEGER NOT NULL UNIQUE,
                brand_name VARCHAR(80) NOT NULL,
                bio TEXT,
                logo_url TEXT,
                banner_url TEXT,
                instagram_handle VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_storefront_owner
                    FOREIGN KEY(owner_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );
        """
        cur.execute(create_storefronts_table)

        # ________________________________________________________
        # LISTINGS TABLE (Each listing belongs to a storefront)
        # Added by Day Ekoi 2/26/26
        # ________________________________________________________
        create_listings_table = """
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                storefront_id INTEGER NOT NULL,

                title VARCHAR(120) NOT NULL,
                description TEXT,
                price NUMERIC(10,2) NOT NULL CHECK (price >= 0),

                fulfillment_type VARCHAR(20) NOT NULL
                    CHECK (fulfillment_type IN ('IN_STOCK', 'PREORDER')),

                quantity_on_hand INTEGER CHECK (quantity_on_hand >= 0),

                sizes_available TEXT,

                status VARCHAR(20) DEFAULT 'ACTIVE'
                    CHECK (status IN ('ACTIVE', 'INACTIVE', 'SOLD_OUT', 'DELETED')),

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_listing_storefront
                    FOREIGN KEY(storefront_id)
                    REFERENCES storefronts(id)
                    ON DELETE CASCADE
            );
        """
        cur.execute(create_listings_table)

        # ________________________________________________________
        # LISTING IMAGES TABLE (Multiple images per listing)
        # Added by Day Ekoi 2/26/26
        # ________________________________________________________
        create_listing_images_table = """
            CREATE TABLE IF NOT EXISTS listing_images (
                id SERIAL PRIMARY KEY,
                listing_id INTEGER NOT NULL,
                image_url TEXT NOT NULL,
                is_primary BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_image_listing
                    FOREIGN KEY(listing_id)
                    REFERENCES listings(id)
                    ON DELETE CASCADE
            );
        """
        cur.execute(create_listing_images_table)

        # ________________________________________________________
        # LISTING SIZES TABLE (Inventory per size)
        # Added by Day Ekoi 2/26/26
        # ________________________________________________________
        create_listing_sizes_table = """
            CREATE TABLE IF NOT EXISTS listing_sizes (
                id SERIAL PRIMARY KEY,
                listing_id INTEGER NOT NULL,
                size VARCHAR(20) NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_size_listing
                    FOREIGN KEY(listing_id)
                    REFERENCES listings(id)
                    ON DELETE CASCADE,

                CONSTRAINT unique_listing_size
                    UNIQUE (listing_id, size)
            );
        """
        cur.execute(create_listing_sizes_table)

        # ________________________________________________________
        # PURCHASES TABLE (Purchase history for users)
        # Added by Elali McNair 3/3/26
        # The frontend protion of this code is not finished or implemented yet. Therfore, this code is not oporational or properly implemented yet.
        # ________________________________________________________
        create_purchases_table = """
            CREATE TABLE IF NOT EXISTS purchases (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                listing_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                purchase_price NUMERIC(10,2) NOT NULL CHECK (purchase_price >= 0),
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_purchase_user
                    FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                CONSTRAINT fk_purchase_listing
                    FOREIGN KEY(listing_id)
                    REFERENCES listings(id)
                    ON DELETE CASCADE
            );
        """
        cur.execute(create_purchases_table)

        # ________________________________________________________
        # WISHLIST TABLE (User wishlists)
        # Added by Elali McNair 3/3/26
        # The frontend protion of this code is not finished or implemented yet. Therfore, this code is not oporational or properly implemented yet.
        # ________________________________________________________
        create_wishlist_table = """
            CREATE TABLE IF NOT EXISTS wishlist (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                listing_id INTEGER NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_wishlist_user
                    FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                CONSTRAINT fk_wishlist_listing
                    FOREIGN KEY(listing_id)
                    REFERENCES listings(id)
                    ON DELETE CASCADE,

                CONSTRAINT unique_user_listing_wishlist
                    UNIQUE (user_id, listing_id)
            );
        """
        cur.execute(create_wishlist_table)

        conn.commit()

        print("DATABASE INITIALIZED: users, storefronts, listings, listing_images, listing_sizes, purchases, and wishlist tables are ready.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"SCHEMA ERROR: {e}")


if __name__ == "__main__":
    create_vault_tables()
