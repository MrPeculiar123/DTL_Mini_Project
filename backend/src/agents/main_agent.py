# Master agent for orchestration.
from backend.src.db.session import SessionLocal
from backend.src.models.rfp import RFPModel

# We will import the Technical Agent here in the next phase
# from backend.src.agents.technical_agent import run_technical_analysis

def run_main_orchestrator():
    print("🤖 Main Agent: Checking for qualified work...")
    db = SessionLocal()
    
    # 1. Select the first 'QUALIFIED' RFP (FIFO queue)
    # In a real system, this would prioritize by value or client importance
    active_rfp = db.query(RFPModel).filter(RFPModel.status == "QUALIFIED").first()
    
    if not active_rfp:
        print("🤖 Main Agent: No qualified RFPs waiting.")
        db.close()
        return

    print(f"🤖 Main Agent: Selected '{active_rfp.title}' for processing.")
    
    # 2. Update status to prevent double-processing
    active_rfp.status = "PROCESSING"
    db.commit()
    
    # 3. Handoff to Technical Agent (Step 5 in your diagram)
    # For now, we just print the handoff. We will build the Tech Agent next.
    print(f"👉 Handoff: Triggering Technical Agent for RFP ID {active_rfp.id}...")
    
    # run_technical_analysis(active_rfp.id) <--- We will uncomment this next phase
    
    db.close()