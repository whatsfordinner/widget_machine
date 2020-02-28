import logging
from flask import abort, Blueprint

bp = Blueprint('widgets', __name__, url_prefix='/widgets')

@bp.route('/', methods=['GET'])
def get_widgets():
    logging.debug('incoming request: GET /widgets')
    abort(501)

@bp.route('/', methods=['POST'])
def new_widget():
    logging.debug('incoming request: POST /widgets')
    abort(501)

@bp.route('/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logging.debug(f'incoming request: GET /widgets/{widget_id}')
    abort(501)

@bp.route('/<int:widget_id>', methods=['PUT'])
def update_widget(widget_id):
    logging.debug(f'incoming request: PUT /widgets/{widget_id}')
    abort(501)

    