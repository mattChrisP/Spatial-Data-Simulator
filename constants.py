import os
import urllib.parse as up
from dotenv import load_dotenv

load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])


FLICKR_API_KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ENCODED_JSON = os.getenv("MY_JSON_FILE")
