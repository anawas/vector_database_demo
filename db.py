import os
from dotenv import load_dotenv
import psycopg2

def get_connection():
    load_dotenv()

    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER_NAME", "postgres"),
        password=os.getenv("DB_USER_PASSWORD", None),
        host=os.getenv("DB_HOST", "localhost")
    )
