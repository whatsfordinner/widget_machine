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

def new_widget(request_data: dict) -> dict:
    """ Add the widget to the database and return the new widget object

    'quantity' is an optional attribute and should be set to 0 if not included.
    If the POST data is bad, re-raise the WidgetError with a 400 status code.
    If the widget already exists, raise a WidgetError with a 422 status code.
    """

    # validate that the POST data is any good and get the name and quantity from it
    try:
        utils.validate_data('post_widget', request_data)
        new_widget_name = request_data['name']

        if 'quantity' in request_data:
            new_widget_quantity = request_data['quantity']
        else:
            new_widget_quantity = 0

    except exceptions.WidgetError as err:
        # the only error we're going to get is the validation error at this point
        raise err

    # see if a widget with that name already exists
    try:
        utils.validate_widget_name(new_widget_name)

        # add the new widget to the DB
        logger.debug(f'adding new widget: name: {new_widget_name}, quantity: {new_widget_quantity}')
        db.get_db().insert_widget(widget_name=new_widget_name, widget_quantity=new_widget_quantity)

        return db.get_db().get_widget_by_name(widget_name=new_widget_name)
    
    except db.exceptions.DBError as err:
        logging.error(f'error accessing database: {err}')
        raise exceptions.WidgetError(500, err)

def update_widget(widget_id: int, request_data: dict) -> dict:
    """ Update an existing widget with the new information provided.

    If the data is bad, re-raise the WidgetError with a 400 status code.
    If the widget doesn't exist, re-raise a WidgetError with a 404 status code.
    """
    
    try:
        utils.validate_data('patch_widget', request_data)
        widget = get_widget(widget_id)

        # if we're updating the name, we want to make sure a widget with that name doesn't
        # already exist
        if 'name' in request_data and request_data['name'] != widget['name']:
            utils.validate_widget_name(request_data['name'])

        for attribute in request_data.keys():
            logger.debug(f'widget ID: {widget_id}. Updating {attribute} to be {request_data[attribute]}')
            widget[attribute] = request_data[attribute]

        logger.debug(f'updating widget with ID {widget_id}')
        affected_widgets = db.get_db().update_widget(
            widget_id=widget_id,
            widget_name=widget['name'],
            widget_quantity=widget['quantity']
        )

        if affected_widgets == 0:
            logger.debug(f'tried to update widget with ID {widget_id} but it does not exist')
            raise exceptions.WidgetError(404, f'widget with ID {widget_id} not found')
        else:
            return get_widget(widget_id)

    except db.exceptions.DBError as err:
        logging.error(f'error accessing database: {err}')
        raise exceptions.WidgetError(500, err)
