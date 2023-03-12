from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from invokes import invoke_http

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

account_URL = environ.get('accountURL')
mission_URL = environ.get('missionURL')
reward_URL = environ.get('rewardURL')
group_URL = environ.get('groupURL')



@app.route("/verification/account/<account_id>")
def verify_account(account_id):
    return invoke_http(
        account_URL + str(account_id), method='GET')

@app.route("/verification/mission/<mission_id>")
def verify_mission(mission_id):
    return invoke_http(
        mission_URL + str(mission_id), method='GET')

@app.route("/verification/reward/<reward_id>")
def verify_reward(reward_id):
    return invoke_http(
        reward_URL + str(reward_id), method='GET')

@app.route("/verification/group/<group_id>")
def verify_group(group_id):
    return invoke_http(
        group_URL + str(group_id),  method='GET')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
