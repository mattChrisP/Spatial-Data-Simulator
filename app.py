import os
import firebase_admin
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from utils import SpatialData
from werkzeug.utils import secure_filename


from firebase_admin import credentials
from firebase_admin import storage

from constants import url



app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"])

instance = SpatialData(url=url)

UPLOAD_DIRECTORY = "static/img"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    else:
        abort(400, description="File type not allowed")

    
    _, extension = os.path.splitext(filename)
    text = request.form.get('location_name', None)
    if text:
        new_filename = f"{text}{extension}"  # replace with your new file name
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        os.rename(file_path, new_file_path)
    
    # # Use a service account
    # cred = credentials.Certificate('path/to/serviceAccountKey.json')
    # firebase_admin.initialize_app(cred, {
    #     'storageBucket': '<your-storage-bucket>'
    # })

    # # Path to local file
    # local = "path/to/image.jpg"

    # # Cloud Storage file path
    # blob = storage.bucket().blob(local)

    # # Upload the local file to Cloud Storage
    # blob.upload_from_filename(local)

    # # The public URL can be used to directly access the uploaded file via HTTP.
    # public_url = blob.public_url
    # print(public_url)

    tags = request.form.get('tags', '')
    t_list = tags.split(",")
    long = request.form.get('longitude', '')
    lat = request.form.get('latitude', '')

    instance.insert_data(name=text,long=long,lat=lat,tags=t_list)
    return 'file uploaded successfully'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/nearest/<k>/<x>/<y>', methods=['GET'])
def get_nearest(k,x,y):
    # Here you can connect to your database and get the data
    data = instance.nearest_k(k=k,long=x,lat=y)
    return jsonify(data)


@app.route('/api/points', methods=['GET'])
def get_points():
    # Here you can connect to your database and get the data
    # data = get_data()
    # return jsonify(data)
    pass


@app.route('/api/rect/<k>/<x1>/<y1>/<x2>/<y2>', methods=['GET'])
def get_rect(k,x1,y1,x2,y2):
    # Here you can connect to your database and get the data
    # data = get_k_most_important_points_in_rect(int(k),float(x1),float(y1),float(x2),float(y2))
    # return jsonify(data)
    pass

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()  # Get data posted as a json
    # Here you can parse and use your data
    print(data)
    return 'Success', 200  # return response to your client

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)