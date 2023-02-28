from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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
    order_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, ForeignKey("account.account_id"), nullable = False, primary_key = True)

    def __init__(self, is_express, order_created, account_id):
        self.is_express = is_express
        self.order_created = order_created
        self.account_id = account_id

    def json(self):
        return {"order_id": self.order_id, "is_express": self.is_express, "order_created": self.order_created, "account_id": self.account_id}


@app.route("/order")
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
