from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
from ..schemas.rfp import Rfp, RfpCreate

router = APIRouter(prefix="/rfps", tags=["rfps"])

# TEMP in-memory store
_rfps: list[Rfp] = []
_next_id = 1

@router.get("/", response_model=List[Rfp])
def list_rfps():
    return _rfps

@router.post("/", response_model=Rfp)
def create_rfp(payload: RfpCreate):
    global _next_id
    rfp = Rfp(id=_next_id, **payload.model_dump())
    _next_id += 1
    _rfps.append(rfp)
    return rfp

# Seed some mock data at import time
if not _rfps:
    sample = Rfp(
        id=1,
        title="Industrial Cables Tender",
        portal="MockPortal",
        due_date=date.today(),
        status="NEW",
    )
    _rfps.append(sample)
    _next_id = 2
