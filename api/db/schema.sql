DROP Table IF EXISTS items;
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY NOT NULL,
    site TEXT NOT NULL,
    price DECIMAL,
    start_time TIMESTAMP WITHOUT TIME ZONE,
    name TEXT,
    description TEXT,
    seller_id INTEGER
);