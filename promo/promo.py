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

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
order_URL = environ.get('orderURL') or "http://localhost:6201/order/"

class Promo(db.Model):
    __tablename__ = 'promos'
    account_id = db.Column(db.Integer, primary_key=True, nullable=False)
    queue_id = db.Column(db.Integer, nullable=False)
    promo_code = db.Column(db.String(256), nullable=False)

    def __init__(self, account_id, queue_id, promo_code):
        self.account_id = account_id
        self.queue_id = queue_id
        self.promo_code = promo_code


    def json(self):
        return {"account_id": self.account_id, "queue_id": self.queue_id, "promo_code": self.promo_code}


with app.app_context():
  db.create_all()
  existing_promo_1 = db.session.query(Promo).filter(Promo.queue_id==1).first()
  if not existing_promo_1:
      new_promo_1 = Promo(queue_id=1, account_id=1, promo_code="123456")
      new_promo_2 = Promo(queue_id=2, account_id=2, promo_code="123456")
      new_promo_3 = Promo(queue_id=3, account_id=3, promo_code="123456")
      new_promo_4 = Promo(queue_id=4, account_id=4, promo_code="123456")
      db.session.add(new_promo_1)
      db.session.add(new_promo_2)
      db.session.commit()

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


@app.get("/promo/<int:account_id>")
def get_by_id(account_id):
    promo = Promo.query.filter_by(account_id=account_id).first()
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
                "message": "Oops, something went wrong! Account",
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
    
    # queue_result = invoke_http(
    #     verification_URL + "queueticket/" + str(new_promo.queue_id), method='GET')

    # if queue_result["code"] in range(500, 600):
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "message": "Oops, something went wrong! Queue",
    #         }
    #     ), 500

    # if queue_result["code"] in range(300, 500):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "queue_id": new_promo.queue_id
    #             },
    #             "message": "queueticket does not exist."
    #         }
    #     ), 400


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


    return jsonify(
        {
            "code": 201,
            "data": new_promo.json()
        }
    ), 201


@app.delete("/promo/<int:account_id>")
def redeem_promo(account_id):
    promo = Promo.query.filter_by(account_id=account_id).first()
    if promo:

        payment_json = {
            "account_id": promo.account_id,
            "queue_id": promo.queue_id,
            "promo_code": promo.promo_code,
            "payment_method": "promo"
        }

        redeem_promo = invoke_http(
            order_URL + str(promo.account_id) + "/paid", method='PATCH', json=payment_json)

        if redeem_promo["code"] in range(500, 600):
            return jsonify(
                {
                    "code": 500,
                    "message": "Oops, something went wrong! Order",
                }
            ), 500 
    
        db.session.delete(promo)
        db.session.commit()

        account_result = invoke_http(
            verification_URL + "account/" + str(promo.account_id), method='GET')

        notification_message = {
            "type": "promo",
            "account_id": promo.account_id,
            "phone_number": account_result["data"]["phone"],
            "promo_code": promo.promo_code,
            "message": "You have successfully redeemed a promo."
        }
        message = json.dumps(notification_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))


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

@app.put("/promo/<int:account_id>")
def update_promo(account_id):
    if request.json() is None:
        raise Exception("No data received.")
    updated_promo = Promo.query.get_or_404(account_id=account_id)
    data = request.get_json()
    updated_promo.account_id = data["account_id"]
    updated_promo.queue_id = data["queue_id"]
    db.session.commit()
    return "Promo updated.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6204, debug=True)