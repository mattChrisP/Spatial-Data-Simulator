import psycopg2
import requests
import shutil
from psycopg2 import sql
from rtree import index

from constants import (
    GOOGLE_API_KEY, dbname, db_user, db_pass
)
from utils import SpatialData



# def find_place(input, api_key):
#     url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype=textquery&fields=photos,formatted_address,name,geometry&key={api_key}"

#     response = requests.get(url)
#     json = response.json()

#     return json['candidates'][0]['photos'][0]['photo_reference']


# def get_photo(photo_reference, api_key, max_width=400):
#     url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={api_key}"

#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         with open('output.jpg', 'wb') as out_file:
#             shutil.copyfileobj(response.raw, out_file)
#         print("Image downloaded to output.jpg")
#     else:
#         print("Unable to download image")

# # Replace with your actual API Key
# api_key = GOOGLE_API_KEY

# place_name = "Lim Bo Seng Memorial"

# # Step 1: Find Place
# photo_reference = find_place(place_name, api_key)

# # Step 3: Get Photo
# print(get_photo(photo_reference, api_key))

instance = SpatialData(db_pass=db_pass,db_user=db_user,dbname=dbname)
print(instance.get_names()[0][0])