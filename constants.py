import os
from dotenv import load_dotenv

load_dotenv()

dbname = os.getenv("DATABASE_NAME")
db_user = os.getenv("D_USER")
db_pass = os.getenv("D_PASS")
FLICKR_API_KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
LOCAL = os.getenv("LOCAL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")