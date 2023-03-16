from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from invokes import invoke_http

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

account_URL = environ.get('accountURL') or "http://localhost:6000/account/"
mission_URL = environ.get('missionURL') or "http://localhost:6300/mission/"
reward_URL = environ.get('rewardURL') or "http://localhost:6303/reward/"
grouping_URL = environ.get('groupingURL') or "http://localhost:6103/grouping/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"



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

@app.route("/verification/promo/<promo_id>")
def verify_promo(promo_id):
    return invoke_http(
        reward_URL + str(promo_id), method='GET')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
