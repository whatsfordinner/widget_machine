import logging
from flask import abort, Blueprint, request
from prometheus_client import Counter, Histogram
from api import db
from api.widgets import utils, exceptions

bp = Blueprint('widgets', __name__, url_prefix='/widgets')
logger = logging.getLogger(__name__)
prom_request_timer = Histogram('http_api_duration_seconds', 'latency of requests to the API', ['method', 'endpoint'])

@bp.route('/', methods=['GET'])
def get_widgets():
    with prom_request_timer.labels('get', '/widgets/').time():
        result = []
        for r in db.get_db().get_widgets():
            result.append(r)

        return {
            'widgets': result
        }

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    with prom_request_timer.labels('get', '/widgets/:widget_id').time():
        logger.debug(f'incoming request: GET /widgets/{widget_id}')
        result = db.get_db().get_widget_by_id(widget_id=widget_id)

        if result is None:
            abort(404, description=f'widget with ID {widget_id} not found')
        else:
            return {
                'widget': result
            }

@bp.route('/', methods=['POST'])
def new_widget():
    with prom_request_timer.labels('post', '/widgets/').time():
        logger.debug('incoming request: POST /widgets')
        post_data = request.get_json()

        try:
            utils.validate_data('post_widget', post_data)

            # check to see if a quantity was specified
            if 'quantity' in post_data:
                quantity = post_data['quantity']
            else:
                quantity = 0
        
        except exceptions.WidgetError as err:
            abort(err.status_code, err.message)
        
        # check to see if a widget with that name already exists
        result = db.get_db().get_widget_by_name(widget_name=post_data['name'])
        if result is not None:
            abort(422, f'widget with name \'{post_data["name"]}\' already exists')
        
        # widget doesn't exist arleady so let's insert it
        logger.info(f'creating new widget: {post_data["name"]}')
        new_id = db.get_db().insert_widget(widget_name=post_data['name'], widget_quantity=quantity)

        # get newly created widget by its id and return it
        result = db.get_db().get_widget_by_id(widget_id=new_id)
        return {
            'widget': result
        }

@bp.route('/<int:widget_id>', methods=['PATCH'])
def update_widget(widget_id):
    with prom_request_timer.labels('patch', '/widgets/:widget_id').time():
        logger.debug(f'incoming request: PUT /widgets/{widget_id}')
        abort(501, description='not implemented')

@bp.route('/<int:widget_id>', methods=['DELETE'])
def delete_widget(widget_id):
    with prom_request_timer.labels('delete', '/widgets/:widget_id').time():
        logger.debug(f'incoming request: DELETE /widgets/{widget_id}')
        abort(501, description='not implemented')