from flask import Flask, request, jsonify
from user import User

app = Flask(__name__)

# dummy user for test
jsmith = User("Joe", "Smith", "jsmith", {"admins", "users"})


# main cached data
users = {"jsmith": jsmith}
groups = {"admins": {"jsmith"}, "users": {"jsmith"}}


def is_valid(data):
    return ("first_name" in data 
        and "last_name" in data 
        and "userid" in data 
        and "groups" in data)

@app.route('users', methods=['POST'])
def create_new_user():
    if request == 'POST':
        user = request.get_json()
        if !is_valid(user):
            return 'Invalid user record', 400
        if user[userid] in users:
            return 'User already exists', 409
        first_name = user['first_name']
        last_name = user['last_name']
        userid = user['userid']
        user_groups = set(user[groups])
        user = User(first_name, last_name, userid, user_groups)
        users[userid] = user
        for group in user_groups:
            groups[group].add(userid)
        return 'User created', 201


@app.route('/users/<userid>', methods=['GET', 'DELETE', 'PUT'])
def users_handler(userid):
    if request.method == 'GET':
        return retrieve_user(userid)
    if request.method == 'DELETE':
        return delete_user(userid)
    if request.method == 'PUT':
        new_data = request.get_json()
        return update_user(userid, new_data)

def retrieve_user(userid):
    if userid in users:
        user = users[userid]
        response_obj = jsonify(first_name=user.first_name,
                               last_name=user.last_name,
                               userid=user.userid,
                               groups=list(user.groups))
        return response_obj, 200
    else:
        return 'User does not exist', 404

def update_user(userid, new_data):
    if userid in users and is_valid(new_data):
        user = users[userid]
        user.first_name = new_data['first_name']
        user.last_name = new_data['last_name']
        user.userid = new_data['userid']
        # handle group reference
        groups_to_remove_from = user.groups.difference(new_data['groups'])
        groups_to_add_to = set(new_data['groups']).difference(user.groups)
        update_groups(userid, groups_to_remove_from, groups_to_add_to)
        user.groups = new_data['groups']

        return 'User updated successfully', 200
    else:
        return 'User does not exists or post body is invalid', 404

def update_groups(userid, groups_to_remove_from, groups_to_add_to):
    for group in groups_to_remove_from:
            groups[group].discard(userid)

    for group in groups_to_add_to:
        if group not in groups:
            groups[group] = set()
        groups[group].add(userid)
    
def delete_user(userid):
    if userid in users:
        user = users[userid]
        # remove user from groups
        for group in user.groups:
            groups[group].discard(userid)
        del users[userid]
        return 'User has been deleted from data store', 200
    else:
        return 'User does not exist', 404





if __name__ == '__main__':
    app.debug = True
    app.run()
