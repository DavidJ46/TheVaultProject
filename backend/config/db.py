#Initializes AWS RDS Credentials

import os #Allows files to manage files, see directory paths, and read environment
import psycopg2 #Allows for Python to manage PostgreSQL databases
from dotenv import load_dotenv #Loads the keys from the hidden .env file

load_dotenv

def get_db_connection():
    try: 
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'), #The web address of the database server
            database=os.getenv('DB_NAME'), #The name of the database
            user=os.getenv('DB_USER'), #database login credentials
            password=os.getenv('DB_PASSWORD') #database login credentials
        )

        print("Login Logic: Connected to AWS RDS")
        return conn

    except Exception as e:
        print(f"Login Logic: Connection Error: {e}")
        return None