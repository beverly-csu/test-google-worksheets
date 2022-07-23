create_table = """CREATE TABLE IF NOT EXISTS test_data (
    db_id serial NOT NULL PRIMARY KEY,
    order_num INT NOT NULL,
    cost_usd INT NOT NULL,
    cost_rub REAL NOT NULL,
    delivery_time TEXT NOT NULL
);"""

get_tables = """SELECT * FROM pg_catalog.pg_tables 
WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"""

add_item = """INSERT INTO test_data VALUES (%s, %s, %s, %s, %s)"""

drop_table = """DROP TABLE test_data"""
