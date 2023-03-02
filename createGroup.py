from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/group'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __init__(self, description, status):
        self.description = description
        self.status = status

    def json(self):
        return {"group_id": self.group_id, "description": self.description, "status": self.status}
    

@app.route("/group")
def get_all():
    grouplist = Group.query.all()
    if len(grouplist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "groups": [group.json() for group in grouplist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no groups."
        }
    ), 404

@app.route("/group/<group_id>")
def find_by_group_id(group_id):
    group = Group.query.filter_by(group_id=group_id).first()
    if group:
        return jsonify(
            {
                "code": 200,
                "data": group.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Group not found."
        }
    ), 404

@app.route("/group/<group_id>", methods=['POST'])
def create_group(group_id):
    data = request.get_json()
    group = Group(**data)

    if (Group.query.filter_by(group_id=group_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "group_id": group.group_id
                },
                "message": "Group already exists."
            }
        ), 400

    try:
        db.session.add(group)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the group."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": group.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)