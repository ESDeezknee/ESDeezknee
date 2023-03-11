from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime, timedelta

from invokes import invoke_http

import amqp_setup
import pika
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verificationURL')
loyalty_URL = environ.get('loyaltyURL')


class Challenge(db.Model):
    __tablename__ = 'challenge'

    challenge_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    mission_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(64), nullable=False, default="In Progress")
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def __init__(self, account_id, mission_id):
        self.account_id = account_id
        self.mission_id = mission_id

    def json(self):
        return {"challenge_id": self.challenge_id, "account_id": self.account_id, "mission_id": self.mission_id, "start_date": self.start_date, "end_date": self.end_date, "status": self.status, "created": self.created, "modified": self.modified}


with app.app_context():
    db.create_all()


@app.route("/challenge")
def get_all():
    challengelist = Challenge.query.all()
    if len(challengelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "challenges": [challenge.json() for challenge in challengelist],
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no challenges."
        }
    ), 404


@app.route("/challenge/<challenge_id>")
def find_by_challenge_id(challenge_id):
    challenge = Challenge.query.filter_by(challenge_id=challenge_id).first()

    if challenge:
        # message = json.dumps({ "type": "email", "first_name": "Benji", "email": "kangting.ng.2021@scis.smu.edu.sg" })
        message = json.dumps({ "type": "sms", "first_name": "Benji", "phone_number": "+6597861048" })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.info", body=message, properties=pika.BasicProperties(delivery_mode = 2))

        return jsonify(
            {
                "code": 200,
                "data": challenge.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Challenge not found."
        }
    ), 404


@app.route("/challenge", methods=['POST'])
def create_challenge():
    data = request.get_json()
    challenge = Challenge(**data)

    account_result = invoke_http(
        verification_URL + "account/" + str(challenge.account_id), method='GET')

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
                    "account_id": challenge.account_id
                },
                "message": "Account does not exist."
            }
        ), 400

    mission_result = invoke_http(
        verification_URL + "mission/" + str(challenge.mission_id), method='GET')

    if mission_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if mission_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "mission_id": challenge.mission_id
                },
                "message": "Mission not found"
            }
        ), 400

    if not mission_result["data"]["is_active"]:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "mission_id": challenge.mission_id
                },
                "message": "Mission is not available"
            }
        ), 400

    mission_duration = mission_result["data"]["duration"]

    existing_challenge = Challenge.query.filter_by(
        account_id=challenge.account_id, mission_id=challenge.mission_id).first()

    if (existing_challenge):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "challenge_id": existing_challenge.challenge_id
                },
                "message": "Challenge already exists."
            }
        ), 400

    try:
        current_time = datetime.now()
        challenge.start_date = current_time
        challenge.end_date = current_time + timedelta(hours=mission_duration)
        db.session.add(challenge)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the challenge.",
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": challenge.json()
        }
    ), 201


@app.route("/challenge/<challenge_id>/complete", methods=['PATCH'])
def update_challenge_complete(challenge_id):
    if (not Challenge.query.filter_by(challenge_id=challenge_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "challenge_id": challenge_id
                },
                "message": "Challenge not found."
            }
        ), 404

    challenge = Challenge.query.filter_by(challenge_id=challenge_id).first()

    if challenge.status == "Completed":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "challenge_id": challenge_id
                },
                "message": "Challenge is already completed."
            }
        ), 400

    mission_result = invoke_http(
        verification_URL + "mission/" + str(challenge.mission_id), method='GET')

    if mission_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if mission_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "mission_id": challenge.mission_id
                },
                "message": "Mission not found"
            }
        ), 400

    earn_json = {
        "points": mission_result["data"]["award_points"]
    }

    earn_result = invoke_http(
        loyalty_URL + str(challenge.account_id) + "/earn", method='PATCH', json=earn_json)

    if earn_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if earn_result["code"] in range(300, 500):
        return earn_result

    try:
        challenge.status = "Completed"
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "challenge": challenge
                },
                "message": "An error occurred updating the challenge."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": challenge.json()
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6302, debug=True)
