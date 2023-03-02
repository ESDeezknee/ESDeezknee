from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime, timedelta

from invokes import invoke_http

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/challenge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

mission_URL = "http://localhost:5001/mission"


class Challenge(db.Model):
    __tablename__ = 'challenge'

    challenge_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.ForeignKey(
        'account.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    mission_id = db.Column(db.ForeignKey(
        'mission.mission_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
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
        )
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
        return jsonify(
            {
                "code": 200,
                "data": challenge.json()
            }
        )
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

    mission_result = invoke_http(
        mission_URL + "/" + str(challenge.mission_id), method='GET')

    if mission_result["code"] not in range(200, 300):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "mission_id": challenge.mission_id
                },
                "message": "Mission not found"
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
        print(challenge.json())
        # db.session.add(challenge)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
