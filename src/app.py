"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import random

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    _id = id
    members = jackson_family.get_all_members()

    for member in members:
        if _id in member.values():
            member = jackson_family.get_member(_id)

            response_body = {
                "member": member
            }

            return jsonify(response_body), 200

        else:    
            response_body = {
                "msg": "Member does not exist. Please enter a valid ID"
            }

            return jsonify(response_body), 404


@app.route('/add-member', methods=['POST'])
def add_member():
    _id = jackson_family._generateId()
    name = request.json.get('name')
    last_name = jackson_family.last_name
    age = request.json.get('age')
    lucky_numbers = tuple(random.sample(range(0, 100), 5))

    member = {
        "id": _id,
        "first_name": name,
        "last_name": last_name,
        "age": '{member_age} years old'.format(member_age=age),
        "lucky_numbers": lucky_numbers
    }

    if name == '' or name == None or age == None or type(name) is not str or type(age) is not int:
        response_body = {
            "msg": "Bad request. Please check the information submited"
        }

        return jsonify(response_body), 400 
    
    jackson_family.add_member(member)

    response_body = {
        "msg": "Member added successfully!"
    }

    return jsonify(response_body), 200

@app.route('/delete-member/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    _id = id
    members = jackson_family.get_all_members()

    for member in members:
        if _id in member.values():
            jackson_family.delete_member(_id)

            response_body = {
                "msg": "Member deleted"
            }

            return jsonify(response_body), 200

        else:    
            response_body = {
                "msg": "Member does not exist. Please enter a valid ID"
            }

            return jsonify(response_body), 404

@app.route('/update-member/<int:id>', methods=['PUT'])
def update_selected_member(id):
    _id = id
    name = request.json.get("name")
    age = request.json.get("age")
    members = jackson_family.get_all_members()

    for member in members:
        if name == '' or name == None or age == None or type(name) is not str or type(age) is not int:
            response_body = {
                "msg": "Bad request. Please check the information submited"
            }

            return jsonify(response_body), 400 

        elif _id in member.values():
            jackson_family.update_member(id, name, age)

            response_body = {
                "msg": "Member updated!"
            }

            return jsonify(response_body), 200
            
        else:    
            response_body = {
                "msg": "Member does not exist. Please enter a valid ID"
            }

            return jsonify(response_body), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
