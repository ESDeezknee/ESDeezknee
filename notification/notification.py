from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

import json
import pika
import amqp_setup

from notificationapi_python_server_sdk import (notificationapi)

app = Flask(__name__)

CORS(app)

monitorBindingKey='#'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("This is notification.py...")
    print()
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Received a successful order...")
    print(order)


@app.route("/notification", methods=['POST'])
def send_notification():
    data = request.get_json()

    print(data["first_name"])

    try:
        # init
        notificationapi.init("4520cecngqlnq5guo9dbe26dte",
                             "1d1pfufn15hbv31ibs36458t92319pis5lllihcho22b94jai0na")

        # send
        notificationapi.send({
          "notificationId": "esdeezknee", 
          "templateId": "bbc3a00a-7752-4b01-9dbd-5d5c8e3faf41",
          "user": {
            "id": data["account_id"],
            "email": data["email"],   # required for email notifications
            "number": data["number"]    # required for SMS/Call
          }, 
          "mergeTags": {"firstName": data["first_name"]}
        })

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during sending of notification."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": "Notification successfully sent!"
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=True)
    # receiveOrderLog()
