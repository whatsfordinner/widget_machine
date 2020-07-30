-- :name add_widgets
CREATE TABLE widgets (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    quantity INT DEFAULT 0
)

-- :name add_orders
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    widgetid INT NOT NULL,
    quantity INT NOT NULL,
    createdon TIMESTAMP NOT NULL,
    fulfilledon TIMESTAMP,
    FOREIGN KEY (widgetid)
        REFERENCES widgets(id)
)

-- :name populate_widgets
INSERT INTO widgets (
    name,
    quantity
) VALUES
    (
        'fizzbotter',
        2
    ),
    (
        'woozle',
        5
    ),
    (
        'gewgaw',
        1
    ),
    (
        'trinket',
        0
    )

-- :name populate_orders
INSERT INTO orders (
    widgetid,
    quantity,
    createdon,
    fulfilledon
) VALUES
    (
        1,
        10,
        '2020-02-05 10:05:00',
        NULL
    ),
    (
        2,
        3,
        '2020-04-10 23:49:15',
        '2020-04-11 03:15:00'
    )