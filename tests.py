#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app import app
from flask.json import jsonify

class IntergrationTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)

    # testing functions

    def test_homepage(self):
        """Should be able to get the homepage."""
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_default_redirecting(self):
        rv = self.app.get('/auth/agiliq')
        self.assertEqual(rv.status_code, 301)

    def test_not_allowed_upload(self):
        rv = self.app.get('/upload/')
        self.assertEqual(rv.status_code, 401)

    def test_not_allowed_callback(self):
        rv = self.app.get('/callback/agiliq/')
        self.assertEqual(rv.status_code, 401)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_logout(self):
        rv = self.logout()
        self.assertIn('Login', rv.data)

if __name__ == '__main__':
    unittest.main()
