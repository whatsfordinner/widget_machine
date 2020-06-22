import logging
from flask import abort, Blueprint, request
from prometheus_client import Counter, Histogram
from api import db
from api.widgets import utils, exceptions, handlers

bp = Blueprint('widgets', __name__, url_prefix='/widgets')
logger = logging.getLogger(__name__)
prom_request_timer = Histogram('api_http_duration_seconds', 'latency of requests to the API', ['method', 'endpoint'])

@bp.route('/', methods=['GET'])
def get_widgets():
    with prom_request_timer.labels('get', '/widgets/').time():
        logger.debug('incoming request: GET /widgets/')
        return {
            'widgets': handlers.get_widgets()
        }

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    with prom_request_timer.labels('get', '/widgets/:widget_id').time():
        logger.debug(f'incoming request: GET /widgets/{widget_id}')

        try:
            return {
                'widget': handlers.get_widget(widget_id)
            }
        
        except exceptions.WidgetError as err:
            abort(err.status_code, description=err.message)

        except Exception as err:
            abort(500, description=err)


@bp.route('/', methods=['POST'])
def new_widget():
    with prom_request_timer.labels('post', '/widgets/').time():
        logger.debug('incoming request: POST /widgets')
        request_data = request.get_json()

        try:
            return {
                'widget': handlers.new_widget(request_data)
            }
        
        except exceptions.WidgetError as err:
            abort(err.status_code, err.message)

@bp.route('/<int:widget_id>', methods=['PATCH'])
def update_widget(widget_id):
    with prom_request_timer.labels('patch', '/widgets/:widget_id').time():
        logger.debug(f'incoming request: PUT /widgets/{widget_id}')
        request_data = request.get_json()

        try:
            return {
                'widget': handlers.update_widget(widget_id, request_data)
            }
        
        except exceptions.WidgetError as err:
            abort(err.status_code, err.message)
