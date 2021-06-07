from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Database/tienda.db'
app.config['SECRET_KEY'] = '123'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

db = SQLAlchemy(app)


class domiciliario(db.Model):
    id = db.Column("domiciliario_id", db.Integer, primary_key=True)
    domiciliario_nombre = db.Column(db.String(100))
    domiciliario_cedula = db.Column(db.Integer)
    domiciliario_direccion = db.Column(db.String(100))
    domiciliario_telefono = db.Column(db.Integer)
    domiciliario_email = db.Column(db.String(100))

    def __init__(self, datos):
        self.domiciliario_nombre = datos["nombre"]
        self.domiciliario_cedula = datos["cedula"]
        self.domiciliario_direccion = datos["direccion"]
        self.domiciliario_telefono = datos["telefono"]
        self.domiciliario_email = datos["email"]


@app.route("/")
@cross_origin()
def principal():
    data = domiciliario.query.all()
    diccionario_productos = {}
    for d in data:
        p = {
            "id": d.id,
            "nombre": d.domiciliario_nombre,
            "cedula": d.domiciliario_cedula,
            "direccion": d.domiciliario_direccion,
            "telefono": d.domiciliario_telefono,
            "email": d.domiciliario_email
        }
        diccionario_productos[d.id] = p
    return diccionario_productos


@app.route("/agregar/<nombre>/<int:cedula>/<direccion>/<int:telefono>/<email>")
@cross_origin()
def agregar(nombre, cedula, direccion, telefono, email):
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = domiciliario.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/actualizar/<int:id>/<nombre>/<int:cedula>/<direccion>/<int:telefono>/<email>")
@cross_origin()
def actualizar(id, nombre, cedula, direccion, telefono, email):
    p = domiciliario.query.filter_by(id=id).first()
    p.domiciliario_nombre = nombre
    p.domiciliario_cedula = cedula
    p.domiciliario_direccion = direccion
    p.domiciliario_telefono = telefono
    domiciliario_email = email
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = domiciliario.query.filter_by(id=id).first()
    p = {
        "nombre": d.domiciliario_nombre,
        "cedula": d.domiciliario_cedula,
        "direccion": d.domiciliario_direccion,
        "telefono": d.domiciliario_telefono,
        "email": d.domiciliario_email
    }
    return p


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
