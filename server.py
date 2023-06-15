from flask import Flask, jsonify, request
from flask_cors import CORS
from t import (
    get_k_most_important_points_in_rect, get_k_nearest_points_to_location, preprocess, get_data
)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Hello, World!"

@app.route('/api/nearest/<k>/<x>/<y>', methods=['GET'])
def get_nearest(k,x,y):
    # Here you can connect to your database and get the data
    data = get_k_nearest_points_to_location(int(k),float(x),float(y))
    return jsonify(data)

@app.route('/api/points', methods=['GET'])
def get_points():
    # Here you can connect to your database and get the data
    data = get_data()
    return jsonify(data)


@app.route('/api/rect/<k>/<x1>/<y1>/<x2>/<y2>', methods=['GET'])
def get_rect(k,x1,y1,x2,y2):
    # Here you can connect to your database and get the data
    data = get_k_most_important_points_in_rect(int(k),float(x1),float(y1),float(x2),float(y2))
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()  # Get data posted as a json
    # Here you can parse and use your data
    print(data)
    return 'Success', 200  # return response to your client

if __name__ == "__main__":
    preprocess()
    app.run(debug=True)