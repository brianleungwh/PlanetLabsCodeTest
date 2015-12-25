from flask import json, jsonify
import server
import unittest

class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

        # add users
        post_body = json.dumps(dict(first_name='Steve',
                                    last_name='Rogers',
                                    userid='srogers',
                                    groups=['superheroes', 'leaders', 'avengers']))
        self.app.post('/users', data=post_body, content_type='application/json')

        post_body = json.dumps(dict(first_name='Peter',
                                    last_name='Parker',
                                    userid='pparker',
                                    groups=['superheroes']))
        self.app.post('/users', data=post_body, content_type='application/json')

        post_body = json.dumps(dict(first_name='Tony',
                                    last_name='Stark',
                                    userid='tstark',
                                    groups=['superheroes', 'avengers', 'CEOs']))
        self.app.post('/users', data=post_body, content_type='application/json')

        post_body = json.dumps(dict(first_name='Bruce',
                                    last_name='Banner',
                                    userid='bbanner',
                                    groups=['superheroes', 'avengers']))
        self.app.post('/users', data=post_body, content_type='application/json')

    def tearDown(self):
        pass

    def test_create_user(self):
        # add one more user
        post_body = json.dumps(dict(first_name='Natasha',
                                    last_name='Romanoff',
                                    userid='nromanoff',
                                    groups=['superheroes', 'avengers']))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # invalid user record
        post_body = json.dumps(dict(first_name='Tony',
                                    userid='tstark'))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # posts to an existing user
        post_body = json.dumps(dict(first_name='Peter',
                                    last_name='Parker',
                                    userid='pparker',
                                    groups=['admins', 'users']))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_get_user(self):
        # get an existing user
        response = self.app.get('/users/pparker')
        res_body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_body['first_name'], 'Peter')

        # get an non-existing user
        response = self.app.get('/users/jsmith')
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        # delete an existing user
        response = self.app.delete('/users/pparker')
        self.assertEqual(response.status_code, 200)

        # delete an non-existing user (just deleted)
        response = self.app.delete('/users/pparker')
        self.assertEqual(response.status_code, 404)

    def test_put_user(self):
        # change an existing user
        post_body = json.dumps(dict(first_name='Captain',
                                    last_name='America',
                                    userid='srogers',
                                    groups=['superheroes', 'leaders', 'avengers']))
        response = self.app.put('/users/srogers', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # change an non-existing user
        post_body = json.dumps(dict(first_name='Joe',
                                    last_name='Smith',
                                    userid='jsmith',
                                    groups=['admins', 'users']))
        response = self.app.put('/users/jsmith', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_group(self):
        # get an existing group
        response = self.app.get('/groups/avengers')
        res_body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(isinstance(res_body['members'], list), True)

        # get a non-existing group
        response = self.app.get('/groups/admins')
        self.assertEqual(response.status_code, 404)

    def test_post_group(self):
        # post to an existing group
        post_body = json.dumps(dict(name='avengers'))
        response = self.app.post('/groups', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 409)

        # create a new group
        post_body = json.dumps(dict(name='humans'))
        response = self.app.post('/groups', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_put_groups(self):
        # avengers: srogers, tstark, bbanner, nromanoff
        post_body = json.dumps(dict(members=['srogers', 'bbanner', 'nromanoff'])) # remove ironman from avengers
        response = self.app.put('/groups/avengers', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        response = self.app.delete('/groups/superheroes')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
