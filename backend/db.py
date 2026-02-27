import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Creates and returns a new PostgreSQL connection
    using environment variables.
    Supports AWS RDS SSL configuration if provided.
    """
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5432")

    sslmode = os.getenv("SSL_MODE")
    sslrootcert = os.getenv("SSL_ROOT_CERT")

    conn_kwargs = {
        "host": host,
        "database": dbname,
        "user": user,
        "password": password,
        "port": port,
    }

    # Only attach SSL settings if provided
    if sslmode:
        conn_kwargs["sslmode"] = sslmode

    if sslrootcert:
        conn_kwargs["sslrootcert"] = sslrootcert

    return psycopg2.connect(**conn_kwargs)
