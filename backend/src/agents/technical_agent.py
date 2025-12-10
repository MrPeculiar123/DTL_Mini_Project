# Technical agent for technical logic.
# backend/src/agents/technical_agent.py
import json
import os
from sqlalchemy.orm import Session
from backend.src.db.session import SessionLocal
from backend.src.models.rfp import RFPModel
from backend.src.services.matching_engine import find_best_matches
from backend.src.services.pdf_service import extract_text_from_pdf # Reusing your existing service

def run_technical_analysis(rfp_id: int):
    print(f"⚙️  Tech Agent: Analyzing RFP ID {rfp_id}...")
    db = SessionLocal()
    
    # 1. Fetch RFP Data
    rfp = db.query(RFPModel).filter(RFPModel.id == rfp_id).first()
    
    if not rfp:
        print("❌ Tech Agent: RFP not found.")
        db.close()
        return

    # 2. Ensure we have text to analyze
    rfp_text = rfp.extracted_text
    if not rfp_text and rfp.file_path:
        print(f"   > Text missing. Extracting from {rfp.filename} now...")
        try:
            rfp_text = extract_text_from_pdf(rfp.file_path)
            rfp.extracted_text = rfp_text # Save back to DB
            db.commit()
        except Exception as e:
            print(f"   ❌ Extraction failed: {e}")
            db.close()
            return
    
    if not rfp_text:
        print("   ❌ No text available for analysis.")
        db.close()
        return

    # 3. Run Matching Algorithm (The Brain)
    print("   > Running Matching Engine (TF-IDF + Regex)...")
    recommendations = find_best_matches(rfp_text)
    
    # 4. Display & Save Results
    print(f"   ✅ Analysis Complete. Top Match: {recommendations[0]['sku']} ({recommendations[0]['match_score']*100}%)")
    
    # In a real app, you would save this to a 'recommendations' table. 
    # For this demo, we can append it to the extracted text or log it.
    # rfp.technical_notes = json.dumps(recommendations) 
    
    # 5. Move Workflow Forward
    rfp.status = "TECH_REVIEW_COMPLETE"
    db.commit()
    db.close()
    
    return recommendations