
import psycopg2
from psycopg2 import sql

from utils import SpatialData

from constants import (
    dbname, db_user, db_pass
)



test = SpatialData(dbname=dbname, db_user=db_user, db_pass=db_pass)
test.insert_data(imp=10, long=7.8, lat=10.7)
test.insert_data(imp=10, long=8, lat=10.7)
test.insert_data(imp=10, long=9, lat=10.7)
test.insert_data(imp=10, long=100, lat=10.7)
test.insert_data(imp=10, long=55, lat=10.7)
test.insert_data(imp=10, long=3, lat=4)



print(test.query_nearest(3, 10, 7))


test.close_connection()