from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from invokes import invoke_http

import json
import random
import pika
import amqp_setup

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verficationURL')


class Promo(db.Model):
    __tablename__ = 'promo'

    order_id = db.Column(db.Integer, primary_key=True)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    promo_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, nullable=False)
    promo_code = db.Column(db.String(256), nullable=False)

    def __init__(self, promo_code, order_id, account_id):
        self.promo_code = promo_code
        self.order_id = order_id
        self.account_id = account_id

    def json(self):
        return {"order_id": self.order_id, "is_express": self.is_express, "promo_created": self.promo_created, "account_id": self.account_id, "promo_code": self.promo_code}


with app.app_context():
  db.create_all()

def generate_promo_code():
    code = ''
    for i in range(6):
        code += ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 6)) + '-'
    code += ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 2))
    return code

@app.get("/promo")
def get_all():
    promoList = Promo.query.all()
    if len(promoList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "promos": [promo.json() for promo in promoList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no promo codes."
        }
    ), 404


@app.get("/promo/<int:promo_code>")
def get_by_id(promo_code):
    promo = Promo.query.filter_by(promo_code=promo_code).first()
    if promo:
        return jsonify(
            {
                "code": 200,
                "data": promo.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Promo not found."
        }
    ), 404


@app.post("/promo")
def create_promo():
    if request.json is None:
        raise Exception("No data received.")
    
    data = request.get_json()
    new_promo = Promo(**data)
    account_result = invoke_http(
        verification_URL + "account/" + str(new_promo.account_id), method='GET')

    if account_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if account_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": new_promo.account_id
                },
                "message": "Account does not exist."
            }
        ), 400

    new_promo.promo_code = generate_promo_code()
    
    try:
        db.session.add(new_promo)
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the promo code."
            }
        ), 500

    # notification_message = {"type": "redeem", "reward_name": reward_result["data"]["name"], "first_name": account_result["data"]
    #                         ["first_name"], "phone_number": account_result["data"]["phone"], "redemption_code": redemption.redemption_code}

    # message = json.dumps(notification_message)

    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
    #                                  body=message, properties=pika.BasicProperties(delivery_mode=2))


    return jsonify(
        {
            "code": 201,
            "data": new_promo.json()
        }
    ), 201


@app.delete("/promo/<int:promo_code>")
def delete_promo(promo_code):
    promo = Promo.query.filter_by(promo_code=promo_code).first()
    if promo:
        db.session.delete(promo)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "promo_code": promo.promo_code
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Promo not found."
        }
    ), 404

@app.put("/promo/<int:promo_code>")
def update_promo(promo_code):
    if request.json() is None:
        raise Exception("No data received.")
    updated_promo = Promo.query.get_or_404(promo_code=promo_code)
    data = request.get_json()

    updated_promo.promo_code = generate_promo_code()
    updated_promo.account_id = data["account_id"]

    db.session.commit()
    return "Promo updated.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6204, debug=True)