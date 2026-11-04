import sqlite3

def db_init():

    conn = sqlite3.connect('database.db')
    with open("schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print('Banco de dados inicializado com sucesso!')


db_init()