from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
from os import environ

from invokes import invoke_http
import requests
import json
import pika
import amqp_setup

# app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False
# CORS(app)

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"


def queueTicketsLog():
    amqp_setup.check_setup()

    queue_name = 'queueTicketsLog'

    amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=ticketCallback, auto_ack=True)
    amqp_setup.channel.start_consuming()

def ticketCallback(channel, method, properties, body):
    print("This is generateTicket.py...", flush=True)
    data = json.loads(body)
    print("data: ", data, flush=True)
    generate_queue_tickets(data)

def generate_queue_tickets(data, message):
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                    body=message, properties=pika.BasicProperties(delivery_mode=2))

    print("Queue Ticket successfully generated!", flush=True)


if __name__ == '__main__':
    queueTicketsLog()
    # app.run(host='0.0.0.0', port=6202, debug=True)
