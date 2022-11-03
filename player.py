import sqltools
import config
from constants import *
import time

def init_player(id):
    if sqltools.cursor.execute("SELECT * FROM users WHERE id = (?)", (id,)).fetchone() is None:
        sqltools.cursor.execute("INSERT INTO users(id) VALUES(?)", (id,))


def get_player(id):
    init_player(id)
    p = list(sqltools.cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone())
    for c, i in enumerate(p):
        if type(i) == bytes:
            p[c] = sqltools.deserialize(p[c])
    update_player(p)
    return p


def set_player(p):
    init_player(p[0])
    # p[INVENTORY] = [random.randint(1, 100) for _ in p[INVENTORY]]
    for c, i in enumerate(sqltools.users_columns):
        sqltools.cursor.execute(f"UPDATE users SET {i} = (?) WHERE id = {p[0]}", (p[c],))
    sqltools.conn.commit()


def update_player(p):
    for i in config.deleted_items:
        p[INVENTORY][i] = 0
    while len(p[INVENTORY]) < config.inventory_size:
        p[INVENTORY].append(0)
    for i in p[TO_ADD][::-1]:
        if i[0] < time.time():
            for j in i[1]:
                p[INVENTORY][j[0]] += j[1]
            p[TO_ADD].remove(i)
    while len(p[SETTINGS]) < config.settings_size:
        p[SETTINGS].append(config.default_settings[len(p[SETTINGS])])
