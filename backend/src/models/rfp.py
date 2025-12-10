from sqlalchemy import Column, Integer, String, Date, Text
from backend.src.db.session import Base

class RFPModel(Base):
    __tablename__ = "rfps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    portal = Column(String)
    due_date = Column(Date)
    status = Column(String, default="NEW")
    
    # New fields for File Uploads
    filename = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    extracted_text = Column(Text, nullable=True) # Placeholder for parsed PDF text