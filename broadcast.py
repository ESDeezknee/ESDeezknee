from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime, timedelta

from invokes import invoke_http

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/broadcast'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

account_URL = "http://localhost:6000/account"


class Broadcast(db.Model):
    __tablename__ = 'broadcast'

    group_id = db.Column(db.Integer, primary_key = True)
    account_id = db.Column(db.Integer, nullable=False)
    lf_pax = db.Column(db.Integer, nullable=False)
    date_of_visit = db.Column(db.Date, nullable=False)
    datetime_of_broadcast = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    def __init__(self, group_id, account_id, lf_pax,date_of_visit,):
        self.group_id = group_id
        self.account_id = account_id
        self.lf_pax = lf_pax
        self.date_of_visit = date_of_visit

    def json(self):
        return {"group_id": self.group_id,"account_id": self.account_id,"lf_pax": self.lf_pax,"date_of_visit":self.date_of_visit,"datetime_of_broadcast":self.datetime_of_broadcast}

with app.app_context():
    db.create_all()

@app.route("/broadcast")
def get_all():
    broadcastlist = Broadcast.query.all()
    if len(broadcastlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "notice": [broadcast.json() for broadcast in broadcastlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no broadcast messages."
        }
    ), 404


@app.route("/broadcast/<group_id>")
def find_by_group_id(group_id):
    broadcast = Broadcast.query.filter_by(group_id = group_id).first()
    if broadcast:
        return jsonify(
            {
                "code":200,
                "data": broadcast.json()
            }
        )
    return jsonify(
        {
            "code":404,
            "message": "broadcast not found"
    
        }
    ),404


@app.route("/broadcast/<group_id>", methods=['POST'])
def create_broadcast(group_id):
    # now = datetime.now()

    #Group_id = INT
    #Account_id = INT
    #lf_pax = INT
    #Date format: YYYY-MM-DD
    #Datetime format: YYYY-MM-DD hh:mm:ss[.fraction] fractions are needed to be sent from Postman...

    data = request.get_json()
    
    broadcast = Broadcast(**data)
    print(broadcast.json())

    try:
        db.session.add(broadcast)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during creation of broadcast."
            }
        ),500
    
    return jsonify(
        {
            "code": 201,
            "data":broadcast.json()
        }
    ),201












if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6102, debug=True)