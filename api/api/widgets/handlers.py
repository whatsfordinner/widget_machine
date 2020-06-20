import logging
from prometheus_client import Counter, Histogram, Gauge
from api import db
from api.widgets import utils, exceptions

logger = logging.getLogger(__name__)

def get_widgets() -> list:
    """ Return a list of all widgets in the database.
    
    If there are no widgets, return an empty list.
    """

    try:
        widgets = []
        results = db.get_db().get_widgets()
    
    except db.exceptions.DBError as err:
        logging.error(f'error accessing database: {err}')
        raise exceptions.WidgetError(500, err)

    # the iterable object returned by PugSQL is not a list
    for result in results:
        widgets.append(result)

    return widgets

def get_widget(widget_id: int) -> dict:
    """ Return the widget object with the corresponding integer ID

    If the widget doesn't exist, return a WidgetError with a 404 status code.
    If the ID isn't an integer, return a TypeError.
    If the ID is smaller than 1, return a ValueError.
    """
    
    # check to make sure the widget_id is valid
    if type(widget_id) is not int:
        logger.debug(f'{widget_id} is not an integer')
        raise TypeError('widget_id must be a positive integer greater than zero')

    if widget_id < 1:
        logger.debug(f'{widget_id} is an integer but is smaller than one')
        raise ValueError('widget_id must be a positive integer greater than zero')

    try:
        widget = db.get_db().get_widget_by_id(widget_id=widget_id)
    
    except db.exceptions.DBError as err:
        logging.error(f'error accessing database: {err}')
        raise exceptions.WidgetError(500, err)

    if widget is None:
        raise exceptions.WidgetError(404, f'widget with ID {widget_id} not found')
    else:
        return widget

def new_widget(post_data: dict) -> dict:
    """ Add the widget to the database and return the new widget object

    'quantity' is an optional attribute and should be set to 0 if not included.
    If the POST data is bad, re-raise the WidgetError with a 400 status code.
    If the widget already exists, raise a WidgetError with a 422 status code.
    """

    # validate that the POST data is any good and get the name and quantity from it
    try:
        utils.validate_data('post_widget', post_data)
        new_widget_name = post_data['name']

        if 'quantity' in post_data:
            new_widget_quantity = post_data['quantity']
        else:
            new_widget_quantity = 0

    except exceptions.WidgetError as err:
        # the only error we're going to get is the validation error at this point
        raise err

    # see if a widget with that name already exists
    try:
        if db.get_db().get_widget_by_name(widget_name=new_widget_name) is not None:
            raise exceptions.WidgetError(422, f'widget with name {new_widget_name} already exists')

        # add the new widget to the DB
        logging.debug(f'adding new widget to DB: name: {new_widget_name}, quantity: {new_widget_quantity}')
        db.get_db().insert_widget(widget_name=new_widget_name, widget_quantity=new_widget_quantity)

        return db.get_db().get_widget_by_name(widget_name=new_widget_name)
    
    except db.exceptions.DBError as err:
        logging.error(f'error accessing database: {err}')
        raise exceptions.WidgetError(500, err)

def update_widget(widget_id: int, post_data: dict) -> dict:
    pass

def delete_widget(widget_id: int) -> None:
    pass

