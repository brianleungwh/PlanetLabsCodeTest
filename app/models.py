from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Group(db.Model):
    name = db.Column(db.String(30), primary_key=True)

    def __init__(self, name):
        self.name = name
