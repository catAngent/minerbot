import pickle
import sqlite3
import config

def serialize(obj):
    return pickle.dumps(obj)


def deserialize(blob):
    return pickle.loads(blob)


users_columns = ["id"]

sqlite3.register_adapter(tuple, serialize)
sqlite3.register_converter("tuple", deserialize)

sqlite3.register_adapter(list, serialize)
sqlite3.register_converter("list", deserialize)

sqlite3.register_adapter(dict, serialize)
sqlite3.register_converter("dict", deserialize)

conn = sqlite3.connect("db.db")
cursor = conn.cursor()
cursor.execute("VACUUM")
cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY)")

if config.debug:
    conn.set_trace_callback(print)
    
def add_columns(table, columns):
    for column in columns:
        users_columns.append(column[0])
        try:
            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN {column[0]} {column[1]} NOT NULL default X'{serialize(column[2]).hex()}'")
            conn.commit()
        except Exception:
            ...


