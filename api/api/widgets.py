import logging
from flask import abort, Blueprint
from api import db

bp = Blueprint('widgets', __name__, url_prefix='/widgets')

@bp.route('/', methods=['GET'])
def get_widgets():
    logging.debug('incoming request: GET /widgets')
    result = get_widgets_from_db()
    return {
        'widgets': result
    }

@bp.route('/', methods=['POST'])
def new_widget():
    logging.debug('incoming request: POST /widgets')
    abort(501)

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logging.debug(f'incoming request: GET /widgets/{widget_id}')
    result = get_widgets_from_db(widget_id=widget_id)

    if len(result) == 0:
        abort(404)
    else:
        return {
            'widget': result[0]
        }

@bp.route('/<int:widget_id>', methods=['PUT'])
def update_widget(widget_id):
    logging.debug(f'incoming request: PUT /widgets/{widget_id}')
    abort(501)
    
def get_widgets_from_db(
    widget_id=None,
    widget_name=None
):
    # prioritise searching by widget ID
    if widget_id is not None:
        logging.debug(f'querying for widget by ID: {widget_id}')
        query = 'SELECT id, name, quantity FROM widgets WHERE id = %(widget_id)s'
        params = {
            'widget_id': widget_id
        }
        
    # query by widget name
    elif widget_name is not None:
        logging.debug(f'querying for widget by name: {widget_id}')
        query = 'SELECT id, name, quantity FROM widgets WHERE name = %(widget_name)s'
        params = {
            'widget_name': widget_name
        }
    
    # query against all widgets
    else:
        logging.debug('querying for all widgets')
        query = 'SELECT id, name, quantity FROM widgets'
        params = {}

    db_conn = db.get_db()
    result = db_conn.execute_query(query, params)
    return result
