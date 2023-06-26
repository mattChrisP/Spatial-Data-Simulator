
import psycopg2
from psycopg2 import sql

from utils import SpatialData

from constants import (
    dbname, db_user, db_pass
)



test = SpatialData(dbname=dbname, db_user=db_user, db_pass=db_pass)
# test.insert_data(imp=10, long=7.8, lat=10.7, tags=["genshin","valo"])
# test.insert_data(imp=10, long=8, lat=10.7, tags=["valo"])
# test.insert_data(imp=10, long=9, lat=10.7, tags=["valo"])
# test.insert_data(imp=10, long=100, lat=10.7, tags=["genshin"])
# test.insert_data(imp=10, long=55, lat=10.7, tags=["genshin"])
# test.insert_data(imp=10, long=3, lat=4, tags=["valo"])



print(test.query_nearest_by_tag(3, 100, 11, tag=["valo"]))


test.close_connection()