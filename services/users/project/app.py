#from flask import Flask, render_template, request, redirect
import os  # new
from flask import Flask, send_file, jsonify, redirect
from flask import request, render_template
from flask_cors import CORS
import sklearn
from sklearn.tree import DecisionTreeClassifier 
from joblib import load

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

my_dir = os.path.dirname( __file__)
pickle_file_path = os.path.join(my_dir, 'DTS.joblib')

@app.route('/api/predict', methods=['GET','POST'])
def api_predict():
    """API request
    """
    if request.method == 'POST':  #this block is only entered when the form is submitted
        #Load the saved model
        loaded_model = cargarModeloSiEsNecesario()

        req_data = request.get_json () 
        if not req_data:
            return jsonify(error="request body cannot be empty"), 400
        glucosa = req_data['glucosa']
        insulina = req_data['insulina']
        r_invmap = {1: 'normal', 2: 'pre-diabetes', 3: 'diabetes'}

        features = {
            'glucosa': glucosa,
            'insulina': insulina
        }

        continuas = [[glucosa, insulina],] 
        #continuas = [[330, 1520],] 
        predictions = loaded_model.predict(continuas)
        prediction = r_invmap[predictions[0]] 

        return jsonify( features=features,predictions=prediction)

    return '''User postman u otro cliente para ejecutar esta API REST'''

@app.route('/', methods=['GET','POST'])
def predict():
    """
    """
    if request.method == 'POST':  #this block is only entered when the form is submitted
        #Load the saved model
        print("Cargar el modelo...")
        loaded_model = cargarModeloSiEsNecesario()

        print("Hacer Pronosticos")
        glucosa = request.form.get('glucosa')
        insulina = request.form['insulina']
        #r_map = {'normal': 1, 'pre-diabetes': 2, 'diabetes': 3}
        r_invmap = {1: 'normal', 2: 'pre-diabetes', 3: 'diabetes'}

        features = {
            'glucosa': glucosa,
            'insulina': insulina
        }
        continuas = [[glucosa, insulina],]

        predictions = loaded_model.predict(continuas)
        prediction = r_invmap[predictions[0]] 

        #return '''<h3>The glucosa value is:  {}</h3>
        #          <h3>The insulina value is: {}</h3>
        #          <h1>The predict value is: {}</h1>'''.format(glucosa, insulina, predictions)
        return render_template("index.html", features=features, predictions=prediction)

    #return '''<form method="POST">
    #              glucosa: <input type="text" name="glucosa"><br>
    #              insulina: <input type="text" name="insulina"><br>
    #              <input type="submit" value="Submit"><br>
    #          </form>'''
    return render_template("index.html")


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

@app.route("/h")
def hello():
    return render_template("index.html")

@app.route('/<name>')
def hello_name(name):
    return "Hello {} {}!".format(name, sklearn.__version__)

if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
