import logging
import json
import jsonschema
from api.widgets.exceptions import WidgetError

logger = logging.getLogger(__name__)

def get_schema(schema_name):
    schema_file_location = f'api/widgets/schemas/{schema_name}.json'
    logging.debug(f'reading in schema file: {schema_file_location}')
    with open(schema_file_location) as schema_file:
        schema_json = json.load(schema_file)
    
    return schema_json

def validate_data(schema_name, post_data):
    schema = get_schema(schema_name)
    try:
        jsonschema.validate(post_data, schema)
    except jsonschema.ValidationError as err:
        raise WidgetError(400, err.message)