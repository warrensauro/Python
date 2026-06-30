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
                amount real NOT NULL,
                is_deleted bool NOT NULL DEFAULT FALSE,
                date_added text DEFAULT CURRENT_TIMESTAMP
              )
    """)
    conn.commit()
    conn.close()

def insert_transaction(description, category, amount):
    conn = connect()
    c = conn.cursor()

    c.execute("Insert into transactions (description, category, amount) values (?,?,?) returning id, description, category, amount, date_added", (description, category, amount))  
    result = c.fetchone()
    conn.commit()
    conn.close()

    return result

def get_all_transactions():
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions where is_deleted = FALSE")
    result = c.fetchall()
    conn.close()

    return result

def get_transaction(id):
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions where id = ? and is_deleted = FALSE", (id,))
    result = c.fetchone()
    conn.close()

    return result

def get_deleted_transactions():
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions where is_deleted = TRUE")
    result = c.fetchall()
    conn.close()

    return result

def get_transactions_by_category(category):
    conn = connect()
    c= conn.cursor()

    c.execute("Select * from transactions where category = ? and is_deleted = FALSE", (category,))
    result = c.fetchall()
    conn.close()

    return result

def get_transactions_by_date_range(start_date, end_date):
    conn = connect()
    c = conn.cursor()

    c.execute("Select * from transactions where date_added between ? and ? and is_deleted = FALSE", (start_date, end_date,))
    result = c.fetchall()
    conn.close()

    return result

def update_transaction(id, description, category, amount):
    conn = connect()
    c = conn.cursor()

    c.execute("Update transactions set description = ?, category = ?, amount = ? where id = ? and is_deleted = FALSE returning id, description, category, amount, date_added", (description, category, amount, id))
    result = c.fetchone()
    conn.commit()
    conn.close()

    return result

def delete_transaction(id):
    conn = connect()
    c = conn.cursor()

    c.execute("Update transactions set is_deleted = TRUE where id = ? and is_deleted = FALSE returning id, description, category, amount, date_added", (id,))
    result = c.fetchone()
    conn.commit()
    conn.close()

    return result

def restore_transaction(id):
    conn = connect()
    c = conn.cursor()

    c.execute("Update transactions set is_deleted = FALSE where id = ? and is_deleted = TRUE returning id, description, category, amount, date_added", (id,))
    result = c.fetchone()
    conn.commit()
    conn.close()

    return result