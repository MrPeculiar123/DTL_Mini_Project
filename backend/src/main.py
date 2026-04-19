from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.routes_rfp import router as rfp_router
from backend.src.db.session import engine, Base
from backend.src.models.rfp import RFPModel

# Create DB Tables on Startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RFP Automation Backend")

# CORS Setup (Allowing your React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfp_router)

@app.get("/health")
def health():
    return {"status": "ok", "database": "connected"}