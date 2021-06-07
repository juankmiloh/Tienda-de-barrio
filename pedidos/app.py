from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Database/tienda.db'
app.config['SECRET_KEY'] = '123'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

db = SQLAlchemy(app)


class pedidos(db.Model):
    consecutivo = db.Column("consecutivo", db.Integer, primary_key=True)
    pedido_id_pedido = db.Column(db.Integer)
    pedido_id_domiciliario = db.Column(db.Integer)
    pedido_id_cliente =  db.Column(db.Integer)
    pedido_id_producto = db.Column(db.Integer)
    pedido_cantidad = db.Column(db.Integer)

    def __init__(self, datos):
        self.pedido_id_pedido = datos["id_pedido"]
        self.pedido_id_domiciliario = datos["id_domiciliario"]
        self.pedido_id_cliente = datos["id_cliente"]
        self.pedido_id_producto = datos["id_producto"]
        self.pedido_cantidad = datos["cantidad"]

@app.route("/")
@cross_origin()
def principal():
    data = pedidos.query.all()
    diccionario_pedidos = {}
    for d in data:
        p = {
            "id_pedido": d.pedido_id_pedido,
            "id_domiciliario": d.pedido_id_domiciliario,
            "id_cliente": d.pedido_id_cliente,
            "id_producto": d.pedido_id_producto,
            "cantidad": d.pedido_cantidad
        }
        diccionario_pedidos[d.consecutivo] = p
    return diccionario_pedidos

# http://127.0.0.1:5000/agregar/pedro/123456/avenida_siempre_viva/3118683006/juan@hotmail.com
@app.route("/agregar/<int:pedido>/<int:domiciliario>/<int:cliente>/<int:producto>/<int:cantidad>")
@cross_origin()
def agregar(pedido,cliente, producto, domiciliario,cantidad):
    datos = {
        "id_pedido": pedido,
        "id_domiciliario": domiciliario,
        "id_cliente": cliente,
        "id_producto": producto,
        "cantidad": cantidad,
    }
    p = pedidos(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

# http://127.0.0.1:5000/eliminar/1
@app.route("/eliminar/<int:pedido>")
@cross_origin()
def eliminar(pedido):
    p = pedidos.query.filter_by(pedido_id_pedido=pedido).all()
    for d in p:
        db.session.delete(d)
    db.session.commit()
    return redirect(url_for('principal'))


@app.route("/actualizar/<int:consecutivo>/<int:domiciliario>/<int:cliente>/<int:producto>/<int:cantidad>")
@cross_origin()
def actualizar(consecutivo,cliente, producto, domiciliario,cantidad):
    p = pedidos.query.filter_by(consecutivo=consecutivo).first()
    p.pedido_id_domiciliario = domiciliario
    p.pedido_id_cliente = cliente
    p.pedido_id_producto = producto
    p.pedido_cantidad = cantidad
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:pedido>")
@cross_origin()
def buscar(pedido):
    ped = pedidos.query.filter_by(pedido_id_pedido=pedido).all()
    diccionario_pedidos = {}
    for d in ped:
        p = {
            "id_pedido": d.pedido_id_pedido,
            "id_domiciliario": d.pedido_id_domiciliario,
            "id_cliente": d.pedido_id_cliente,
            "id_producto": d.pedido_id_producto,
            "cantidad": d.pedido_cantidad,
        }
        diccionario_pedidos[d.consecutivo] = p
    return diccionario_pedidos


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
