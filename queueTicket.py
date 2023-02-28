from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/queueTicket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class QueueTicket(db.Model):
    __tablename__ = 'queueTicket'

    queue_id = db.Column(db.Integer, primary_key=True)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    queue_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    account_id = db.Column(db.Integer, ForeignKey("account.account_id"), nullable = False, primary_key = True)

    def __init__(self, is_express, order_created, account_id):
        self.is_express = is_express
        self.order_created = order_created
        self.account_id = account_id

    def json(self):
        return {"queue_id": self.queue_id, "is_express": self.is_express, "queue_created": self.queue_created, "account_id": self.account_id}


@app.route("/queueTicket")
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
