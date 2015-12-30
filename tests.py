from flask import json, jsonify
from flask.ext.testing import TestCase
from app.models import User, Group
from app import app, db
import unittest


class Tests(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def inject_users_for_testing(self):
        jsmith = User('jsmith', 'Joe', 'Smith')
        jdoe = User('jdoe', 'John', 'Doe')
        shill = User('shill', 'Sarah', 'Hill')

        group_a = Group('A')
        group_b = Group('B')
        group_c = Group('C')

        jsmith.groups = [group_a, group_b]
        jdoe.groups = [group_b, group_c]
        shill.groups = [group_a, group_c]

        db.session.add(jsmith)
        db.session.add(jdoe)
        db.session.add(shill)
        db.session.commit()

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.inject_users_for_testing()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        # add one more user
        post_body = json.dumps(dict(first_name='David',
                                    last_name='Letterman',
                                    userid='dletterman',
                                    groups=['A', 'B']))
        response = self.client.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # invalid user record
        post_body = json.dumps(dict(first_name='Tony',
                                    userid='tstark'))
        response = self.client.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # posts to an existing user
        post_body = json.dumps(dict(first_name='Joe',
                                    last_name='Smith',
                                    userid='jsmith',
                                    groups=['A', 'B']))
        response = self.client.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_get_user(self):
        # get an existing user
        response = self.client.get('/users/jsmith')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, dict(first_name='Joe',
                                             last_name='Smith',
                                             userid='jsmith',
                                             groups=['A', 'B']))
        # get an non-existing user
        response = self.client.get('/users/tstark')
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        # delete an existing user
        response = self.client.delete('/users/shill')
        self.assertEqual(response.status_code, 200)

        # delete an non-existing user
        response = self.client.delete('/users/pparker')
        self.assertEqual(response.status_code, 404)

    def test_put_user(self):
        # change an existing user
        post_body = json.dumps(dict(first_name='Johnny',
                                    last_name='Doe',
                                    userid='jdoe',
                                    groups=['A', 'B']))
        response = self.client.put('/users/jdoe', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # change an non-existing user
        post_body = json.dumps(dict(first_name='Tony',
                                    last_name='Stark',
                                    userid='tstark',
                                    groups=['D', 'E']))
        response = self.client.put('/users/tstark', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_group(self):
        # get an existing group
        response = self.client.get('/groups/A')

        self.assertEqual(response.status_code, 200)
        members = set(response.json['members'])
        self.assertEqual(members, set(['jsmith', 'shill']))

        # get a non-existing group
        response = self.client.get('/groups/F')
        self.assertEqual(response.status_code, 404)

    def test_post_group(self):
        # post to an existing group
        post_body = json.dumps(dict(name='A'))
        response = self.client.post('/groups', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 409)

        # create a new group
        post_body = json.dumps(dict(name='G'))
        response = self.client.post('/groups', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_groups(self):
        post_body = json.dumps(dict(members=['jsmith', 'jdoe', 'shill']))
        response = self.client.put('/groups/A', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # print(Group.query.get('A').users)
        # self.assertEqual(len(Group.query.get('A').users), 3)

        # put to an non-existing group
        post_body = json.dumps(dict(members=['jsmith', 'jdoe', 'shill']))
        response = self.client.put('/groups/K', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_group(self):
        response = self.client.delete('/groups/A')
        self.assertEqual(response.status_code, 200)

        # delete a non-existing group
        response = self.client.delete('/groups/K')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
