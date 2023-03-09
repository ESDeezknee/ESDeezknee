from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/queueTicket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class QueueTicket(db.Model):
    __tablename__ = 'queueTicket'

    queue_id = db.Column(db.Integer, primary_key=True)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    ride_times = db.Column(db.Integer, nullable=False, default=0)
    queue_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, nullable = False)
    # tentative do not use FK

    def __init__(self, is_express, ride_times, order_created, account_id):
        self.is_express = is_express
        self.ride_times = ride_times
        self.order_created = order_created
        self.account_id = account_id

    def json(self):
        return {"queue_id": self.queue_id, "is_express": self.is_express, "ride_times":self.ride_times, "queue_created": self.queue_created, "account_id": self.account_id}

with app.app_context():
  db.init_app(app)
  db.create_all()

@app.route("/queueTicket")
def get_all():
    queueList = QueueTicket.query.all()
    if len(queueList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "queues": [queue.json() for queue in queueList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no queues."
        }
    ), 404

@app.get("/queueTicket/<int:queue_id>")
def get_by_id(queue_id):
    queueTicket = QueueTicket.query.filter_by(queue_id=queue_id).first()
    if queueTicket:
        return jsonify(
            {
                "code": 200,
                "data": queueTicket.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "queueTicket not found."
        }
    ), 404

@app.post("/queueTicket")
def create_queueTicket():
    if request.json is None:
        raise Exception("No data received.")
    try:
        data = request.get_json()
        new_queueTicket = QueueTicket(**data)
        db.session.add(new_queueTicket)
        db.session.commit()
        db.session.refresh(new_queueTicket)
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "queue_id": new_queueTicket.queue_id
                },
                "message": "An error occurred creating the queueTicket."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_queueTicket.json()
        }
    ), 201

@app.delete("/queueTicket/<int:queue_id>")
def delete_order(queue_id):
    queueTicket = QueueTicket.query.filter_by(queue_id=queue_id).first()
    if queueTicket:
        db.session.delete(queueTicket)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "queue_id": queueTicket.queue_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "queueTicket not found."
        }
    ), 404

@app.put("/queueTicket/<int:queue_id>")
def update_queue(queue_id):
    if request.json() is None:
        raise Exception("No data received.")
    updated_queue = QueueTicket.query.get_or_404(queue_id=queue_id)
    data = request.get_json()
    updated_queue.is_express = data["is_express"]
    updated_queue.ride_times = data["ride_times"]
    updated_queue.queue_created = data["queue_created"]
    updated_queue.account_id = data["account_id"]

    db.session.commit()
    return "Queue updated.", 200

if __name__ == '__main__':
    app.run(port=6202, debug=True)
