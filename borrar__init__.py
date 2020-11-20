# services/mlapp/project/__init__.py
"""
import os  # new
from flask import Flask, send_file, jsonify
from flask import request, render_template
from flask_cors import CORS
#import json, pickle
import sklearn
from sklearn.tree import DecisionTreeClassifier 
from joblib import load

# instantiate the app
app = Flask(__name__)

# set config
#app_settings = os.getenv('APP_SETTINGS')  # new
#app.config.from_object(app_settings)      # new

# configuration
DEBUG = True
#FLASK_DEBUG=0

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

my_dir = os.path.dirname( __file__)
print(my_dir)
#classi = open('DTS.joblib', 'rb')
pickle_file_path = os.path.join(my_dir, 'DTS.joblib')
print("sklearn version:",sklearn.__version__)

@app.route('/api/predict', methods=['GET','POST'])
def api_predict():

    if request.method == 'POST':  #this block is only entered when the form is submitted
        #Load the saved model
        loaded_model = cargarModeloSiEsNecesario()

        req_data = request.get_json () 
        if not req_data:
            return jsonify(error="request body cannot be empty"), 400
        glucosa = req_data['glucosa']
        insulina = req_data['insulina']

        continuas = [[glucosa, insulina],] 
        #continuas = [[330, 1520],] 
        predictions = str(loaded_model.predict(continuas))
        return jsonify(prediction=predictions)

    return '''User postman u otro cliente para ejecutar esta API REST'''

@app.route('/predict', methods=['GET','POST'])
def predict():

    if request.method == 'POST':  #this block is only entered when the form is submitted
        #Load the saved model
        print("Cargar el modelo...")
        loaded_model = cargarModeloSiEsNecesario()

        print("Hacer Pronosticos")
        glucosa = request.form.get('glucosa')
        insulina = request.form['insulina']

       
        continuas = [[glucosa, insulina],] #330, 1520
        predictions = str(loaded_model.predict(continuas))
  

        return '''<h3>The glucosa value is:  {}</h3>
                  <h3>The insulina value is: {}</h3>
                  <h1>The predict value is: {}</h1>'''.format(glucosa, insulina, predictions)

    return '''<form method="POST">
                  glucosa: <input type="text" name="glucosa"><br>
                  insulina: <input type="text" name="insulina"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''



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


# puede eliminar desde esta línea en adelante
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'pong'})


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
"""