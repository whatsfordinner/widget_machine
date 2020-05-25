import unittest
from unittest.mock import MagicMock, patch
from api import db

class MockDB:
    def __init__(self, return_value):
        self.return_value = return_value
    
    def get_widgets(self):
        return self.return_value

    def get_widget_by_id(self, **kwargs):
        return self.return_value

@patch('api.db.get_db')
class GetWidgetsTestCase(unittest.TestCase):

    def test_get_widgets(self, mock_db):
        from api.widgets.routes import get_widgets
        db_return = [
            {
                'id': 1,
                'name': 'foo',
                'quantity': 1
            },
            {
                'id': 2,
                'name': 'bar',
                'quantity': 2
            }
        ]

        expect = {
            'widgets': db_return
        }

        mock_db.return_value = MockDB(db_return)
        result = get_widgets()
        self.assertDictEqual(result, expect)
    
@patch('api.widgets.routes.abort')
@patch('api.db.get_db')
class GetWidgetTestCase(unittest.TestCase):
    def test_widget_exists(self, mock_db, mock_abort):
        from api.widgets.routes import get_widget
        db_return = {
            'id': 1,
            'name': 'foo',
            'quantity': 3
        }

        expect = {
            'widget': db_return
        }

        mock_db.return_value = MockDB(db_return)
        result = get_widget(1)
        self.assertDictEqual(result, expect)

    def test_widget_nonexistent(self, mock_db, mock_abort):
        from api.widgets.routes import get_widget
        db_return = []
        mock_db.return_value = MockDB(db_return)
        result = get_widget(1)
        self.assertIsNone(result)
        mock_abort.assert_called_with(404, description='widget with ID 1 not found')

class NewWidgetTestCase(unittest.TestCase):
    def test_no_widget_data(self):
        self.assertTrue(False)

    def test_malformed_widget_data(self):
        self.assertTrue(False)

    def test_widget_already_exists(self):
        self.assertTrue(False)

    def test_create_widget(self):
        self.assertTrue(False)