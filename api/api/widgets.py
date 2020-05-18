import logging
from flask import abort, Blueprint, request
from api import db

bp = Blueprint('widgets', __name__, url_prefix='/widgets')
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_widgets():
    logger.debug('incoming request: GET /widgets')
    result = get_widgets_from_db()
    return {
        'widgets': result
    }

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logger.debug(f'incoming request: GET /widgets/{widget_id}')
    result = get_widgets_from_db(widget_id=widget_id)

    if len(result) == 0:
        abort(404)
    else:
        return {
            'widget': result[0]
        }

@bp.route('/', methods=['POST'])
def new_widget():
    logger.debug('incoming request: POST /widgets')
    post_data = request.get_json()
    logger.debug(f'new widget POST data: {post_data}')

    if post_data is None or 'widget' not in post_data:
        abort(415)
    
    widget_data = post_data['widget']

    if 'name' not in widget_data:
        abort(415)
    
    # check to see if a widget with that name already exists
    result = get_widgets_from_db(widget_name=widget_data['name'])
    if len(result) != 0:
        abort(422)

    # check to see if a quantity was specified
    if 'quantity' in widget_data:
        quantity = widget_data['quantity']
    else:
        quantity = 0
    
    # widget doesn't exist arleady so let's insert it
    db_conn = db.get_db()
    query = 'INSERT INTO widgets (name, quantity) VALUES (%(widget_name)s, %(widget_quantity)s)'
    params = {
        'widget_name': widget_data['name'],
        'widget_quantity': quantity
    }
    logger.info(f'createing new widget: {params}')
    db_conn.execute_query(query, params)

    # get newly created widget and return it
    result = get_widgets_from_db(widget_name=widget_data['name'])
    return {
        'widget': result[0]
    }

@bp.route('/<int:widget_id>', methods=['PATCH'])
def update_widget(widget_id):
    logger.debug(f'incoming request: PUT /widgets/{widget_id}')
    abort(501)
    
def get_widgets_from_db(
    widget_id=None,
    widget_name=None
):
    # prioritise searching by widget ID
    if widget_id is not None:
        logger.debug(f'querying for widget by ID: {widget_id}')
        query = 'SELECT id, name, quantity FROM widgets WHERE id = %(widget_id)s'
        params = {
            'widget_id': widget_id
        }
        
    # query by widget name
    elif widget_name is not None:
        logger.debug(f'querying for widget by name: {widget_name}')
        query = 'SELECT id, name, quantity FROM widgets WHERE name = %(widget_name)s'
        params = {
            'widget_name': widget_name
        }
    
    # query against all widgets
    else:
        logger.debug('querying for all widgets')
        query = 'SELECT id, name, quantity FROM widgets'
        params = {}

    db_conn = db.get_db()
    result = db_conn.execute_query(query, params)
    logger.debug(f'{len(result)} widgets returned')
    return result
