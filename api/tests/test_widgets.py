import unittest
from unittest.mock import MagicMock, patch
from api import widgets, db

@patch('api.widgets.get_widgets_from_db')
class GetWidgetsTestCase(unittest.TestCase):
    def test_get_widgets(self, mock_db):
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

        mock_db.return_value = db_return
        result = widgets.get_widgets()
        self.assertDictEqual(result, expect)
    
@patch('api.widgets.abort')
@patch('api.widgets.get_widgets_from_db')
class GetWidgetTestCase(unittest.TestCase):
    def test_widget_exists(self, mock_db, mock_abort):
        db_return = [
            {
                'id': 1,
                'name': 'foo',
                'quantity': 3
            }
        ]

        expect = {
            'widget': db_return[0]
        }

        mock_db.return_value = db_return
        result = widgets.get_widget(1)
        self.assertDictEqual(result, expect)

    def test_widget_nonexistent(self, mock_db, mock_abort):
        db_return = []
        mock_db.return_value.execute_query.return_value = db_return
        result = widgets.get_widget(1)
        self.assertIsNone(result)
        mock_abort.assert_called_with(404)
