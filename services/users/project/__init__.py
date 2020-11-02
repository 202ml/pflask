# services/users/project/__init__.py

import uuid

from flask_cors import CORS

import os  # new
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask import Blueprint, request, render_template

import sys
import sklearn
from joblib import load
from sklearn.tree import DecisionTreeClassifier 
import pandas as pd



# instantiate the app
app = Flask(__name__)

#print(app.config, file=sys.stderr)

api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings)      # new

# configuration
DEBUG = True
FLASK_DEBUG=0

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

my_dir = os.path.dirname( __file__)
print(my_dir)
#classi = open('DTS.joblib', 'rb')
pickle_file_path = os.path.join(my_dir, 'DTS.joblib')
print(pickle_file_path)

print( sklearn.__version__)

#DTSf = load(pickle_file_path) 

@app.route('/predict', methods=['GET'])
def predict():
    """API request
    """
    #Load the saved model
    print("Cargar el modelo...")
    loaded_model = cargarModeloSiEsNecesario()

    print("Hacer Pronosticos")
    continuas = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],]
    predictions = str(loaded_model.predict(continuas))
    return jsonify(predictions)

global_model = None

def cargarModeloSiEsNecesario():
    global global_model
    if global_model is not None:
        print('Modelo YA cargado')
        return global_model
    else:
        global_model = load(pickle_file_path) 
        print('Modelo Cargado')
        return global_model


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)








class UsersPing(Resource):
    def get(self):
        return {
        'status': 'success okokoko',
        'message': 'pong!'
    }


api.add_resource(UsersPing, '/users/ping')

@app.route("/hello")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.7 ooo "

#we define the route /
@app.route('/api1')
def welcome():
    # return a json
    return jsonify({'status': 'api ok'})

@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, "index.html")
    return send_file(index_path)

# Everything not declared before (not a Flask route / API endpoint)...
@app.route("/<path:path>")
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)

@app.route('/users/<string:nombre>')
def hello_world(nombre=None):

    return ("Hola {}!".format(nombre))
    