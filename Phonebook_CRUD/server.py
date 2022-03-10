from bson import ObjectId
from flask import Flask, Response, request
import pymongo
import json

app = Flask(__name__)
mongo = pymongo.MongoClient(host="localhost", port=27017)

db = mongo.company


# Add user information
@app.route("/users", methods=["POST"])
def create_user():
    user = {"name": request.form["name"],
            "lastName": request.form["lastname"],
            "Contact_number": request.form["Contact_number"],
            "E-mail": request.form["E-mail"],
            "Address": request.form["Address"]}
    dbResponse = db.users.insert_one(user)
    print(dbResponse.inserted_id)
    return Response(
        response=json.dumps(
            {"message": "user created",
             "id": f"{dbResponse.inserted_id}"}),
        status=200,
        mimetype="application/json")


@app.route("/delete/<id>", methods=['DELETE'])
def delete_todo(id):
    result = db.users.delete_one({'_id': ObjectId(id)})
    return result.raw_result


@app.route("/update/<id>", methods=['PATCH'])
def update_one(id):
    user = {"name": request.form["name"],
            "lastName": request.form["lastname"],
            "Contact_number": request.form["Contact_number"],
            "E-mail": request.form["E-mail"],
            "Address": request.form["Address"]}
    result = db.todos.update_one({'_id': ObjectId(id)}, {"$set": {'title': "updated title"}})
    return result.raw_result


@app.route("/", methods=["GET"])
def getUsers():
    users = db.users.find()
    print([user for user in users])
    return Response(
        response=json.dumps(
            {}),
        status=200,
        mimetype="application/json")


if __name__ == "__main__":
    app.run(port=80, debug=True)
