import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from utils import SpatialData
from werkzeug.utils import secure_filename

from constants import (
    dbname, db_user, db_pass
)


app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"])

instance = SpatialData(dbname=dbname, db_user=db_user, db_pass=db_pass)

UPLOAD_DIRECTORY = "birds"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
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
    text = request.form.get('text', None)
    if text:
        new_filename = f"{text}{extension}"  # replace with your new file name
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        os.rename(file_path, new_file_path)
    variable = request.form.get('variable', '')

    print('Text:', text)
    print('Variable:', variable)
    
    return 'file uploaded successfully'


@app.route('/')
def home():
    return "Hello, World!"

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
    app.run(debug=True)