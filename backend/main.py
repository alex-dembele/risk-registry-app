from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import get_db, engine
from sqlalchemy.orm import Session
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Risk Registry API",
    description="API for IT risk management!",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test connexion DB
        db.execute(text("SELECT 1"))
        logger.info("Health check: DB connection OK")
        return {"status": "healthy", "db_connection": "OK", "version": app.version}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="DB connection failed")