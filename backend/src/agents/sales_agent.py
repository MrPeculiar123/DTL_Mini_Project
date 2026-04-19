# Sales agent for sales logic.
from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.src.db.session import SessionLocal
from backend.src.models.rfp import RFPModel

def run_sales_agent():
    print("🕵️‍♂️ Sales Agent: Started. Reviewing new RFPs...")
    db = SessionLocal()
    
    # 1. Fetch all 'NEW' RFPs
    new_rfps = db.query(RFPModel).filter(RFPModel.status == "NEW").all()
    
    if not new_rfps:
        print("🕵️‍♂️ Sales Agent: No new RFPs to process.")
        db.close()
        return

    today = date.today()
    three_months_out = today + timedelta(days=90)
    
    for rfp in new_rfps:
        print(f"   > Reviewing '{rfp.title}' (Due: {rfp.due_date})")
        
        # 2. Apply Business Rules
        if rfp.due_date < today:
            rfp.status = "REJECTED"
            print(f"     ❌ REJECTED: Expired.")
            
        elif rfp.due_date > three_months_out:
            rfp.status = "ON_HOLD"
            print(f"     ⏸️  ON HOLD: Due date is too far away.")
            
        else:
            rfp.status = "QUALIFIED"
            print(f"     ✅ QUALIFIED: Ready for Technical Team.")
            
    db.commit()
    db.close()
    print("🕵️‍♂️ Sales Agent: Review complete.")