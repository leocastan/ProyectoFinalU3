# Libraries
from traceback import print_tb
from flask import Flask, jsonify, render_template, url_for, flash, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from bson import ObjectId
from bson.json_util import dumps


app = Flask(__name__, template_folder='templates')


# Conexion con la Base de datos
app.config['MONGO_DBNAME'] = 'Proyecto-U3'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Proyecto-U3'

mongo = PyMongo(app)


@app.route('/')
def administrador():
    if 'username' in session:
        return render_template('/regAdmin.html')
    return render_template('/selUser.html')

# ---------------------------------------
# Admin Access
# ---------------------------------------


@app.route('/logAdmin', methods=['POST'])
def logAdmin():
    users = mongo.db.Users
    login_user = users.find_one({'username': request.form['username']})
    login_pass = users.find_one({'password': request.form['pass']})
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


# Iniciar Sesion Administrador
@app.route('/logAdmin')
def logAd():
    return render_template('/logAdmin.html')

# ---------------------------------------
# Teacher Access
# ---------------------------------------


@app.route('/docente')
def docente():
    if 'username' in session:
        return render_template('/regAdmin.html')
    return render_template('/selUser.html')


@app.route('/logTeacher', methods=['POST'])
def logTeacher():
    users = mongo.db.Users
    login_user = users.find_one({'username': request.form['username']})
    login_pass = users.find_one({'password': request.form['pass']})
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


# Iniciar Sesion Docente
@app.route('/logTeacher')
def logDo():
    return render_template('/logTeacher.html')

# ---------------------------------------
# Student Access
# ---------------------------------------


@app.route('/logStudent', methods=['POST'])
def logStudent():
    users = mongo.db.Users
    login_user = users.find_one({'name': request.form['username']})
    login_pass = users.find_one({'password': request.form['pass']})
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

# Iniciar sesion Alumno


@app.route('/logStudent')
def logAl():
    return render_template('/logStudent.html')

# ---------------------------------------
# Register an Admin
# ---------------------------------------


@app.route('/regAdmin', methods=['POST', 'GET'])
def regAdmin():
    if request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            if 'submitButton' in request.form:
                users.insert_one({
                    'id_Institucional': request.form['id_Institucional'],
                    'cedula': request.form['cedula'],
                    'nombre': request.form['nombre'],
                    'apellido': request.form['apellido'],
                    'telefono': request.form['telefono'],
                    'direccion': request.form['direccion'],
                    'username': request.form['username'],
                    'password': request.form['pass'],
                    'userType': 'Administrador', })
                session['username'] = request.form['username']
            return redirect(url_for('docente'))
        return 'Ese usuario ya existe!'
    return render_template('/regAdmin.html')

# ---------------------------------------
# Register a Teacher
# ---------------------------------------


@app.route('/regTeacher', methods=['POST', 'GET'])
def regTeacher():
    if request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            if 'submitButton' in request.form:
                users.insert_one({
                    'id_Institucional': request.form['id_Institucional'],
                    'cedula': request.form['cedula'],
                    'nombre': request.form['nombre'],
                    'apellido': request.form['apellido'],
                    'telefono': request.form['telefono'],
                    'direccion': request.form['direccion'],
                    'titulo_Universitario': request.form['titulo_Universitario'],
                    'username': request.form['username'],
                    'password': request.form['pass'],
                    'userType': 'Docente', })
                session['username'] = request.form['username']
            return redirect(url_for('administrador'))
        return 'Ese usuario ya existe!'
    return render_template('/regTeacher.html')


@app.route('/docente')
def docenteReg():
    if 'username' in session:
        return render_template('/regTeacher.html')
    return render_template('/selUser.html')

# ---------------------------------------
# Register a Student
# ---------------------------------------


@app.route('/regStudent', methods=['POST', 'GET'])
def regStudent():
    if request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            if 'submitButton' in request.form:
                users.insert_one({
                     'id_Institucional': request.form['id_Institucional'],
                    'cedula': request.form['cedula'],
                    'nombre': request.form['nombre'],
                    'apellido': request.form['apellido'],
                    'telefono': request.form['telefono'],
                    'direccion': request.form['direccion'],
                    'paralelo': request.form['paralelo'],
                    'anio_lectivo': request.form['anio_lectivo'],
                    'username': request.form['username'],
                    'password': request.form['pass'],
                    'foto': request.form['foto'],
                    'userType': 'Estudiante', })
                session['username'] = request.form['username']
            return redirect(url_for('administrador'))
        return 'Ese usuario ya existe!'
    return render_template('/regStudent.html')


@app.route('/alumno')
def alumnoReg():
    if 'username' in session:
        return render_template('/regStudent.html')
    return render_template('/selUser.html')

# ---------------------------------------
# Cerrar Sesion
# ---------------------------------------


@app.route('/login')
def CerrarSession():
    session.pop('username', None)
    return render_template('/selUser.html')

# Ruta a app administrador


@app.route('/loginAdmin')
def logAdmin1():
    return render_template('/administrador.html')

# Ruta a app docente


@app.route('/RegisterUsers')
def logUser():
    return render_template('/RegistratUser.html')

# Ruta a app alumno


@app.route('/loginAlumno')
def logAlumno():
    return render_template('/IAlumnos.html')


# ---------------------------------------
# Main Method
# ---------------------------------------
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
