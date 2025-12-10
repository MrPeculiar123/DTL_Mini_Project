# backend/src/agents/main_agent.py
from backend.src.db.session import SessionLocal
from backend.src.models.rfp import RFPModel

# --- IMPORT THE NEW AGENT ---
from backend.src.agents.technical_agent import run_technical_analysis

def run_main_orchestrator():
    print("🤖 Main Agent: Checking for qualified work...")
    db = SessionLocal()
    
    # 1. Select the first 'QUALIFIED' RFP
    active_rfp = db.query(RFPModel).filter(RFPModel.status == "QUALIFIED").first()
    
    if not active_rfp:
        print("🤖 Main Agent: No qualified RFPs waiting.")
        db.close()
        return

    print(f"🤖 Main Agent: Selected '{active_rfp.title}' (ID: {active_rfp.id})")
    
    # 2. Update status to PROCESSING
    active_rfp.status = "PROCESSING"
    db.commit()
    
    # 3. Trigger Technical Agent
    print(f"👉 Handoff: Triggering Technical Agent...")
    try:
        recommendations = run_technical_analysis(active_rfp.id)
        
        # 4. If successful, handoff to Pricing (Next Step in future)
        if recommendations:
            print("🤖 Main Agent: Technical analysis received.")
            print("   > Ready for Pricing Agent.")
            # run_pricing_agent(active_rfp.id, recommendations)
        else:
            print("⚠️ Main Agent: Technical Agent returned no results.")
            
    except Exception as e:
        print(f"❌ Main Agent Error: {e}")
        active_rfp.status = "ERROR"
        db.commit()
    
    db.close()