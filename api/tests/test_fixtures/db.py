import pugsql

def purge_db():
    db = pugsql.module('tests/test_fixtures/queries')
    db.connect('mysql+pymysql://widgets:password@localhost/widgets')
    db.purge_orders()
    db.purge_widgets()
    db.disconnect()

def populate_db():
    db = pugsql.module('tests/test_fixtures/queries')
    db.connect('mysql+pymysql://widgets:password@localhost/widgets')
    db.add_widgets()
    db.add_orders()
    db.populate_widgets()
    db.populate_orders()
    db.disconnect()
