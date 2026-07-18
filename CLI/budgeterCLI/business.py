from database import insert, get_all, get_by_id, get_deleted, get_by_category, get_by_date_range, update, delete, restore

def create_transaction(description, category, amount):
    if not description:
        raise ValueError("Description cannot be empty.")
    if not category:
        raise ValueError("Category is required.")
    if amount is None or amount <= 0:
        raise ValueError("Amount missing or is less than 1.")
    
    return insert(description, category, amount)

def get_all_transactions():
    return get_all()

def get_transaction(id):
    if id is None:
        raise ValueError("Provide transaction ID.")
    result = get_by_id(id)
    if result is None:
        raise ValueError("Transaction not found.")
    
    return result

def get_deleted_transactions():
    return get_deleted()

def get_transactions_by_category(category):
    if not category:
        raise ValueError("Provide category to filter.")
    
    return get_by_category(category)

def get_transactions_by_date_range(start_date, end_date):
    if not start_date:
        raise ValueError("Provide start date to filter.")
    if not end_date:
        raise ValueError("Provide end date to filter.")
    if start_date > end_date:
        raise ValueError( "Invalid date range: End date must be greater than or equal to start date.")
    
    return get_by_date_range(start_date, end_date)

def update_transaction(id, description, category, amount):
    if id is None:
        raise ValueError("Provide transaction ID.")
    if not description:
        raise ValueError("Description cannot be empty.")
    if not category:
        raise ValueError("Category is required")
    if amount is None or amount <= 0:
        raise ValueError("Amount missing or is less than 1.")
    
    result = update(id, description, category, amount)
    if result is None:
        raise ValueError("Transaction not found.")
    
    return result

def delete_transaction(id):
    if id is None:
        raise ValueError("Provide transaction ID.")
    
    result = delete(id)
    if result is None:
        raise ValueError("Transaction not found.")
    
    return result

def restore_transaction(id):
    if id is None:
        raise ValueError("Provide transaction ID.")
    
    result = restore(id)
    if result is None:
        raise ValueError("Transaction not found.")
    
    return result