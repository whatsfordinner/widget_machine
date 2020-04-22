CREATE DATABASE IF NOT EXISTS widgets;

USE widgets;

CREATE TABLE widgets (
    widgetid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    widgetname VARCHAR(20) NOT NULL
);

INSERT INTO widgets (widgetname) VALUES
    ('fizzbotter'),
    ('woozle'),
    ('gewgaw'),
    ('trinket')
;

CREATE TABLE orders (
    orderid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    widgetid INT NOT NULL,
    quantity INT NOT NULL,
    createdon TIMESTAMP NOT NULL,
    fulfilledon TIMESTAMP,
    FOREIGN KEY (widgetid)
        REFERENCES widgets(widgetid)
);

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
;

CREATE USER IF NOT EXISTS 'widgets'@'%' IDENTIFIED BY 'password';

GRANT ALL ON widgets.* TO 'widgets'