import logging
from flask import abort, Blueprint

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['GET'])
def get_orders():
    logging.debug('incoming request: GET /orders')
    abort(501)

@bp.route('/', methods=['POST'])
def new_order():
    logging.debug('incoming request: POST /orders')
    abort(501)

@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    logging.debug(f'incoming request: GET /orders/{order_id}')
    abort(501)

@bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    logging.debug(f'incoming request: PUT /orders/{order_id}')
    abort(501)
