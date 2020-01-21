from flask import Flask
import logging

app = Flask(__name__)

@app.route('/widgets', methods=['GET'])
def get_widgets():
    logging.debug('incoming request: GET /widgets')
    return 'widgets'

@app.route('/widgets/<int:widget_id>', methods=['GET'])
def get_widget(widget_id):
    logging.debug(f'incoming request: GET /widgets/{widget_id}')
    return f'widget {widget_id}'

@app.route('/widgets/<int:widget_id>', methods=['PUT'])
def update_widget(widget_id):
    logging.debug(f'incoming request: PUT /widgets/{widget_id}')
    return f'update widget {widget_id}'

@app.route('/orders', methods=['GET'])
def get_orders():
    logging.debug('incoming request: GET /orders')
    return 'orders'

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    logging.debug(f'incoming request: GET /orders/{order_id}')
    return f'order {order_id}'

@app.route('/orders', methods=['POST'])
def new_order():
    logging.debug('incoming request: POST /orders')
    return 'new order'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
