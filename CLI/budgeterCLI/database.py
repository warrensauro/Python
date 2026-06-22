import sqlite3

def connect():
    conn = sqlite3.connect('transaction.db')
    return conn

def create_table():
    conn = connect()
    c = conn.cursor()
    
    c.execute("""Create table if not exists transactions (
                id integer PRIMARY KEY,
                description text NOT NULL,
                category text NOT NULL,
                amount real NOT NULL
              )
    """)
    conn.commit()
    conn.close()

def insert_transaction(description, category, amount):
    conn = connect()
    c = conn.cursor()

    c.execute("Insert into transactions (description, category, amount) values (?,?,?)", (description, category, amount))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions")
    result = c.fetchall()
    conn.close()

    return result

def get_transaction(id):
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions where id = ?", (id,))
    result = c.fetchone()
    conn.close()

    return result

def update_transaction(id, description, category, amount):
    conn = connect()
    c = conn.cursor()

    c.execute("Update transactions set description = ?, category = ?, amount = ? where id = ?", (description, category, amount, id))
    
    conn.commit()
    conn.close()