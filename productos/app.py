from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SECRET_KEY'] = '123'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

db = SQLAlchemy(app)


class producto(db.Model):
    id = db.Column("product_id", db.Integer, primary_key=True)
    producto_nombre = db.Column(db.String(100))
    producto_valor = db.Column(db.Integer)
    producto_cantidad = db.Column(db.Integer)

    def __init__(self, datos):
        self.producto_nombre = datos["nombre"]
        self.producto_cantidad = datos["cantidad"]
        self.producto_valor = datos["valor"]


@app.route("/")
@cross_origin()
def principal():
    data = producto.query.all()
    diccionario_productos = {}
    for d in data:
        p = {
            "id": d.id,
            "nombre": d.producto_nombre,
            "cantidad": d.producto_cantidad,
            "valor": d.producto_valor
        }
        diccionario_productos[d.id] = p
    return diccionario_productos

# http://127.0.0.1:5000/agregar/borrador/10/1800
@app.route("/agregar/<nombre>/<int:cantidad>/<int:valor>")
@cross_origin()
def agregar(nombre, cantidad, valor):
    datos = {
        "nombre": nombre,
        "cantidad": cantidad,
        "valor": valor
    }
    p = producto(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

# http://127.0.0.1:5000/eliminar/1
@app.route("/eliminar/<int:id>")
@cross_origin()
def eliminar(id):
    p = producto.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/actualizar/<int:id>/<nombre>/<int:cantidad>/<int:valor>")
@cross_origin()
def actualizar(id, nombre, cantidad, valor):
    p = producto.query.filter_by(id=id).first()
    p.producto_nombre = nombre
    p.producto_cantidad = cantidad
    p.producto_valor = valor
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/buscar/<int:id>")
@cross_origin()
def buscar(id):
    d = producto.query.filter_by(id=id).first()
    p = {
        "id": d.id,
        "nombre": d.producto_nombre,
        "cantidad": d.producto_cantidad,
        "valor": d.producto_valor
    }
    return p


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
