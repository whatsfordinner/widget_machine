CREATE DATABASE IF NOT EXISTS widgets;

USE widgets;

CREATE TABLE widgets (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    quantity INT DEFAULT 0
);

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
;

CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    widgetid INT NOT NULL,
    quantity INT NOT NULL,
    createdon TIMESTAMP NOT NULL,
    fulfilledon TIMESTAMP,
    FOREIGN KEY (widgetid)
        REFERENCES widgets(id)
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
GRANT ALL ON widgets.* TO 'widgets';

CREATE USER IF NOT EXISTS 'exporter'@'%' IDENTIFIED BY 'password' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter';