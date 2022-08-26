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
    login_user = users.find_one({'username': request.form['username']})
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
                    'userType': request.form['tipo_usuario'],
                    'titulo_Universitario': request.form['titulo_Universitario'],
                    'foto': request.form['foto'],
                    'paralelo': request.form['paralelo'],
                    'anio_lectivo': request.form['anio_lectivo'],
                })
                session['username'] = request.form['username']
            return redirect(url_for('docente'))
        return 'Ese usuario ya existe!'
    return render_template('/regAdmin.html')

# ---------------------------------------
# Register a Course
# ---------------------------------------


@app.route('/regTeacher', methods=['POST', 'GET'])
def regTeacher():
    if request.method == 'POST':
        users = mongo.db.Paralelo
        existing_paralelo = users.find_one({'paralelo': request.form['paralelo']})
        if existing_paralelo is None:
            if 'submitButton' in request.form:
                users.insert_one({
                    'paralelo': request.form['paralelo'],
                    'docente': request.form['docente'],
                    'anio_lectivo': request.form['anio_lectivo'], })
                session['paralelo'] = request.form['paralelo']
            return redirect(url_for('docenteReg'))
        return 'Ese paralelo ya existe!'
    return render_template('/regTeacher.html')


@app.route('/docente')
def docenteReg():
    if 'username' in session:
        return render_template('/regTeacher.html')
    return render_template('/selUser.html')

# ---------------------------------------
# Register a Year
# ---------------------------------------


@app.route('/regStudent', methods=['POST', 'GET'])
def regStudent():
    if request.method == 'POST':
        users = mongo.db.Anio_lectivo
        existing_user = users.find_one({'anio_lectivo': request.form['anio_lectivo']})
        if existing_user is None:
            if 'submitButton' in request.form:
                users.insert_one({
                    'anio_lectivo': request.form['anio_lectivo'],
                    'fecha_inicia': request.form['fecha_inicia'],
                    'fecha_termina': request.form['fecha_termina'], })
                session['anio_lectivo'] = request.form['anio_lectivo']
            return redirect(url_for('estudianteReg'))
        return 'Ese año lectivo ya existe!'
    return render_template('/regStudent.html')


@app.route('/estudiante')
def estudianteReg():
    if 'username' in session:
        return render_template('/regStudent.html')
    return render_template('/selUser.html')

# ---------------------------------------
# Register a Matricula
# ---------------------------------------


@app.route('/regMatricula', methods=['POST', 'GET'])
def regMatricula():
    if request.method == 'POST':
        users = mongo.db.Matricula
        existing_user = users.find_one({'estudiante': request.form['estudiante']})
        if existing_user is None:
            if 'submitButton' in request.form:
                users.insert_one({
                    'estudiante': request.form['estudiante'],
                    'paralelo': request.form['paralelo'],
                    'asignatura': request.form['asignatura'], })
                session['estudiante'] = request.form['estudiante']
            return redirect(url_for('matriculaReg'))
        return 'EL estudiante ya esta registrado en esa asignatura!'
    return render_template('/regMatricula.html')


@app.route('/estudiante')
def matriculaReg():
    if 'username' in session:
        return render_template('/regMatricula.html')
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

#Ver Alumnos
@app.route('/verAlumnosA')
def verAlumnosA():    
    Alumn_list = mongo.db.Users.find({'paralelo' : "A"})
    return render_template("paraleloA.html", Alumn_list = Alumn_list)

#Ver Alumnos
@app.route('/verAlumnosB')
def verAlumnosB():
    Alumn_list = mongo.db.Users.find({'paralelo' : "B"})
    return render_template("paraleloB.html", Alumn_list = Alumn_list)

#Iniciar juego
@app.route('/iniciarJuego')
def iniciarJuego():
    return render_template("adivina.html")

@app.route('/regAdmin')
def mostrarUsers():
    personas = mongo.db.Users
    personasReceived = personas.find()
    return render_template('regAdmin.html', personas = personasReceived)

# ---------------------------------------
# Main Method
# ---------------------------------------
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
