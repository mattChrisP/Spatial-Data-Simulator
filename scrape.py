import psycopg2
import requests
import json

from constants import (
    FLICKR_API_KEY, SECRET, dbname, db_user, db_pass
)

from utils import SpatialData


instance = SpatialData(dbname=dbname,db_user=db_user,db_pass=db_pass)


# This is for WIKIPEDIA COMMONS URL
def get_img(name):
    filename = f"{name}.jpg"

    # Define the endpoint
    url = 'https://commons.wikimedia.org/w/api.php'

    # Define the parameters for the API request
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'imageinfo',
        'titles': f'File:{filename}',
        'iiprop': 'url'
    }

    # Send the API request
    response = requests.get(url, params=params).json()

    # Get the imageinfo from the response
    imageinfo = list(response['query']['pages'].values())[0]['imageinfo']

    # Get the image URL
    image_url = imageinfo[0]['url']

    # Download the image
    image_data = requests.get(image_url).content

    img_binary = psycopg2.Binary(image_data)

    return img_binary


#This is for FLICKR API
def get_flickr_photos(api_key, tags):
    url = 'https://www.flickr.com/services/rest'
    payload = {
        'method': 'flickr.photos.search',
        'api_key': api_key,
        'tags': tags,
        'format': 'json',
        'nojsoncallback': 1,
    }
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200 and data.get('stat') == 'ok':
            for photo in data['photos']['photo']:
                return build_photo_url(photo)
    except requests.exceptions.RequestException as e:
        print(f"RequestException for {tags}: {e}")
    except json.JSONDecodeError:
        print(f"JSONDecodeError for {tags}, skipping this one.")
    return None


def build_photo_url(photo):
    return f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_m.jpg"


def scrape_overpass(k1,k2):
    global instance
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        area["ISO3166-1"="SG"]->.searchArea;
        (
            node["{k1}"="{k2}"](area.searchArea);
            way["{k1}"="{k2}"](area.searchArea);
            relation["{k1}"="{k2}"](area.searchArea);
        );
        out;
    """
    response = requests.get(overpass_url, 
                            params={'data': overpass_query})
    data = response.json()

    for element in data['elements']:
        if element['type'] == 'node':
            latitude = element['lat']
            longitude = element['lon']
            name = element['tags'].get('name', 'No Name Provided')
            if name == "No Name Provided":
                continue

            img_url = get_flickr_photos(FLICKR_API_KEY, name)
            if img_url:
                instance.insert_data(name=name, lat=latitude, long=longitude, url=img_url)
                print(f'Name: {name}, Latitude: {latitude}, Longitude: {longitude}')


prompt = [
    # ("amenity", "bar"),
    # ("amenity", "bbq"),
    # ("amenity", "cafe"),
    # ("amenity", "fast_food"),
    # ("amenity", "food_court"),
    # ("amenity", "ice_cream"),
    # ("amenity", "pub"),
    # ("amenity", "restaurant"),
    # ("amenity", "place_of_worship"),
    ("historic", "memorial"),
    ("historic", "monument"),
    ("historic", "statue"),
    ("historic", "archaeological_site"),
    ("historic", "ruins"),
    ("historic", "castle"),
    ("historic", "fort"),
    ("historic", "battlefield"),
    ("historic", "cannon"),
    ("historic", "milestone"),
    ("historic", "tomb"),
    ("historic", "tower"),
    ("historic", "wayside_cross"),
    ("historic", "wayside_shrine"),
    ("historic", "wreck"),
    ("historic", "citywalls"),
    ("historic", "manor"),
    ("historic", "stone"),
    ("tourism", "attraction"),
    ("tourism", "hotel"),
    ("tourism", "motel"),
    ("tourism", "hostel"),
    ("tourism", "guest_house"),
    ("tourism", "information"),
    ("tourism", "museum"),
    ("tourism", "zoo"),
    ("tourism", "camp_site"),
    ("tourism", "caravan_site"),
    ("tourism", "picnic_site"),
    ("tourism", "viewpoint"),
    ("tourism", "theme_park"),
    ("tourism", "artwork"),
    ("leisure", "park"),
    ("leisure", "swimming_pool"),
    ("leisure", "stadium"),
    ("leisure", "sports_centre"),
    ("leisure", "pitch"),
    ("leisure", "playground"),
    ("leisure", "golf_course"),
    ("leisure", "water_park"),
    ("leisure", "marina"),
    ("leisure", "slipway"),
    ("leisure", "fishing"),
    ("leisure", "nature_reserve"),
    ("leisure", "park"),
    ("leisure", "garden"),
    ("leisure", "recreation_ground"),
    ("leisure", "common"),
    ("leisure", "grass"),
    ("leisure", "beach_resort")
]

for keys in prompt:
    k1, k2 = keys[0], keys[1]
    scrape_overpass(k1,k2)
