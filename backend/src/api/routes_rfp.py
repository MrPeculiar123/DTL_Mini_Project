import shutil
import os
import threading
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.src.db.session import get_db
from backend.src.models.rfp import RFPModel
from backend.src.schemas.rfp import Rfp
from backend.src.services.pdf_service import extract_text_from_pdf

# --- IMPORT AGENT FUNCTIONS ---
from backend.src.scraping.scraper_service import run_scraper
from backend.src.agents.sales_agent import run_sales_agent
from backend.src.agents.main_agent import run_main_orchestrator

router = APIRouter(prefix="/rfps", tags=["rfps"])

UPLOAD_DIR = "backend/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- 1. LOGGING SYSTEM (In-Memory for Demo) ---
system_logs = []

def log_event(agent: str, message: str, type: str = "info"):
    """
    Adds a log entry to the in-memory list.
    The Frontend polls /rfps/logs to display these in the Live Feed.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = {
        "time": timestamp,
        "agent": agent,
        "msg": message,
        "type": type
    }
    # Insert at the beginning (newest first)
    system_logs.insert(0, log_entry)
    
    # Keep only the last 50 logs to prevent memory overflow during demo
    if len(system_logs) > 50:
        system_logs.pop()

@router.get("/logs")
def get_logs():
    return system_logs

# --- 2. USER & UTILITY ENDPOINTS (New Features) ---

@router.get("/me")
def get_current_user():
    """Mock endpoint for the 'Profile' section"""
    return {
        "username": "admin_user",
        "role": "Procurement Manager",
        "avatar": "https://i.pravatar.cc/150?u=admin"
    }

@router.get("/{rfp_id}/download")
def download_rfp_file(rfp_id: int, db: Session = Depends(get_db)):
    """Allows the frontend to download the actual PDF file"""
    rfp = db.query(RFPModel).filter(RFPModel.id == rfp_id).first()
    if not rfp or not rfp.file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Ensure file exists on disk
    if not os.path.exists(rfp.file_path):
        raise HTTPException(status_code=404, detail="File missing from server storage")
        
    return FileResponse(path=rfp.file_path, filename=rfp.filename, media_type='application/pdf')

# --- 3. CRUD ENDPOINTS (Updated with Filters) ---

@router.get("/", response_model=List[Rfp])
def list_rfps(
    status: Optional[str] = Query(None, description="Filter by status (NEW, QUALIFIED, etc)"),
    search: Optional[str] = Query(None, description="Search by title"),
    db: Session = Depends(get_db)
):
    query = db.query(RFPModel)
    
    # Apply Status Filter
    if status and status != "ALL":
        query = query.filter(RFPModel.status == status)
    
    # Apply Search Filter
    if search:
        query = query.filter(RFPModel.title.ilike(f"%{search}%"))
        
    return query.all()

@router.post("/", response_model=Rfp)
def create_rfp(
    title: str = Form(...),
    portal: str = Form(...),
    due_date: date = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    file_path = None
    filename = None
    extracted_text = None
    
    if file:
        filename = file.filename
        file_path = f"{UPLOAD_DIR}/{filename}"
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract text immediately for the agents to use later
        extracted_text = extract_text_from_pdf(file_path)
        log_event("Upload Service", f"Manually uploaded '{filename}'", "success")

    db_rfp = RFPModel(
        title=title,
        portal=portal,
        due_date=due_date,
        status="NEW",
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text
    )
    
    db.add(db_rfp)
    db.commit()
    db.refresh(db_rfp)
    
    return db_rfp

# --- 4. AUTOMATION TRIGGERS (The "Buttons") ---

@router.post("/scrape")
def trigger_scraping():
    log_event("System", "Scraper process initiated...", "info")
    
    def scrape_wrapper():
        try:
            # Run the scraper logic
            run_scraper()
            log_event("Scraper", "Scraping cycle completed successfully.", "success")
        except Exception as e:
            log_event("Scraper", f"Error during scraping: {str(e)}", "error")

    # Run in background thread so the UI doesn't freeze
    thread = threading.Thread(target=scrape_wrapper)
    thread.start()
    
    return {"message": "Scraping started in background"}

@router.post("/run-sales-agent")
def trigger_sales_agent():
    log_event("System", "Sales Agent activated.", "info")
    try:
        run_sales_agent()
        log_event("Sales Agent", "Filtering complete. Dashboard updated.", "success")
    except Exception as e:
        log_event("Sales Agent", f"Critical failure: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Sales Agent finished processing."}

@router.post("/run-main-agent")
def trigger_main_agent():
    log_event("System", "Main Orchestrator activated.", "info")
    try:
        run_main_orchestrator()
        log_event("Main Agent", "Orchestration cycle complete.", "success")
    except Exception as e:
        log_event("Main Agent", f"Orchestration failed: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Main Agent started."}