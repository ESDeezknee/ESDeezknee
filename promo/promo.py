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
    is_used = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, account_id, queue_id, promo_code, is_used):
        self.account_id = account_id
        self.queue_id = queue_id
        self.promo_code = promo_code
        self.is_used = is_used


    def json(self):
        return {"account_id": self.account_id, "queue_id": self.queue_id, "promo_code": self.promo_code, "is_used": self.is_used}


with app.app_context():
  db.create_all()
  existing_promo_1 = db.session.query(Promo).filter(Promo.queue_id==1).first()
  if not existing_promo_1:
      new_promo_1 = Promo(queue_id=1, account_id=1, promo_code="123456", is_used=0)
      new_promo_2 = Promo(queue_id=2, account_id=2, promo_code="123456", is_used=0)
      new_promo_3 = Promo(queue_id=3, account_id=3, promo_code="123456", is_used=0)
      new_promo_4 = Promo(queue_id=4, account_id=4, promo_code="123456", is_used=0)
      db.session.add(new_promo_1)
      db.session.add(new_promo_2)
      db.session.add(new_promo_3)
      db.session.add(new_promo_4)
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
def delete_promo(account_id):
    promo = Promo.query.filter_by(account_id=account_id).first()
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

@app.patch("/promo/<int:account_id>")
def used_promo(account_id):
    if (not Promo.query.filter_by(account_id=account_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "account_id": account_id
                },
                "message": "Promo not found."
            }
        ), 404
    
    data = request.get_json()
    # frontend need to pass
    # {
    #   "is_used": 1
    #   "promo_code": "123456"
    # }
    updated_promo = Promo.query.filter_by(account_id=account_id).first()

    if updated_promo.is_used == 0:
        payment_json = {
            "account_id": updated_promo.account_id,
            "queue_id": updated_promo.queue_id,
            "promo_code": updated_promo.promo_code,
            "payment_method": "promo"
        }
        create_ticket = invoke_http(
            order_URL + str(updated_promo.account_id) + "/paying", method='POST', json=payment_json)

        if create_ticket["code"] in range(500, 600):
            return jsonify(
                {
                    "code": 500,
                    "message": "Oops, something went wrong! promo_invalid",
                }
            ), 500
        
        try:
            updated_promo.is_used = data["is_used"]
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating promo db.",
                    "invoking": updated_promo
                }
            ), 500

        create_ticket = invoke_http(
            order_URL + str(updated_promo.account_id) + "/paying", method='POST', json=payment_json)

        if create_ticket["code"] in range(500, 600):
            return jsonify(
                {
                    "code": 500,
                    "message": "Oops, something went wrong! Order",
                }
            ), 500 
        
        account_result = invoke_http(
            verification_URL + "account/" + str(updated_promo.account_id), method='GET')

        notification_message = {
            "type": "promo",
            "account_id": updated_promo.account_id,
            "first_name": account_result["data"]["first_name"],
            "phone_number": account_result["data"]["phone"],
            "promo_code": updated_promo.promo_code,
            "message": "You have successfully redeemed a promo."
        }
        message = json.dumps(notification_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify(
            {
                "code": 200,
                "data": updated_promo.json(),
                "message": "Promo has been updated (used)."
            }
        ), 200

    else:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": account_id,
                    "asdf": updated_promo.json()
                },
                "message": "Promo has already been used."
            }
        ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6204, debug=True)