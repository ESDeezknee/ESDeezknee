from flask import Flask, request, jsonify, abort, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import sys, os
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

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
account_URL = environ.get('accountURL') or "http://localhost:6003/account/"
payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"
queue_URL = environ.get('queueURL') or "http://localhost:6202/queueticket/"
redemption_URL = environ.get('redemptionURL') or "http://localhost:6304/redemption_URL/"

# is verification needed here?
@app.get('/order/retrieve_account/<int:account_id>')
def verify_account(account_id):
    url = verification_URL + "account/" + str(account_id)
    account_status = invoke_http(url, method='GET')
    if account_status["code"] == 200:
        return account_status
    else:
        abort(404)

async def confirm_order(account_id):
    # logic for confirmation
    # if person presses "express ticket button",
    # return this True, if not nothing will happen
    express_button = request.form.get('button_pressed', False)
    if express_button:
        return True
    else:
        await asyncio.sleep(1)

@app.route('/order/get_payment_method/<int:account_id>', methods=['POST'])
async def select_payment_method(account_id):
    # buttons to allow user to input what payment method they want to use
    # data = await request.get_json()
    # payment_method = data['payment_method']
    # account_id = str(account_id)
    payment_method = request.form.get('payment_method')
    # payment_method = "external" # temporary 
    queue_id = 1
    check_qid = invoke_http(
        queue_URL + str(queue_id), method='GET')
    if check_qid["code"] == 200:
        queue_id += 1

    data = {
        "account_id": account_id,
        "queue_id": queue_id,
        "payment_method": payment_method
    } 

    p_method = data["payment_method"]
    if (p_method == "external"):
        return jsonify({"redirect_url": payment_URL})
    elif (p_method == "promo"):
        return jsonify({"redirect_url": promo_URL})
    elif (p_method == "loyalty"):
        points = {
            "points": 500
        }
        update_loyalty = invoke_http(
            loyalty_URL + str(account_id) + "/redeem", method='PATCH', json=points)
        print(update_loyalty)
        if update_loyalty["code"] == 200:
            ini_create_ticket(account_id, data)
            return jsonify({
                "code": 200,
                "message": "Loyalty points have been redeemed", 
                "data": update_loyalty["data"]
                }), 200
        else:
            return jsonify({
                "code": 405,
                "message": "Error in redeeming loyalty points",
                "error": update_loyalty,
            }), 405
    else:
        return "Cannot find payment method"

@app.post("/order")
def post_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            orderRequest = request.get_json()
            print("\nReceived an order in JSON:", orderRequest)

            # do the actual work
            result = place_order(orderRequest)
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "order.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# def place_order(orderRequest):

@app.route("/order/<int:account_id>/paying", methods=['POST'])
def ini_create_ticket(account_id, data1):
    # this function initialises the create ticket post
    # invoked by one of 3 payment microservice to indicate that it has been paid
    if (not request.is_json):
        data = data1
        # return jsonify({
        #     "code": 404,
        #     "message": "Invalid JSON input: " + str(request.get_data())
        # }), 404

    else:    
        data = request.get_json()
        print(data)

    create_ticket = invoke_http(
        queue_URL, method='POST', json=data)
    print(create_ticket)
    
    if create_ticket["code"] == 201:
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
    print(data)

    update_account = invoke_http(
        account_URL + str(account_id), method='PATCH', json=data)
    print(update_account)
    
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
        # generateTicket.generate_queue_tickets(data, message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))


        return jsonify({
            "code": 200,
            "message": "Account updated successfully (is express)"
        }), 200
    else:
        return jsonify({
            "code": 405,
            "message": "Order not updated",
            "invoking": update_account["message"],
        }), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6201, debug=True)