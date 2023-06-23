import uuid
import psycopg2
from psycopg2 import sql

from constants import (
    dbname, db_user, db_pass
)

class Register:

    def __init__(self):
        self.id = uuid.uuid1()

        self.cur, self.conn = None, None
        # Connect to your postgres DB
        try:
            self.conn = psycopg2.connect(f"dbname={dbname} user={db_user} password={db_pass}")
        except psycopg2.Error as e:
            print(f"Error: Could not make connection to the Postgres database\n{e}")

        try:
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error: Could not get curser to the Database\n{e}")

        try:

            # Create a new table with a spatial column
            self.cur.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255)
                );
            """)

        except psycopg2.Error as e:
            print(f"Error: Issue creating table\n{e}")

    def get_id(self):
        insert = sql.SQL(f"""
        INSERT INTO users (name) 
        VALUES (
            {self.id}
            );
        """)
        try:
            self.cur.execute(insert)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error: Issue inserting data\n{e}")
            return e
        return self.id
