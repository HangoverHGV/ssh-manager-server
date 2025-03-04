
"""
This module is used to wait for the database to be ready before starting the application.
"""

import time
import os
import psycopg2
from psycopg2 import OperationalError


def wait_for_db():
    db_host = os.environ.get("POSTGRES_HOST")
    db_port = os.environ.get("POSTGRES_PORT")
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_name = os.environ.get("POSTGRES_DB")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.close()
            print("Database is ready!")
            return True
        except OperationalError:
            print("Database is not ready, waiting...")
            time.sleep(2)
