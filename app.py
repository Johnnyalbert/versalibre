from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)

@app.route('/api/registrar', methods=['POST'])
def registrar():
    datos = request.get_json()
    nombre = datos['username']
    contrasena = datos['password']

    if Usuario.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    hash = generate_password_hash(contrasena)
    nuevo_usuario = Usuario(nombre=nombre, contrasena=hash)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado con éxito"})

@app.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    nombre = datos['username']
    contrasena = datos['password']

    usuario = Usuario.query.filter_by(nombre=nombre).first()
    if usuario and check_password_hash(usuario.contrasena, contrasena):
        return jsonify({"mensaje": "Inicio de sesión correcto"})
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@app.before_first_request
def crear_tablas():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
