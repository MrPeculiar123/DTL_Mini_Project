from pydantic import BaseModel
from datetime import date
from typing import Optional

class RfpBase(BaseModel):
    title: str
    portal: str
    due_date: date
    status: str = "NEW"

# Used for reading data (Response)
class Rfp(RfpBase):
    id: int
    filename: Optional[str] = None
    file_path: Optional[str] = None

    class Config:
        from_attributes = True