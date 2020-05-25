import unittest
from unittest.mock import MagicMock, patch

class GetSchemaTestCase(unittest.TestCase):
    pass

@patch('api.widgets.utils.get_schema')
class ValidateDataTestCase(unittest.TestCase):
    test_schema = {
        'type': 'object',
        'properties': {
            'foo': {
                'type': 'string'
            }
        },
        'required': [
            'foo'
        ]
    }

    valid_object = {
        'foo': 'bar'
    }

    invalid_object = {
        'foo': 5
    }

    def test_valid_object(self, mock_schema):
        from api.widgets.utils import validate_data

        mock_schema.return_value = self.test_schema

        # validate_data() returns None if the object meets the schema
        self.assertIsNone(validate_data('test_schema', self.valid_object))

    def test_invalid_object(self, mock_schema):
        from api.widgets.utils import validate_data
        from api.widgets.exceptions import WidgetError

        mock_schema.return_value = self.test_schema

        with self.assertRaises(WidgetError):
            validate_data('test_schema', self.invalid_object)