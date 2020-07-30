import logging
import os
import unittest
import api
from tests.test_fixtures import db


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = api.create_app().test_client()
        db.purge_db()
        db.populate_db()

    def tearDown(self):
        pass

    def test_get_widgets(self):
        expect = {
            'widgets': [
                {
                    'id': 1,
                    'name': 'fizzbotter',
                    'quantity': 2
                },
                {
                    'id': 2,
                    'name': 'woozle',
                    'quantity': 5
                },
                {
                    'id': 3,
                    'name': 'gewgaw',
                    'quantity': 1
                },
                {
                    'id': 4,
                    'name': 'trinket',
                    'quantity': 0
                }
            ]
        }

        result = self.app.get('/widgets/')
        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())
    
    def test_get_existing_widget(self):
        expect = {
            'widget': {
                'id': 2,
                'name': 'woozle',
                'quantity': 5
            }
        }

        result = self.app.get('/widgets/2')
        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_nonexistent_widget(self):
        result = self.app.get('/widgets/20')
        self.assertEqual(404, result.status_code)

    def test_create_widget(self):
        expect = {
            'widget': {
                'id': 5,
                'name': 'geewhiz',
                'quantity': 5
            }
        }

        result = self.app.post(
            '/widgets/',
            json = {
                'name': 'geewhiz',
                'quantity': 5
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_create_widget_without_quantity(self):
        expect = {
            'widget': {
                'id': 5,
                'name': 'geewhiz',
                'quantity': 0
            }
        }

        result = self.app.post(
            '/widgets/',
            json = {
                'name': 'geewhiz'
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_create_widget_with_existing_name(self):
        result = self.app.post(
            '/widgets/',
            json = {
                'name': 'fizzbotter'
            }
        )

        self.assertEqual(422, result.status_code)

    def test_update_existing_widget_quantity(self):
        expect = {
            'widget': {
                'id': 1,
                'name': 'fizzbotter',
                'quantity': 6
            }
        }

        result = self.app.patch(
            '/widgets/1',
            json = {
                'quantity': 6
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_update_existing_widget_name(self):
        expect = {
            'widget': {
                'id': 1,
                'name': 'finglonger',
                'quantity': 2
            }
        }

        result = self.app.patch(
            '/widgets/1',
            json = {
                'name': 'finglonger'
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_update_nonexistent_widget(self):
        result = self.app.patch(
            '/widgets/20',
            json = {
                'name': 'finglonger'
            }
        )

        self.assertEqual(404, result.status_code)