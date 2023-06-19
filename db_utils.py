import psycopg2
from psycopg2 import sql


class SpatialData:


    def __init__(self, dbname, db_user, db_pass):
        self.cur, self.conn = None, None
        # Connect to your postgres DB
        try:
            self.conn = psycopg2.connect(f"dbname={dbname} user={db_user} password={db_pass}")
        except psycopg2.Error as e:
            print(f"Error: Could not make connection to the Postgres database\n{e}")
            return e

        try:
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error: Could not get curser to the Database\n{e}")
            return e
        
        try:
            # Enable PostGIS (includes raster)
            self.cur.execute("CREATE EXTENSION postgis;")

            # Enable Topology
            self.cur.execute("CREATE EXTENSION postgis_topology;")

            # Create a new table with a spatial column
            self.cur.execute("""
                CREATE TABLE locations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    importance double precision,
                    geom GEOMETRY(Point, 4326)
                );
            """)

        except psycopg2.Error as e:
            print(f"Error: Issue creating table\n{e}")
            return e
        return None



    def insert_data(self, name="Default", imp=None, long=None, lat=None):
        insert = sql.SQL("""
        INSERT INTO locations (name, importance, geom) 
        VALUES (
            {}, 
            {}, 
            ST_SetSRID(ST_MakePoint({}, {}), 4326)
            );
        """).format(sql.Identifier(name), sql.Identifier(imp), sql.Identifier(long), sql.Identifier(lat))
        try:
            self.cur.execute(insert)
        except psycopg2.Error as e:
            print(f"Error: Issue inserting data\n{e}")
            return e
        return None


    def query_nearest(self, k):
        self.cur.execute(f"""
        SELECT name, ST_Distance(geom::geography, ST_MakePoint(40.7128, -74.0060)::geography) AS distance
        FROM locations 
        ORDER BY distance
        LIMIT {k};
        """)

        print(self.cur.fetchone())
        pass


    def query_rect():
        pass