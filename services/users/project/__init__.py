# services/users/project/__init__.py


import os  # new
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api

import sys


# instantiate the app
app = Flask(__name__)

print(app.config, file=sys.stderr)

api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings)      # new


class UsersPing(Resource):
    def get(self):
        return {
        'status': 'successc c',
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