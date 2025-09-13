DROP TABLE IF EXISTS users;

CREATE TABLE users
(   
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

INSERT INTO users (user_id, password)
VALUES
    ('aoife','password');



DROP TABLE IF EXISTS items;

CREATE TABLE items
(   
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    image TEXT NOT NULL 
);

INSERT INTO items (name, price, type, description, image)
VALUES
    ('Black Leather Jacket', 30, 'Jacket', 'black', 'blackLjacket.jpg'),
    ('Blue Denim Jacket', 28, 'Jacket', 'Blue rustic denim jacket', 'bluedjacket.jpg'),
    ('Green dress', 12.99, 'Dress', 'red', 'greendress.jpg'),
    ('red tshirt', 12.99, '', 'T-shirt', 'redtshirt.jpg'),
    ('Pink Tshirt', 12.99, 'T-shirt', 'Loose Pink tshirt', 'pinktshirt.jpg'),
    ('Grey Jeans', 21.50, 'Jeans', 'Dark grey low rise jeans', 'greyjeans.jpg');


DROP TABLE IF EXISTS selling;

CREATE TABLE selling
(   
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    image TEXT NOT NULL DEFAULT "default.jpeg"
);

INSERT INTO selling (name, price, type, description)
VALUES
    ('top', 12.99, 'Top', 'black'),
    ('Blue Denim Jacket', 28, 'Jacket', 'Blue rustic denim jacket'),
    ('dress', 12.99, 'Dress', 'red'),
    ('tshirt', 12.99, 'top', 'green'),
    ('Pink Tshirt', 12.99, 'T-shirt', 'Loose Pink tshirt'),
    ('Grey Jeans', 21.50, 'Jeans', 'Dark grey low rise jeans');
