# main.py
from expense_engine import load_ledger, register_expense, clear_ledger

def print_summary(ledger_data):
    """
    Display Layer: Loops through row vectors using standard Iterator Protocol 
    and presents data tracking calculations cleanly.
    """
    print("\n" + "="*50)
    print(f" {'DECODELABS FINANCIAL SUMMARY':^46} ")
    print("="*50)
    print(f" AGGREGATE TOTAL SPENT: ${ledger_data['total_spent']:.2f}")
    print("-"*50)
    print(f"{'TXN ID':<8} | {'AMOUNT':<12} | {'CATEGORY':<22}")
    print("-"*50)
    
    if not ledger_data["transactions"]:
        print(f" {'[No transaction entries found in ledger]':^46}")
    else:
        for txn in ledger_data["transactions"]:
            print(f"{txn['id']:<8} | ${txn['amount']:<11.2f} | {txn['category']:<22}")
            
    print("="*50)

def main():
    print("====================================================")
    print(" DECODELABS EXPENSE TRACKING ENGINE v2.0 - ONLINE   ")
    print("====================================================")
    
    # Initialize state from permanent memory layer
    current_ledger = load_ledger()
    
    while True:
        print("\n[1] View Statement Summary (Display Layer)")
        print("[2] Log Real-Time Transaction (Poka-Yoke Entry)")
        print("[3] Flush Ledger Database (Reset State)")
        print("[4] Terminate Session Interface")
        
        user_intent = input("\nSelect system execution parameter (1-4): ").strip()
        
        if user_intent == "1":
            print_summary(current_ledger)
            
        elif user_intent == "2":
            raw_amount = input("Enter operational expense amount ($): ")
            raw_category = input("Enter transaction classification category: ")
            
            # Implementation of the Defensive Coding / Error-Proofing Barrier
            try:
                logged_record = register_expense(current_ledger, raw_amount, raw_category)
                print(f" -> TRANSACTION VERIFIED: Logged ${logged_record['amount']:.2f} under '{logged_record['category']}'")
            except ValueError as error_message:
                print(f"\n [DIGITAL BARRIER BLOCKED INPUT]: {error_message}")
                print(" -> Logic protection active. Non-numeric or invalid fields rejected.")
                
        elif user_intent == "3":
            confirmation = input("Are you sure you want to completely clear the ledger? (y/n): ").strip().lower()
            if confirmation == 'y':
                current_ledger = clear_ledger()
                print(" -> STATE RESET: Financial tables purged.")
                
        elif user_intent == "4":
            print("\nShutting down engine matrix safely. Ledger status committed. Goodbye!")
            break
            
        else:
            print(" -> Invalid menu coordinate. Select options 1 through 4.")

if __name__ == "__main__":
    main()