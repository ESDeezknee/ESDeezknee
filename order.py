from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import relationship

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    order_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, nullable=False)
    # tentative do not use FK

    def __init__(self, is_express, order_created, account_id):
        self.is_express = is_express
        self.order_created = order_created
        self.account_id = account_id

    def json(self):
        return {"order_id": self.order_id, "is_express": self.is_express, "order_created": self.order_created, "account_id": self.account_id}


with app.app_context():
    db.init_app(app)
    db.create_all()


@app.get("/order")
def get_all():
    orderList = Order.query.all()
    if len(orderList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404


@app.get("/order/<int:order_id>")
def get_by_id(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Order not found."
        }
    ), 404


@app.post("/order")
def create_order():
    if request.json is None:
        raise Exception("No data received.")
    try:
        data = request.get_json()
        new_order = Order(**data)
        db.session.add(new_order)
        db.session.commit()
        db.session.refresh(new_order)
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": new_order.order_id
                },
                "message": "An error occurred creating the order."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_order.json()
        }
    ), 201


@app.delete("/order/<int:order_id>")
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "order_id": order.order_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Order not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=6201, debug=True)
