#Libraries
from traceback import print_tb
from flask import Flask,jsonify, render_template, url_for, flash, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from bson import ObjectId
from bson.json_util import dumps


app = Flask(__name__, template_folder='templates')


#Conexion con la Base de datos
app.config['MONGO_DBNAME'] = 'Proyecto-U3'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Proyecto-U3'

mongo = PyMongo(app)


@app.route('/')
def administrador():
    if 'username' in session:
        return render_template('/regUser.html')
    return render_template('/selUser.html')

#---------------------------------------
#Acceso para Administrador
#---------------------------------------

@app.route('/logAdmin', methods=['POST'])
def logAdmin():
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
                flash("ACCESO DENEGADO")
                return render_template('logAdmin.html')
        else:
            flash("CONTRASEÑA INCORRECTA")
            return render_template('logAdmin.html')
    else:
        flash("USUARIO NO ENCONTRADO")
        return render_template('logAdmin.html')
  

#Iniciar Sesion Administrador
@app.route('/logAdmin')
def logAd():
    return render_template('/logAdmin.html')

#---------------------------------------
#Acceso para Docente
#---------------------------------------

@app.route('/docente')
def docente():
    if 'username' in session:
        return redirect(url_for('verAlumnos'))
    return render_template('/selUser.html')
    
@app.route('/logTeacher', methods=['POST'])
def logTeacher():
    users = mongo.db.Users
    login_user = users.find_one({'name' : request.form['username']})
    login_pass = users.find_one({'password' : request.form['pass']}) 
    log_claseA = "A" 
    log_claseB = "B" 
    login_doc = "Docente" 

    if login_user != None:
        if login_pass:
            if login_doc == request.form['Tusuario']:
                if log_claseA == request.form['clase']:
                    session['username'] = request.form['username']
                    return redirect(url_for('verAlumnosA'))
                elif log_claseB == request.form['clase']:
                        session['username'] = request.form['username']
                        return redirect(url_for('verAlumnosB'))
        else:
            flash("CONTRASEÑA INCORRECTA")
            return render_template('logTeacher.html')
    else:
        flash("USUARIO NO ENCONTRADO")
        return render_template('logTeacher.html')
        

#Iniciar Sesion Docente
@app.route('/logTeacher')
def logDo():
    return render_template('/logTeacher.html')

#---------------------------------------
#Acceso para Estudiante
#---------------------------------------

@app.route('/logStudent', methods=['POST'])
def logStudent():
    users = mongo.db.Users
    login_user = users.find_one({'name' : request.form['username']})
    login_pass = users.find_one({'password' : request.form['pass']}) 
    login_alum = "Alumno" 

    if login_user != None:
        if login_pass:
            if login_alum == request.form['Tusuario']:
                session['username'] = request.form['username']
                return redirect(url_for('OpcionesJuegos'))
            else:
                flash("ACCESO DENEGADO")
                return render_template('logStudent.html')
        else:
            flash("CONTRASEÑA INCORRECTA")
            return render_template('logStudent.html')
    else:
        flash("USUARIO NO ENCONTRADO")
        return render_template('logStudent.html')
        
#Iniciar sesion Alumno
@app.route('/logStudent')
def logAl():
    return render_template('/logStudent.html')




#Main de la aplicacion
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

