import logging
from flask import abort, Blueprint, request
from prometheus_client import Counter, Summary
from api import db
from api.widgets import utils, exceptions

bp = Blueprint('widgets', __name__, url_prefix='/widgets')
logger = logging.getLogger(__name__)
prom_request_counter = Counter('http_api_requests', 'API Requests', ['method', 'endpoint'])
prom_request_timer = Summary('http_api_requests_latency_seconds', 'Latency of requests to the API', ['method', 'endpoint'])

@prom_request_timer.time('get', '/widgets/')
@bp.route('/', methods=['GET'])
def get_widgets():
    logger.debug('incoming request: GET /widgets')
    result = []
    for r in db.get_db().get_widgets():
        result.append(r)

    prom_request_counter.labels('get', '/widgets/').inc()
    return {
        'widgets': result
    }

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logger.debug(f'incoming request: GET /widgets/{widget_id}')
    result = db.get_db().get_widget_by_id(widget_id=widget_id)

    if result is None:
        abort(404, description=f'widget with ID {widget_id} not found')
    else:
        prom_request_counter.labels('get', '/widget/:widget_id').inc()
        return {
            'widget': result
        }

@bp.route('/', methods=['POST'])
def new_widget():
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
    new_id = db.get_db().insert_widget(widget_name=post_data['name'], widget_quantity=quantity)

    # get newly created widget by its id and return it
    result = db.get_db().get_widget_by_id(widget_id=new_id)
    prom_request_counter.labels('post', '/widgets/').inc()
    return {
        'widget': result
    }

@bp.route('/<int:widget_id>', methods=['PATCH'])
def update_widget(widget_id):
    logger.debug(f'incoming request: PUT /widgets/{widget_id}')
    abort(501, description='not implemented')
