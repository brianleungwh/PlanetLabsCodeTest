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

@app.route('/users', methods=['POST'])
def create_new_user():
    if request.method == 'POST':
        user = request.get_json()
        userid = user['userid']
        if not is_valid(user):
            return 'Invalid user record', 400
        if userid in users:
            return 'User already exists', 409
        first_name = user['first_name']
        last_name = user['last_name']
        user_groups = set(user['groups'])
        user = User(first_name, last_name, userid, user_groups)
        users[userid] = user
        for group in user_groups:
            if group not in groups:
                groups[group] = set()
            groups[group].add(userid)
        return 'User created', 201

@app.route('/users/<userid>', methods=['GET', 'PUT', 'DELETE'])
def users_handler(userid):
    if request.method == 'GET':
        return retrieve_user(userid)
    if request.method == 'PUT':
        new_data = request.get_json()
        return update_user(userid, new_data)
    if request.method == 'DELETE':
        return delete_user(userid)

@app.route('/groups/<groupname>', methods=['GET', 'PUT', 'DELETE'])
def groups_handler(groupname):
    if request.method == 'GET':
        return retrieve_group_members(groupname)
    if request.method == 'PUT':
        members = request.get_json()['members']
        return update_group_memebership(groupname, members)
    if request.method == 'DELETE':
        return delete_group(groupname)


def retrieve_group_members(groupname):
    if groupname in groups:
        response_obj = jsonify(members=list(groups[groupname]))
        return response_obj, 200
    else:
        return 'Group does not exists', 404

def update_group_membership(groupname, members):
    if groupname not in groups:
        return 'Group does not exists', 404
    new_memebership = set(members)
    # find users that are in the old list but not in the new list
    # and remove groupname from their groups
    to_remove_from = groups[groupname].difference(new_memebership)
    for user in to_remove_from:
        users[user].groups.discard(groupname)

    # find users that are in the new list but not in the old list 
    # and add groupname to their groups
    to_add_to = new_memebership.difference(groups[groupname])
    for user in to_add_to:
        users[user].groups.add(groupname)

    # replace group
    groups[groupname] = set(members)
    return 'Group memberships updated', 200

def delete_group(groupname):
    if groupname not in groups:
        return 'Group does not exists', 404

    # remove group from users' group set
    for user in groups[groupname]:
        users[user].groups.discard(groupname)

    # remove group from groups
    del groups[groupname]



@app.route('/groups', methods=['POST'])
def create_new_group():
    if request.method == 'POST':
        json = request.get_json()
        new_group_name = json[name]
        if new_group_name in groups:
            return 'Group already exists', 409
        groups[new_group_name] = set()
        return 'New group created', 201

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
        # handle group references
        groups_to_remove_from = user.groups.difference(new_data['groups'])
        groups_to_add_to = set(new_data['groups']).difference(user.groups)

        for group in groups_to_remove_from:
            groups[group].discard(userid)

        for group in groups_to_add_to:
            if group not in groups:
                groups[group] = set()
            groups[group].add(userid)

        user.groups = new_data['groups']

        return 'User updated successfully', 200
    else:
        return 'User does not exists or post body is invalid', 404
    
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
