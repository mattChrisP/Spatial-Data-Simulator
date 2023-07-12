import os
import base64
import json
from flask import Flask, jsonify, request, abort, render_template

from utils import SpatialData
from werkzeug.utils import secure_filename

from firebase_admin import initialize_app, storage, credentials
from constants import url, ENCODED_JSON



app = Flask(__name__)

instance = SpatialData(url=url)

encoded_cred = ENCODED_JSON

# Decode base64 string back to JSON string
json_credentials = base64.b64decode(encoded_cred).decode('utf-8')


# Convert JSON string to Python dictionary
dict_credentials = json.loads(json_credentials)

# Initialize Firestore DB
cred = credentials.Certificate(dict_credentials)
default_app = initialize_app(cred, {
    'storageBucket': 'spatial-data-f99f2.appspot.com', # replace with your Firebase Storage bucket
})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    global instance
    print(request.form, "this is form")
    if 'img' not in request.files:
        abort(400, description="No file part")
    file = request.files['img']

    if file.filename == '':
        abort(400, description="No selected file")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        _, extension = os.path.splitext(filename)
        text = request.form.get('location_name', None)

        # Get a reference to the storage service
        bucket = storage.bucket()

        # Create a new blob and upload the file's content.
        new_filename = f"{text}{extension}" if text else filename
        blob = bucket.blob(new_filename)
        blob.upload_from_string(file.read())

        # Make the blob publicly viewable.
        blob.make_public()

        file_url = blob.public_url
    else:
        abort(400, description="File type not allowed")


    tags = request.form.get('tags', '')
    t_list = [tags]
    long = request.form.get('longitude', '')
    lat = request.form.get('latitude', '')
    print(tags, "this is tags")

    instance.insert_data(name=text,long=long,lat=lat,tags=t_list,url=file_url)
    return 'file uploaded successfully'


@app.route('/')
def home():
    base_url = request.host_url
    return render_template('index.html', base_url = base_url)

@app.route('/api/nearest/<k>/<x>/<y>', methods=['GET'])
def get_nearest(k,x,y):
    # Here you can connect to your database and get the data
    data = instance.nearest_k(k=k,long=x,lat=y)
    return jsonify(data)




if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True)