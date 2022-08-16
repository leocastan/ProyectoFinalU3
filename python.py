#Libraries
from traceback import print_tb
from flask import Flask,jsonify, render_template, url_for, flash, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from bson import ObjectId
from bson.json_util import dumps

app = Flask(__name__, template_folder='templates')

#Conexion con la Base de datoss
app.config['MONGO_DBNAME'] = 'Proyecto-U3'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Proyecto-U3'

mongo = PyMongo(app)

@app.route('/')
def administrador():
    if 'username' in session:
        return render_template('/regUser.html')
    return render_template('/selUser.html')

###################################################
@app.route('/loginAd', methods=['POST'])
def loginAd():
    users = mongo.db.Users
    login_user = users.find_one({'name' : request.form['username']})
    login_pass = users.find_one({'password' : request.form['pass']}) 
    login_admin = "Administrador" 

    if login_user != None:
        if login_pass:
            if login_admin == request.form['Tusuario']:
                session['username'] = request.form['username']
                return redirect(url_for('administrador'))
            else:
                flash("Acceso Denegado")
                return render_template('logAdmin.html')
        else:
            flash("Contaseña Incorrecta")
            return render_template('logAdmin.html')
    else:
        flash("Usuario No encontrado")
        return render_template('logAdmin.html')
  

#Iniciar Sesion Administrador
@app.route('/logAdmin')
def logAd():
    return render_template('/logAdmin.html')

#iniciamos la aplicacion
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

