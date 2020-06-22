import logging
import json
import jsonschema
from api import db
from api.widgets.exceptions import WidgetError

logger = logging.getLogger(__name__)

def get_schema(schema_name: str) -> dict:
    schema_file_location = f'api/widgets/schemas/{schema_name}.json'
    logger.debug(f'reading in schema file: {schema_file_location}')
    with open(schema_file_location) as schema_file:
        schema_json = json.load(schema_file)
    
    return schema_json

def validate_data(schema_name: str, request_data: dict) -> None:
    schema = get_schema(schema_name)
    try:
        jsonschema.validate(request_data, schema)
    except jsonschema.ValidationError as err:
        raise WidgetError(400, err.message)

def validate_widget_name(widget_name: str) -> None:
    """ Validates that the provided widget name is unique.

    Raises a WidgetError exception if the name is not unique.
    Return None if the name is unique.
    Will be extended if other naming requirements emerge.
    """

    if db.get_db().get_widget_by_name(widget_name=widget_name) is not None:
        raise WidgetError(422, f'a widget with the name {widget_name} already exists') 