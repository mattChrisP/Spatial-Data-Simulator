import psycopg2
from psycopg2 import sql
from rtree import index


class SpatialData:

    def __init__(self, dbname, db_user, db_pass):
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
            # # Enable PostGIS (includes raster)
            # self.cur.execute("CREATE EXTENSION postgis;")

            # # Enable Topology
            # self.cur.execute("CREATE EXTENSION postgis_topology;")

            # Create a new table with a spatial column
            self.cur.execute("""
                CREATE TABLE locations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    importance double precision,
                    tags text[], 
                    geom GEOMETRY(Point, 4326)
                );
            """)

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error: Issue creating table\n{e}")


    def insert_data(self, name="Default", imp=None, long=None, lat=None, tags=None):
        c_tag = '{' + ','.join(map(str, tags)) + '}'
        insert = sql.SQL(f"""
        INSERT INTO locations (name, importance, tags, geom) 
        VALUES (
            {name}, 
            {imp}, 
            '{c_tag}'::text[],
            ST_SetSRID(ST_MakePoint({long}, {lat}), 4326)
            );
        """)
        try:
            self.cur.execute(insert)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error: Issue inserting data\n{e}")
            return e
        return None


    def query_nearest(self, k, long, lat):
        self.cur.execute(f"""
            SELECT name, ST_X(geom), ST_Y(geom), ST_Distance(geom::geography, ST_MakePoint({long}, {lat})::geography) AS distance
            FROM locations 
            ORDER BY distance
            LIMIT {k};
        """)
        res = []
        for r in self.cur:
            res.append(r)
        return res


    def query_rect(self, k, left, bottom, right, top):
        self.cur.execute(f"""
            SELECT name, importance, ST_X(geom), ST_Y(geom) 
            FROM locations 
            WHERE ST_Contains(
                ST_MakeEnvelope({left}, {bottom}, {right}, {top}, 4326),  -- Replace :left, :bottom, :right, :top with the coordinates of your rectangle
                geom
            )
            ORDER BY importance DESC
            LIMIT {k};
        """)
        res = []
        for r in self.cur:
            res.append(r)
        return res
    
    def query_nearest_by_tag(self, k, long, lat, tag=[]):
        c_tag = '{' + ','.join(map(str, tag)) + '}'
        self.cur.execute(f"""
            SELECT name, ST_X(geom), ST_Y(geom), ST_Distance(geom::geography, ST_MakePoint({long}, {lat})::geography) AS distance
            FROM locations 
            WHERE tags @> '{c_tag}'::text[]
            ORDER BY distance
            LIMIT {k};
        """)
        res = []
        for r in self.cur:
            res.append(r)
        return res



    def close_connection(self):  # Add this new method
        try:
            # Close the cursor
            if self.cur is not None:
                self.cur.close()
        except psycopg2.Error as e:
            print(f"Error: Could not close cursor\n{e}")

        try:
            # Close the connection
            if self.conn is not None:
                self.conn.close()
        except psycopg2.Error as e:
            print(f"Error: Could not close connection\n{e}")


class RT:

    def __init__(self):
        p = index.Property()
        self.rt = index.Index(properties=p)
        self.idx = 0


    def insert_point(self, x,y):
        self.rt.insert(self.idx, (float(x), float(y), float(x), float(y)))
        self.idx += 1


    def get_k_most_important_points_in_rect(self, k, x1, y1, x2, y2):
        global rt, data_points
        point_ids = list(rt.intersection((x1, y1, x2, y2)))
        points = [data_points[i] for i in point_ids]
        return sorted(points, key=lambda x: x[3], reverse=True)[:k]


    def get_k_nearest_points_to_location(self, k, x, y):
        global rt, data_points
        point_ids = list(rt.nearest(coordinates=(x,y), num_results=k))
        return [data_points[i] for i in point_ids]

