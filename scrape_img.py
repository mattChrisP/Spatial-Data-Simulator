import os
import psycopg2
import requests
import shutil
from psycopg2 import sql
from rtree import index

from constants import (
    GOOGLE_API_KEY, dbname, db_user, db_pass
)
from utils import SpatialData



def find_place(input, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype=textquery&fields=photos,formatted_address,name,geometry&key={api_key}"

    response = requests.get(url)
    json = response.json()

    if json['candidates']:
        if 'photos' in json['candidates'][0] and json['candidates'][0]['photos']:
            return json['candidates'][0]['photos'][0]['photo_reference']
        else:
            print('No photos found for this place.')
            return None
    else:
        print('No candidates found for this place.')
        return None


def get_photo(photo_reference, api_key, max_width=400, name="output"):
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={api_key}"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        try:
            if '/' in name:
                directory = '/'.join(name.split('/')[:-1])
                if not os.path.exists(directory):
                    os.makedirs(directory)
            with open(f'assets/{name}.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Image downloaded to {name}.jpg")
        except IOError as e:
            print(f"IO Error: Unable to save image: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    else:
        print("Unable to download image")

# Replace with your actual API Key
api_key = GOOGLE_API_KEY


instance = SpatialData(db_pass=db_pass,db_user=db_user,dbname=dbname)
names = instance.get_names()


for i in range(len(names)):
    place_name = names[i][0]
    photo_reference = find_place(place_name, api_key)
    if photo_reference:
        get_photo(photo_reference, api_key, name=place_name)
