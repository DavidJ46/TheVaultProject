import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() # This pulls your Endpoint/Username from the .env file

try:
    # Attempt to "knock on the door" of the RDS server
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    print("SUCCESS: Your laptop is authorized. You have access to The Vault!")
    conn.close()
except Exception as e:
    print(f"CONNECTION FAILED: {e}")
