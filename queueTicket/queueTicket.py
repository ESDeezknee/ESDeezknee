from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
from os import environ

import requests
import json
import pika
import amqp_setup

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"


db = SQLAlchemy(app)

CORS(app)

class QueueTicket(db.Model):
    __tablename__ = 'queueticket'

    queue_id = db.Column(db.Integer, primary_key=True)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    ride_times = db.Column(db.Integer, nullable=False, default=0)
    queue_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, nullable = False)
    order_id = db.Column(db.Integer, nullable = False)


    def __init__(self, is_express, ride_times, order_created, account_id, queue_created):
        self.is_express = is_express
        self.ride_times = ride_times
        self.order_created = order_created
        self.account_id = account_id
        self.queue_created = queue_created

    def json(self):
        return {"queue_id": self.queue_id, "is_express": self.is_express, "ride_times":self.ride_times, "queue_created": self.queue_created, "account_id": self.account_id}

with app.app_context():
  db.create_all()

@app.route("/queueticket")
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

@app.get("/queueticket/<int:queue_id>")
def get_by_id(queue_id):
    queueticket = QueueTicket.query.filter_by(queue_id=queue_id).first()
    if queueticket:
        return jsonify(
            {
                "code": 200,
                "data": queueticket.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "queueticket not found."
        }
    ), 404

@app.post("/queueticket")
def create_queueTicket():
    if request.json is None:
        raise Exception("No data received.")
    try:
        data = request.get_json()
        new_queueticket = QueueTicket(**data)
        db.session.add(new_queueticket)
        db.session.commit()
        db.session.refresh(new_queueticket)
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "queue_id": new_queueticket.queue_id
                },
                "message": "An error occurred creating the queueticket."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_queueticket.json()
        }
    ), 201

@app.delete("/queueticket/<int:queue_id>")
def delete_order(queue_id):
    queueticket = QueueTicket.query.filter_by(queue_id=queue_id).first()
    if queueticket:
        db.session.delete(queueticket)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "queue_id": queueticket.queue_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "queueticket not found."
        }
    ), 404

@app.put("/queueticket/<int:queue_id>")
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
    app.run(host='0.0.0.0', port=6202, debug=True)
