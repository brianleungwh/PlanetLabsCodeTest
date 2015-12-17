from flask import json, jsonify
import server
import unittest

class ServerTests(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

        # add users


        print('setup')

    def tearDown(self):
        pass

    def test_create_user(self):
        post_body = json.dumps(dict(first_name='Steve',
                                    last_name='Rogers',
                                    userid='srogers',
                                    groups=['superheroes', 'leaders', 'avengers']))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_body = json.dumps(dict(first_name='Peter',
                                    last_name='Parker',
                                    userid='pparker',
                                    groups=['superheroes']))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_body = json.dumps(dict(first_name='Tony',
                                    last_name='Stark',
                                    userid='tstark',
                                    groups=['superheroes', 'avengers', 'CEOs']))
        response = self.app.post('/users', data=post_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        post_body = json.dumps(dict(first_name='Bruce',
                                    last_name='Banner',
                                    userid='bbanner',
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
        response = self.app.get('/users/pparker')
        res_body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_body['first_name'], 'Peter')

        response = self.app.get('/users/jsmith')
        self.assertEqual(response.status_code, 404)

    # def test_delete_user(self):
    #     response = self.app.delete('/users/pparker')
    #     self.assertEqual(response.status_code, 200)

        # response = self.app.delete('/users/pparker')
        # self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
