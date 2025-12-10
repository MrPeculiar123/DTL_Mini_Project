from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connects to the postgres container defined in docker-compose
DATABASE_URL = "postgresql://admin:password@localhost:5432/rfp_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to be used in API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()