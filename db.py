import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


load_dotenv()

dbname = os.getenv("DATABASE_NAME")
db_user = os.getenv("D_USER")
db_pass = os.getenv("D_PASS")

# Connect to your postgres DB
try:
    conn = psycopg2.connect(f"dbname={dbname} user={db_user} password={db_pass}")
except psycopg2.Error as e:
    print(f"Error: Could not make connection to the Postgres database\n{e}")
    exit()

try:
    # Open a cursor to perform database operations
    cur = conn.cursor()
except psycopg2.Error as e:
    print(f"Error: Could not get curser to the Database\n{e}")
    exit()

try:
    # Enable PostGIS (includes raster)
    cur.execute("CREATE EXTENSION postgis;")

    # Enable Topology
    cur.execute("CREATE EXTENSION postgis_topology;")

    # Create a new table with a spatial column
    cur.execute("""
        CREATE TABLE locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            importance INTEGER,
            geom GEOMETRY(Point, 4326)
        );
    """)

    # Variables for insertion
    name = "Location 1"
    importance = 10
    longitude = 40.712776
    latitude = -74.005974

    # Insert a new point
    insert = sql.SQL("""
        INSERT INTO locations (name, importance, geom) 
        VALUES (
            {}, 
            {}, 
            ST_SetSRID(ST_MakePoint({}, {}), 4326)
        );
    """).format(sql.Identifier(name), sql.Identifier(importance), sql.Identifier(longitude), sql.Identifier(latitude))

    cur.execute(insert)

    # Query the nearest point
    cur.execute("""
        SELECT name, ST_Distance(geom::geography, ST_MakePoint(40.7128, -74.0060)::geography) AS distance
        FROM locations 
        ORDER BY distance
        LIMIT 1;
    """)

    print(cur.fetchone())
except psycopg2.Error as e:
    print(f"Error: Issue creating table")
    print (e)

try:
    # Commit changes and close communication with the PostgreSQL database server
    conn.commit()
    cur.close()
    conn.close()
except psycopg2.Error as e:
    print(f"Error: Could not close the curser & connection")
    print(e)