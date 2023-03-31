from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
from os import environ

from invokes import invoke_http
import requests
import json
from json import JSONEncoder


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
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    account_id = db.Column(db.Integer, nullable = False)
    payment_method = db.Column(db.String(256), nullable=False)


    def __init__(self, queue_id, is_express, account_id, payment_method):
        self.queue_id = queue_id
        self.is_express = is_express
        self.account_id = account_id
        self.payment_method = payment_method

    def json(self):
        return {"queue_id": self.queue_id, "is_express": self.is_express, "account_id":self.account_id, "payment_method": self.payment_method}

with app.app_context():
  db.create_all()
  existing_queue_ticket_1 = db.session.query(QueueTicket).filter(QueueTicket.queue_id==1).first()
  if not existing_queue_ticket_1:
      new_queue_ticket_1 = QueueTicket(queue_id=1, is_express=1, account_id=1, payment_method="promo")
      new_queue_ticket_2 = QueueTicket(queue_id=2, is_express=1, account_id=2, payment_method="stripe")
      new_queue_ticket_3 = QueueTicket(queue_id=3, is_express=1, account_id=3, payment_method="loyalty")
      db.session.add(new_queue_ticket_1)
      db.session.add(new_queue_ticket_2)
      db.session.add(new_queue_ticket_3)
      db.session.commit()

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__ 

@app.get("/queueticket")
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

@app.route("/queueticket", methods=['POST'])
def create_queueticket():
    if request.json is None:
        raise Exception("No data received.")
    
    data1 = request.get_json()
    data = data1["data"]
    print(data)
    new_queue1 = QueueTicket(
        queue_id=data["queue_id"],
        is_express=data["is_express"],
        account_id=data["account_id"],
        payment_method=data["payment_method"]
    )
    MyEncoder().encode(new_queue1)
    new_queue_json = json.dumps(cls=MyEncoder, obj=new_queue1)
    new_queue_l = json.loads(new_queue_json)
    new_queue = {
        "queue_id": new_queue_l["queue_id"],
        "is_express": new_queue_l["is_express"],
        "account_id": new_queue_l["account_id"],
        "payment_method": new_queue_l["payment_method"]
    }

    existing_queue = QueueTicket.query.filter_by(
        account_id=new_queue["account_id"]).first()

    if (existing_queue):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": existing_queue.account_id
                },
                "message": "queueticket already exists."
            }
        ), 400

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
            is_express=new_queue["is_express"],
            account_id=new_queue["account_id"],
            payment_method=new_queue["payment_method"]
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

    

    # notification_message = {
    #     "type": "queueticket",
    #     "account_id": new_queue["account_id"],
    #     "phone_number": account_result["data"]["phone"],
    #     "payment_method": new_queue["payment_method"],
    #     "queue_id": new_queue["queue_id"],
    #     "message": "You have successfully created a queueticket."
    #     }
    # message = json.dumps(notification_message)
    # # generateTicket.generate_queue_tickets(data, message)
    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
    #                                 body=message, properties=pika.BasicProperties(delivery_mode=2))



    return jsonify(
        {
            "code": 201,
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

@app.put("/queueticket/<int:queue_id>")
def update_queue(queue_id):
    if (not QueueTicket.query.filter_by(queue_id=queue_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "queue_id": queue_id
                },
                "message": "Queue not found."
            }
        ), 404
    data = request.get_json()
    print(data)
    updated_queue = QueueTicket.query.filter_by(queue_id=queue_id).first()
    # print(updated_queue)
    

    account_result = invoke_http(
        verification_URL + "account/" + str(updated_queue.account_id), method='GET')

    try:
        updated_queue.is_express = data["is_express"]
        updated_queue.account_id = data["account_id"]
        updated_queue.payment_method = data["payment_method"]

        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the queueticket.",
                "asdf": updated_queue
            }
        ), 500
    
    notification_message = {
        "type": "queueticket",
        "account_id": updated_queue.account_id,
        "phone_number": account_result["data"]["phone"],
        "payment_method": updated_queue.payment_method,
        "queue_id": updated_queue.queue_id,
        "message": "You have successfully updated a queueticket."
    }
    message = json.dumps(notification_message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                    body=message, properties=pika.BasicProperties(delivery_mode=2))


    return jsonify(
        {
            "code": 200,
            "data": updated_queue.json()
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6202, debug=True)