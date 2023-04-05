from flask import Flask, request, jsonify, abort, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import sys
import os
import asyncio

import requests
from invokes import invoke_http
import pika
import amqp_setup
import json

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get(
    'verificationURL') or "http://localhost:6001/verification/"
account_URL = environ.get('accountURL') or "http://localhost:6003/account/"
epayment_URL = environ.get('epaymentURL') or "http://localhost:6203/epayment"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"
queue_URL = environ.get('queueURL') or "http://localhost:6202/queueticket/"
order_URL = environ.get('orderURL') or "http://localhost:6201/order/"


@app.route('/order/get_payment_method/<int:account_id>', methods=['POST'])
async def select_payment_method(account_id):
    payment_method1 = request.get_json()
    payment_method = payment_method1['payment_method']
    check_qid = invoke_http(
        queue_URL, method='GET')
    if check_qid["code"] == 200:
        if len(check_qid["data"]["queues"]) == 0:
            queue_id = 1
        else:
            queue_id = len(check_qid["data"]["queues"]) + 1
    else:
        queue_id = 1

    data = {
        "account_id": account_id,
        "queue_id": queue_id,
        "payment_method": payment_method
    }

    if (payment_method == "external"):
        response = invoke_http(epayment_URL + 'create_checkout_session',
                               method="POST", json={"account_id": data["account_id"]})
        if response:
            response["queue_id"] = data["queue_id"]

            ini_create_ticket = invoke_http(
                order_URL + str(account_id) + "/paying", method='POST', json=data)
            if ini_create_ticket["code"] == 201:
                return jsonify({
                    "code": 200,
                    "data": response,
                    "queue_id": data["queue_id"]
                    }), 200
            else:
                return jsonify({
                    "code": 405,
                    "data": response,
                    "message": "Failed to create ticket"
                }), 405

        else:
            return jsonify({'status': 'error', 'message': 'Failed to create checkout session', 'data': response})
    elif (payment_method == "promo"):
        promo_json = {
            "is_used": 1,
            "promo_code": payment_method1["promo_code"]
        }
        update_promo = invoke_http(
            promo_URL + str(account_id), method="PATCH", json=promo_json)
        if update_promo["code"] == 200:
            ini_create_ticket = invoke_http(
                order_URL + str(account_id) + "/paying", method='POST', json=data)
            if ini_create_ticket["code"] == 201:
                return jsonify({
                    "code": 200,
                    "message": "Promo code has been redeemed",
                    "data": update_promo["data"],
                    "queue_id": data["queue_id"]
                    }), 200
        else:
            return jsonify({
                "code": 405,
                "message": update_promo["message"]
            }), 405
    elif (payment_method == "loyalty"):
        points = {
            "points": 500
        }
        update_loyalty = invoke_http(
            loyalty_URL + str(account_id) + "/redeem", method='PATCH', json=points)
        if update_loyalty["code"] == 200:
            ini_create_ticket = invoke_http(
                order_URL + str(account_id) + "/paying", method='POST', json=data)
            if ini_create_ticket["code"] == 201:
                return jsonify({
                    "code": 200,
                    "message": "Loyalty points have been redeemed",
                    "data": update_loyalty["data"],
                    "queue_id": data["queue_id"],
                    "available_points": update_loyalty["data"]["available_points"]
                    }), 200
        else:
            return jsonify({
                "code": 405,
                "message": update_loyalty["message"],
                "available_points": update_loyalty["data"]["available_points"]
            }), 405
    else:
        return "Cannot find payment method"


@app.route("/order/<int:account_id>/paying", methods=['POST'])
def ini_create_ticket(account_id):
    # this function initialises the create ticket post
    # invoked by one of 3 payment microservice to indicate that it has been paid
    if (not request.is_json):
        return jsonify({
            "code": 404,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 404

    data = request.get_json()

    create_ticket = invoke_http(
        queue_URL, method='POST', json=data)

    if create_ticket["code"] == 201:
        # For User Scenario 3, Update Challenge Status
        challenge_message = {
            "mission_id": 2,
            "code": 201
        }

        challenge_message.update(create_ticket["data"])
        message = json.dumps(challenge_message)

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename1, routing_key="challenge.challenge_complete", body=message, properties=pika.BasicProperties(delivery_mode=2))


        return jsonify({
            "code": 201,
            "message": "Queueticket being created", 
            "data": create_ticket["data"]
            }), 201
    else:
        return jsonify({
            "code": 405,
            "message": "Queueticket not being created",
            "error": create_ticket,
        }), 405

@app.patch("/order/<int:account_id>/paid")
def update_order(account_id):
    # this function is being invoked by post queue ticket
    # indicates that the ticket has been created
    if (not request.is_json):
        return jsonify({
            "code": 404,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 404
    
    data = request.get_json()

    update_account = invoke_http(
        account_URL + str(account_id), method='PATCH', json=data)
    
    if update_account["code"] == 200:

        account_result = invoke_http(
            verification_URL + "account/" + str(data["account_id"]), method='GET')

        notification_message = {
            "type": "queueticket",
            "account_id": data["account_id"],
            "first_name": account_result["data"]["first_name"],
            "phone_number": account_result["data"]["phone"],
            "payment_method": data["payment_method"],
            "queue_id": data["queue_id"],
            "message": "You have successfully created a queueticket."
        }
        message = json.dumps(notification_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))


        return jsonify({
            "code": 200,
            "message": "Account updated successfully (is express)",
            "queue_id": data["queue_id"]
        }), 200
    else:
        return jsonify({
            "code": 405,
            "message": "Order not updated"
        }), 405

@app.route("/order/<int:queue_id>/used", methods=['PATCH'])
def ticket_used(queue_id):
    if (not request.is_json):
        return jsonify({
            "code": 404,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 404
    
    data = request.get_json()

    ticket_update = invoke_http(
        queue_URL + str(data["queue_id"]), method='PATCH', json=data)

    if ticket_update["code"] == 200:
        update_is_prio = {
            "is_priority": 0
        }
        account_res = invoke_http(
            account_URL + str(account_URL), method='PATCH', json=update_is_prio)
        
        if account_res["code"] == 200:
            return jsonify({
                "code": 200,
                "message": "Ticket used successfully"
            }), 200
        
        account_result = invoke_http(
            verification_URL + "account/" + str(ticket_update["data"]["account_id"]), method='GET')

        notification_message = {
            "type": "use_queue",
            "account_id": ticket_update["data"]["account_id"],
            "first_name": account_result["data"]["first_name"],
            "phone_number": account_result["data"]["phone"],
            "payment_method": ticket_update["data"]["payment_method"],
            "queue_id": ticket_update["data"]["queue_id"],
            "message": "You have redeemed your queue ticket."
        }
        message = json.dumps(notification_message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 200,
            "message": "Ticket used successfully",
            "data": ticket_update["data"]
        }), 200
        
    else:
        return jsonify({
            "code": 405,
            "message": ticket_update["message"]
        }), 405
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6201, debug=True)