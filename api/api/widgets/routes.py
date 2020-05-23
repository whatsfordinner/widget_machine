import logging
from flask import abort, Blueprint, request
from api import db
from api.widgets import utils

bp = Blueprint('widgets', __name__, url_prefix='/widgets')
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_widgets():
    logger.debug('incoming request: GET /widgets')
    result = []
    for r in db.get_db().get_widgets():
        result.append(r)
    return {
        'widgets': result
    }

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logger.debug(f'incoming request: GET /widgets/{widget_id}')
    result = db.get_db().get_widget_by_id(widget_id=widget_id)

    if len(result) == 0:
        abort(404, description=f'widget with ID {widget_id} not found')
    else:
        return {
            'widget': result
        }

@bp.route('/', methods=['POST'])
def new_widget():
    logger.debug('incoming request: POST /widgets')
    post_data = request.get_json()
    logger.debug(f'new widget POST data: {post_data}')

    if post_data is None or 'widget' not in post_data:
        abort(422, description='data object did not contain \'widget\' object')
    
    widget_data = post_data['widget']

    # make sure a name has been specified and it's a string
    if 'name' not in widget_data:
        abort(400, description='\'widget\' object did not have \'name\' attribute')

    if not isinstance(widget_data['name'], str):
        abort(422, 'widget name must be string')

    # check to see if a quantity was specified
    if 'quantity' in widget_data:
        # is the specified quantity an integer
        if not isinstance(widget_data['quantity'], int):
            abort(422, 'quantity must be integer')
        quantity = widget_data['quantity']
    else:
        quantity = 0
    
    # check to see if a widget with that name already exists
    result = db.get_db().get_widget_by_name(widget_name=widget_data['name'])
    if result is not None:
        abort(422, f'widget with name \'{widget_data["name"]}\' already exists')

    
    # widget doesn't exist arleady so let's insert it
    new_id = db.get_db().insert_widget(widget_name=widget_data['name'], widget_quantity=quantity)

    # get newly created widget and return it
    result = db.get_db().get_widget_by_id(widget_id=new_id)
    return {
        'widget': result
    }

@bp.route('/<int:widget_id>', methods=['PATCH'])
def update_widget(widget_id):
    logger.debug(f'incoming request: PUT /widgets/{widget_id}')
    abort(501, description='not implemented')
