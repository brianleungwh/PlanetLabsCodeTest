from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

user_group = db.Table('user_group',
    db.Column('userid', db.String(30), db.ForeignKey('user.userid')),
    db.Column('group_name', db.String(30), db.ForeignKey('group.name'))
)

class User(db.Model):
    userid = db.Column(db.String(30), primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    groups = db.relationship('Group', secondary=user_group,
                backref=db.backref('users', lazy='dynamic'))

    def __init__(self, userid, first_name, last_name):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name

    # def add(self, user):
    #     db.session.add(user)
    #     return session_commit()

    # def delete(self, user):
    #     db.session.delete(user)
    #     return session_commit()


class Group(db.Model):
    name = db.Column(db.String(30), primary_key=True)

    def __init__(self, name):
        self.name = name

    # def add(self, group):
    #     db.session.add(group)
    #     return session_commit()

    # def delete(self, group):
    #     db.session.delete(group)
    #     return session_commit()

    # def __str__(self):
    #     return self.name


# def session_commit():
#     try:
#         db.session.commit()
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         error = str(e)
#         return error

db.create_all()


def is_valid(data):
    return ("first_name" in data 
        and "last_name" in data 
        and "userid" in data 
        and "groups" in data)

@app.route('/users', methods=['POST'])
def create_new_user():
    user = request.get_json()
    if not is_valid(user):
        return 'Invalid user record', 400

    userid = user['userid']
    if User.query.get(userid) is not None:
        return 'User already exists', 409
    first_name = user['first_name']
    last_name = user['last_name']
    groups = user['groups']

    # create model instance
    user = User(userid, first_name, last_name)
    
    for group_name in groups:
        group = Group.query.get(group_name)
        if group is None:
            # if group doesn't exist already, create it
            group = Group(group_name)
        # add association
        user.groups.append(group)

    # add user to db
    db.session.add(user)
    # since user is associated with groups instances, groups that 
    # did not already exists will be automatically added
    db.session.commit()

    return 'User created', 201

@app.route('/groups', methods=['POST'])
def create_new_group():
    json = request.get_json()
    if "name" not in json:
        return 'Invalid request body', 400
    new_group_name = json['name']
    group = Group.query.get(new_group_name)
    if group is not None:
        return 'Group already exists', 409
    group = Group(new_group_name)
    db.session.add(group)
    db.session.commit()
    return 'New group created', 201

@app.route('/users/<userid>', methods=['GET', 'PUT', 'DELETE'])
def users_handler(userid):
    if request.method == 'GET':
        return retrieve_user(userid)
    if request.method == 'PUT':
        new_user_record = request.get_json()
        return update_user(userid, new_user_record)
    if request.method == 'DELETE':
        return delete_user(userid)

# @app.route('/groups/<groupname>', methods=['GET', 'PUT', 'DELETE'])
# def groups_handler(groupname):
#     if request.method == 'GET':
#         return retrieve_group_members(groupname)
#     if request.method == 'PUT':
#         members = request.get_json()['members']
#         return update_group_membership(groupname, members)
#     if request.method == 'DELETE':
#         return delete_group(groupname)

### User Handlers
def retrieve_user(userid):
    user = User.query.get(userid)
    if user is not None:
        response_obj = jsonify(first_name=user.first_name,
                               last_name=user.last_name,
                               userid=user.userid,
                               groups=map(lambda g: g.name, user.groups))
        return response_obj, 200
    else:
        return 'User does not exist', 404

def update_user(userid, user_record):
    user = User.query.get(userid)
    if user is not None and is_valid(user_record):
        user.first_name = user_record['first_name']
        user.last_name = user_record['last_name']
        # assuming userid doesn't change but update anyways
        user.userid = user_record['userid']
        
        # update new group relationships
        new_group_names = user_record['groups']
        new_groups = []
        for group_name in new_group_names:
            group = Group.query.get(group_name)
            if group is None:
                group = Group(group_name)
            new_groups.append(group)

        # sqlalchemy automatically handles removing old and appending new associations
        # http://docs.sqlalchemy.org/en/rel_1_0/orm/collections.html#custom-collection-implementations
        user.groups = new_groups

        db.session.commit()
        return 'User updated successfully', 200
    else:
        return 'User does not exists or post body is invalid', 404
    
def delete_user(userid):
    user = User.query.get(userid)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return 'User has been deleted from data store', 200
    else:
        return 'User does not exist', 404

# ### Groups Handlers
# def retrieve_group_members(groupname):
#     if groupname in groups:
#         response_obj = jsonify(members=list(groups[groupname]))
#         return response_obj, 200
#     else:
#         return 'Group does not exists', 404

# def update_group_membership(groupname, members):
#     if groupname not in groups:
#         return 'Group does not exists', 404
#     new_memebership = set(members)
#     # find users that are in the old list but not in the new list
#     # and remove groupname from their groups
#     to_remove_from = groups[groupname].difference(new_memebership)
#     for user in to_remove_from:
#         users[user].groups.discard(groupname)

#     # find users that are in the new list but not in the old list 
#     # and add groupname to their groups
#     to_add_to = new_memebership.difference(groups[groupname])
#     for user in to_add_to:
#         users[user].groups.add(groupname)

#     # replace group
#     groups[groupname] = set(members)
#     return 'Group memberships updated', 200

# def delete_group(groupname):
#     if groupname not in groups:
#         return 'Group does not exists', 404

#     # remove group from users' group set
#     for user in groups[groupname]:
#         users[user].groups.discard(groupname)

#     # remove group from groups
#     del groups[groupname]
#     return 'Group deleted', 200


if __name__ == '__main__':
    app.debug = True
    app.run()
