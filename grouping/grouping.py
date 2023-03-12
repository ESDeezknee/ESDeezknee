from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from invokes import invoke_http


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Grouping(db.Model):
    __tablename__ = 'groupings'

    grouping_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False, default="grouping has been created. Members have not been added")
    status = db.Column(db.String(256), nullable=False, default="Started")

    def __init__(self, description, status):
        self.description = description
        self.status = status

    def json(self):
        return {"grouping_id": self.grouping_id, "description": self.description, "status": self.status}

with app.app_context():
    db.create_all()  

@app.route("/grouping")
def get_all():
    groupinglist = Grouping.query.all()
    if len(groupinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "groupings": [grouping.json() for grouping in groupinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no groupings."
        }
    ), 404

@app.route("/grouping/<grouping_id>")
def find_by_grouping_id(grouping_id):
    grouping = Grouping.query.filter_by(grouping_id=grouping_id).first()
    if grouping:
        return jsonify(
            {
                "code": 200,
                "data": grouping.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "grouping not found."
        }
    ), 404

@app.route("/grouping", methods=['POST'])
def create_grouping():
    data = request.get_json()
    grouping = Grouping(**data)
    print(grouping.json())

    try:
        db.session.add(grouping)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Grouping.",
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": grouping.json(),
            "message": "New group creation success."
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6103, debug=True)