import logging
from flask import abort, Blueprint
from . import db

bp = Blueprint('widgets', __name__, url_prefix='/widgets')

@bp.route('/', methods=['GET'])
def get_widgets():
    logging.debug('incoming request: GET /widgets')
    db_conn = db.get_db()
    query = 'SELECT widgetid, widgetname FROM widgets'
    result = db_conn.execute_query(query)
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
    db_conn = db.get_db()
    query = 'SELECT widgetid, widgetname FROM widgets WHERE widgetid = %(widgetid)s'
    params = {
        'widgetid': widget_id
    }
    result = db_conn.execute_query(query, params=params)

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

    