# expense_engine.py
import json
import os

# Database file to manage volatile-to-permanent state translation
STORAGE_FILE = "expenses_db.json"

def load_ledger():
    """
    Persistence Layer: Hydrates volatile RAM structures with existing historical 
    data saved in permanent storage upon application initialization.
    """
    if not os.path.exists(STORAGE_FILE):
        return {"total_spent": 0.0, "transactions": []}
    
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        # Prevent runtime collapse if file structural integrity is compromised
        return {"total_spent": 0.0, "transactions": []}

def save_ledger(ledger_data):
    """
    Persistence Layer: Flushes current Heap memory tables to disk, protecting 
    state variables against sudden process termination.
    """
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(ledger_data, file, indent=4)
        return True
    except IOError:
        return False

def register_expense(ledger_data, amount_str, category_str):
    """
    Defensive Coding Layer (Digital Poka-Yoke) & Process Layer:
    Performs type-safe conversion, updates the real-time Accumulator state,
    and structures the transaction with a tracking identifier.
    """
    # 1. Type-Safety Check (Transformation Mechanism)
    clean_amount = float(amount_str.strip())
    if clean_amount <= 0:
        raise ValueError("Transaction values must be strictly greater than zero.")
        
    # 2. State Accumulation Logic (total = total + new_value)
    ledger_data["total_spent"] = round(ledger_data["total_spent"] + clean_amount, 2)
    
    # 3. Structural Record Generation
    transaction_id = 1 if not ledger_data["transactions"] else ledger_data["transactions"][-1]["id"] + 1
    new_record = {
        "id": transaction_id,
        "amount": clean_amount,
        "category": category_str.strip() if category_str.strip() else "Uncategorized"
    }
    
    # 4. Insertion into dynamic heap array
    ledger_data["transactions"].append(new_record)
    
    # 5. Commit change to disk
    save_ledger(ledger_data)
    return new_record

def clear_ledger():
    """
    Process Layer: Purges transactional logs and resets numerical accumulators.
    """
    fresh_ledger = {"total_spent": 0.0, "transactions": []}
    save_ledger(fresh_ledger)
    return fresh_ledger