from database import insert_transaction

def create_transaction(description, category, amount):
    if not description:
        raise ValueError("Description cannot be empty.")
    if not category:
        raise ValueError("Category cannot be None.")
    if not amount or amount <= 0:
        raise ValueError("Amount missing or is less than 1")
    
    return insert_transaction(description, category, amount)
    