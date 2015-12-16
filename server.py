from flask import Flask, request, jsonify
from user import User

app = Flask(__name__)

jsmith = User("Joe", "Smith", "jsmith", ["admins", "users"])

users = {"jsmith": jsmith}


def is_valid(data):
    return ("first_name" in data 
        and "last_name" in data 
        and "userid" in data 
        and "groups" in data)


@app.route('/users/<userid>', methods=['GET', 'DELETE', 'PUT'])
def users_handler(userid):
    if request.method == 'GET':
        return retrieve_user(userid)
    # if request.method == 'DELETE':


    if request.method == 'PUT':
        new_data = request.get_json()
        return update_user(userid, new_data)

def retrieve_user(userid):
    if userid in users:
        user = users[userid]
        response_obj = jsonify(first_name=user.first_name,
                               last_name=user.last_name,
                               userid=user.userid,
                               groups=user.groups)
        return response_obj, 200
    else:
        return 'User does not exist', 404

def update_user(userid, new_data):
    if userid in users and is_valid(new_data):
        user = users[userid]
        user.first_name = new_data['first_name']
        user.last_name = new_data['last_name']
        user.userid = new_data['userid']
        user.groups = new_data['groups']
        return 'User updated successfully', 200
    else:
        return 'User does not exists or post body is invalid', 404


if __name__ == '__main__':
    app.debug = True
    app.run()
