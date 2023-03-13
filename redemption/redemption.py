from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime, timedelta

from invokes import invoke_http

import random
import amqp_setup
import pika
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verificationURL')
loyalty_URL = environ.get('loyaltyURL')


class Redemption(db.Model):
    __tablename__ = 'redemptions'

    redemption_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    reward_id = db.Column(db.Integer, nullable=False)
    redemption_code = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(64), nullable=False, default="Not Claimed")
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def __init__(self, account_id, reward_id):
        self.account_id = account_id
        self.reward_id = reward_id

    def json(self):
        return {"redemption_id": self.redemption_id, "account_id": self.account_id, "reward_id": self.reward_id, "redemption_code": self.redemption_code, "status": self.status, "created": self.created, "modified": self.modified}


with app.app_context():
    db.create_all()


def generate_redemption_code():
    code = ''
    for i in range(4):
        code += ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 4)) + '-'
    code += ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 2))
    return code


@app.route("/redemption")
def get_all():
    redemptionlist = Redemption.query.all()
    if len(redemptionlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "redemptions": [redemption.json() for redemption in redemptionlist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no redemptions."
        }
    ), 404


@app.route("/redemption/<redemption_id>")
def find_by_redemption_id(redemption_id):
    redemption = Redemption.query.filter_by(
        redemption_id=redemption_id).first()
    if redemption:
        return jsonify(
            {
                "code": 200,
                "data": redemption.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Redemption not found."
        }
    ), 404


@app.route("/redemption", methods=['POST'])
def create_redemption():
    data = request.get_json()
    redemption = Redemption(**data)

    account_result = invoke_http(
        verification_URL + "account/" + str(redemption.account_id), method='GET')

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
                    "account_id": redemption.account_id
                },
                "message": "Account does not exist."
            }
        ), 400

    reward_result = invoke_http(
        verification_URL + "reward/" + str(redemption.reward_id), method='GET')

    if reward_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if reward_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "reward_id": redemption.reward_id
                },
                "message": "Reward not found"
            }
        ), 400

    if not reward_result["data"]["is_active"]:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "reward_id": redemption.reward_id
                },
                "message": "Reward is not available"
            }
        ), 400

    redeem_json = {
        "points": reward_result["data"]["exchange_points"]
    }

    redeem_result = invoke_http(
        loyalty_URL + str(redemption.account_id) + "/redeem", method='PATCH', json=redeem_json)

    if redeem_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if redeem_result["code"] in range(300, 500):
        return redeem_result

    redemption.redemption_code = generate_redemption_code()

    try:
        db.session.add(redemption)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the redemption.",
            }
        ), 500

    notification_message = {"type": "redeem", "reward_name": reward_result["data"]["name"], "first_name": account_result["data"]
                            ["first_name"], "phone_number": account_result["data"]["phone"], "redemption_code": redemption.redemption_code}

    message = json.dumps(notification_message)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                     body=message, properties=pika.BasicProperties(delivery_mode=2))

    return jsonify(
        {
            "code": 201,
            "data": redemption.json()
        }
    ), 201


@app.route("/redemption/<redemption_id>/claimed", methods=['PATCH'])
def update_redemption_claimed(redemption_id):
    if (not Redemption.query.filter_by(redemption_id=redemption_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "redemption_id": redemption_id
                },
                "message": "Redemption not found."
            }
        ), 404

    redemption = Redemption.query.filter_by(
        redemption_id=redemption_id).first()

    if redemption.status == "Claimed":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "redemption_id": redemption_id
                },
                "message": "Redemption has already been claimed."
            }
        ), 400

    try:
        redemption.status = "Claimed"
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "redemption": redemption
                },
                "message": "An error occurred updating the redemption."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": redemption.json()
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6304, debug=True)
