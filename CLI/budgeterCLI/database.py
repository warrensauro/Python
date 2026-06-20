import sqlite3

def create_table():
    conn = sqlite3.connect('transaction.db')
    c = conn.cursor()
    
    c.execute(""" Create table if not exists transactions (
                id integer PRIMARY KEY,
                description text,
                category text,
                amount real
              )
    """)
    conn.commit()
    conn.close()
