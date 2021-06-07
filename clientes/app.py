from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Database/tienda.db'
app.config['SECRET_KEY'] = '123'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

db = SQLAlchemy(app)


class Cliente(db.Model):
    id = db.Column("cliente_id", db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100))
    cliente_nit = db.Column(db.Integer)
    cliente_direccion = db.Column(db.String(100))
    cliente_telefono = db.Column(db.Integer)
    cliente_email = db.Column(db.String(100))

    def __init__(self, datos):
        self.cliente_nombre = datos["nombre"]
        self.cliente_nit = datos["nit"]
        self.cliente_direccion = datos["direccion"]
        self.cliente_telefono = datos["telefono"]
        self.cliente_email = datos["email"]


@app.route("/")
@cross_origin()
def principal():
    data = Cliente.query.all()
    diccionario_productos = {}
    for d in data:
        p = {
            "id": d.id,
            "nombre": d.cliente_nombre,
            "nit": d.cliente_nit,
            "direccion": d.cliente_direccion,
            "telefono": d.cliente_telefono,
            "email": d.cliente_email
        }
        diccionario_productos[d.id] = p
    return diccionario_productos

# http://127.0.0.1:5000/agregar/juan/123456/avenida_siempre_viva/3118683006/juan@hotmail.com
@app.route("/agregar/<nombre>/<int:nit>/<direccion>/<telefono>/<email>")
@cross_origin()
def agregar(nombre, nit, direccion, telefono, email):
    datos = {
        "nombre": nombre,
        "nit": nit,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }
    p = Cliente(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

# http://127.0.0.1:5000/eliminar/1
@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = Cliente.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

# http://127.0.0.1:5000/actualizar/2/camilo/123456/avenida_siempre_viva/3118683006/juan@hotmail.com
@app.route("/actualizar/<int:id>/<nombre>/<int:nit>/<direccion>/<telefono>/<email>")
@cross_origin()
def actualizar(id, nombre, nit, direccion, telefono, email):
    p = Cliente.query.filter_by(id=id).first()
    p.cliente_nombre = nombre
    p.cliente_nit = nit
    p.cliente_direccion = direccion
    p.cliente_telefono = telefono
    p.cliente_email = email
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = Cliente.query.filter_by(id=id).first()
    p = {
        "id": d.id,
        "nombre": d.cliente_nombre,
        "nit": d.cliente_nit,
        "direccion": d.cliente_direccion,
        "telefono": d.cliente_telefono,
        "email": d.cliente_email
    }
    return p


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
