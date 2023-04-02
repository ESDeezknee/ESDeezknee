from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from invokes import invoke_http

import json
import threading
import pika
import amqp_setup


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

account_URL = environ.get('accountURL') or "http://localhost:6000/account/"
mission_URL = environ.get('missionURL') or "http://localhost:6300/mission/"
reward_URL = environ.get('rewardURL') or "http://localhost:6303/reward/"
grouping_URL = environ.get('groupingURL') or "http://localhost:6103/grouping/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"
queue_URL = environ.get('queueURL') or "http://localhost:6202/queueticket/"
icebreakers_url = environ.get('icebreakersURL') or "http://localhost:6101/api/icebreakers/"
challenge_url = environ.get('challengeURL') or "http://localhost:6302/challenge/"


monitorBindingKey = '#'

def receiveMessage():
    rabbitmq_thread = threading.Thread(target=start_consuming)
    rabbitmq_thread.start()

def start_consuming():
    amqp_setup.check_setup()

    challenge_complete_queue_name = 'challenge_complete'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=challenge_complete_queue_name, on_message_callback=challenge_callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def challenge_callback(channel, method, properties, body):
    print("This is verification.py...", flush=True)
    print("Received message:", json.loads(body), flush=True)

    data = json.loads(body)

    if data["code"] not in range(200,300):
      return

    for account_id in data["group_obj"]["list_account"]:
      challenge_result = invoke_http(challenge_url + "account/" + str(account_id) + "/mission/" + str(data["mission_id"]), method='GET')
      
      if challenge_result["code"] not in range(200,300):
        return

      if challenge_result["data"]["status"] == "Completed":
        return

      update_challenge_result = invoke_http(challenge_url + str(challenge_result["data"]["challenge_id"]) + "/complete", method='PATCH')

      print(update_challenge_result)




@app.route("/verification/account/<account_id>")
def verify_account(account_id):
    return invoke_http(
        account_URL + str(account_id), method='GET')

@app.route("/verification/grouping/<grouping_id>")
def verify_grouping(grouping_id):
    return invoke_http(
        grouping_URL + str(grouping_id),  method='GET')

@app.route("/verification/mission/<mission_id>")
def verify_mission(mission_id):
    return invoke_http(
        mission_URL + str(mission_id), method='GET')

@app.route("/verification/reward/<reward_id>")
def verify_reward(reward_id):
    return invoke_http(
        reward_URL + str(reward_id), method='GET')

@app.route("/verification/queueticket/<queue_id>")
def verify_queue(queue_id):
    return invoke_http(
        queue_URL + str(queue_id), method='GET')


@app.route("/verification/icebreakers")
def get_icebreakers():
    return invoke_http(
        icebreakers_url, method='GET')


if __name__ == '__main__':
    receiveMessage()
    app.run(host='0.0.0.0', port=6001, debug=True)
