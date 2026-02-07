import psycopg2
import os
from dotenv import load_dotenv

# Load the credentials your teammate provided
load_dotenv()

def create_vault_tables():
    try:
        # Establish the connection using the Success-verified settings
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cur = conn.cursor()
        
        # SQL command to build the users table structure
        # 'IF NOT EXISTS' prevents errors if the table is already there
        create_table_command = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        
        cur.execute(create_table_command)
        conn.commit() # This saves the table to AWS
        print("✅ DATABASE INITIALIZED: The 'users' table is now live in the cloud.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ SCHEMA ERROR: {e}")

if __name__ == "__main__":
    create_vault_tables()