import os
import urllib.parse as up
from dotenv import load_dotenv

load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

dbname = os.getenv("DATABASE_NAME")
db_user = os.getenv("D_USER")
db_pass = os.getenv("D_PASS")
FLICKR_API_KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
LOCAL = os.getenv("LOCAL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HOST = os.getenv("HOST")
ELEPHANTSQLCRED = os.getenv("ELEPHANTSQLCRED")
ELE_PASS = os.getenv("ELE_PASS")
