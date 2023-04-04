from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
from os import environ

from invokes import invoke_http
import requests
import json


from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
order_URL = environ.get('orderURL') or "http://localhost:6201/order/"


db = SQLAlchemy(app)

CORS(app)

class QueueTicket(db.Model):
    __tablename__ = 'queuetickets'

    queue_id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_priority = db.Column(db.Boolean, default=False, nullable=False)
    account_id = db.Column(db.Integer, nullable = False)
    payment_method = db.Column(db.String(256), nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)


    def __init__(self, queue_id, is_priority, account_id, payment_method, is_used):
        self.queue_id = queue_id
        self.is_priority = is_priority
        self.account_id = account_id
        self.payment_method = payment_method
        self.is_used = is_used

    def json(self):
        return {"queue_id": self.queue_id, "is_priority": self.is_priority, "account_id":self.account_id, "payment_method": self.payment_method, "is_used": self.is_used}

with app.app_context():
  db.create_all()
  existing_queue_ticket_1 = db.session.query(QueueTicket).filter(QueueTicket.queue_id==1).first()
  if not existing_queue_ticket_1:
      new_queue_ticket_1 = QueueTicket(queue_id=1, is_priority=1, account_id=1, payment_method="promo", is_used=0)
      new_queue_ticket_2 = QueueTicket(queue_id=2, is_priority=1, account_id=2, payment_method="external", is_used=0)
      new_queue_ticket_3 = QueueTicket(queue_id=3, is_priority=1, account_id=3, payment_method="loyalty", is_used=0)
      db.session.add(new_queue_ticket_1)
      db.session.add(new_queue_ticket_2)
      db.session.add(new_queue_ticket_3)
      db.session.commit()


@app.get("/queueticket/")
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

@app.route("/queueticket/", methods=['POST'])
def create_queueticket():
    if request.json is None:
        raise Exception("No data received.")
    
    data = request.get_json()

    verify_queue = invoke_http(
        verification_URL + "queueticket/" + str(data["queue_id"]), method='GET')

    if verify_queue["code"] != 200:
        new_queue = {
            "queue_id": data["queue_id"],
            "is_priority": 1,
            "account_id": data["account_id"],
            "payment_method": data["payment_method"],
            "is_used": 0
        }
    else:
        data["queue_id"] += 1
        new_queue = {
            "queue_id": data["queue_id"],
            "is_priority": 1,
            "account_id": data["account_id"],
            "payment_method": data["payment_method"],
            "is_used": 0
        }

    account_result = invoke_http(
        verification_URL + "account/" + str(new_queue["account_id"]), method='GET')

    if account_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong! Account"
            }
        ), 500

    if account_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": new_queue["account_id"]
                },
                "message": "Account does not exist."
            }
        ), 400

    paid_ticket = invoke_http(
        order_URL + str(new_queue["account_id"]) + "/paid", method="PATCH", json=new_queue)
    print(paid_ticket)

    if paid_ticket["code"] in range(500, 600):
            return jsonify(
                {
                    "code": 500,
                    "message": "Oops, something went wrong! paid ticket",
                    "asdf": paid_ticket
                }
            ), 500 

    try:
        
        db.session.add(QueueTicket(
            queue_id=new_queue["queue_id"],
            is_priority=new_queue["is_priority"],
            account_id=new_queue["account_id"],
            payment_method=new_queue["payment_method"],
            is_used=new_queue["is_used"]
        ))
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the queueticket.",
                "asdf": new_queue
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Queueticket created",
            "data": new_queue
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

@app.patch("/queueticket/<int:queue_id>")
def queue_used(queue_id):

    data = request.get_json()
    
    updated_queue = QueueTicket.query.filter_by(queue_id=queue_id).first()
    
    try:
        updated_queue.is_used = data["is_used"]

        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": updated_queue.json(),
                "message": "Queue ticket has been updated (used)."
            }
        ), 200

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the queueticket."
            }
        ), 500
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6202, debug=True)