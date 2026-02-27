"""
db.py

Purpose:
This file provides a centralized database connection utility
for runtime application operations.

This file:
- Loads environment variables
- Establishes PostgreSQL connections
- Returns a reusable get_connection() function
- Is used by models to execute SQL queries
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    
    Creates and returns a new PostgreSQL connection for runtime DB operations.
    Uses the same environment variables as init_db.py.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
