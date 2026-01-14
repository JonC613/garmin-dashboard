"""
Garmin Dashboard API
FastAPI backend for Garmin Connect data
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from garmin_service import GarminService
from pydantic import BaseModel
import traceback
import logging
from sqlalchemy.orm import Session
from database import get_db, init_db
from db_service import DatabaseService

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Garmin Dashboard API",
    description="API for retrieving health and fitness data from Garmin Connect",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Garmin Dashboard",
        "url": "http://localhost:8000"
    },
    license_info={
        "name": "MIT"
    }
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

# Initialize Garmin service
try:
    garmin_service = GarminService()
except Exception as e:
    print(f"Warning: Could not initialize Garmin service: {e}")
    garmin_service = None


class DateRequest(BaseModel):
    date: str


@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint - API Information
    
    Returns basic information about the API and available endpoints.
    """
    return {
        "message": "Garmin Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "heart_rate": "/api/heart-rate/{date}",
            "stress": "/api/stress/{date}",
            "sleep": "/api/sleep/{date}",
            "activities": "/api/activities/{date}",
            "all_data": "/api/data/{date}"
        }
    }


@app.get("/api/heart-rate/{target_date}", tags=["Health Data"])
async def get_heart_rate(target_date: str):
    """
    Get heart rate data for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns time-series heart rate measurements in beats per minute (BPM).
    """
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        data = garmin_service.get_heart_rate_data(target_date)
        return {
            "success": True,
            "date": target_date,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stress/{target_date}", tags=["Health Data"])
async def get_stress(target_date: str):
    """
    Get stress data for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns time-series stress level measurements (0-100 scale).
    """
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        data = garmin_service.get_stress_data(target_date)
        return {
            "success": True,
            "date": target_date,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sleep/{target_date}", tags=["Health Data"])
async def get_sleep(target_date: str):
    """
    Get sleep data for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns sleep stages, duration, and quality metrics.
    """
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        data = garmin_service.get_sleep_data(target_date)
        return {
            "success": True,
            "date": target_date,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/activities/{target_date}", tags=["Activities"])
async def get_activities(target_date: str):
    """
    Get activities for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns list of activities (runs, walks, cycling, etc.) with metrics.
    """
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        data = garmin_service.get_activities(target_date)
        return {
            "success": True,
            "date": target_date,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/hrv/{target_date}", tags=["Health Data"])
async def get_hrv(target_date: str):
    """
    Get HRV (Heart Rate Variability) data for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns time-series HRV measurements in milliseconds.
    """
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        data = garmin_service.get_hrv_data(target_date)
        return {
            "success": True,
            "date": target_date,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/{target_date}", tags=["Combined Data"])
async def get_all_data(target_date: str, db: Session = Depends(get_db)):
    """
    Get all data for a specific date
    
    - **target_date**: Date in YYYY-MM-DD format (e.g., 2025-12-25)
    
    Returns combined data including heart rate, stress, sleep, and activities.
    Data is automatically saved to the database.
    """
    logger.info(f"API request received for date: {target_date}")
    if not garmin_service:
        raise HTTPException(status_code=500, detail="Garmin service not initialized")
    
    try:
        logger.debug("Calling garmin_service.get_all_data")
        data = garmin_service.get_all_data(target_date)
        logger.info(f"Successfully retrieved data for {target_date}")
        logger.debug(f"Data keys: {data.keys() if isinstance(data, dict) else 'not a dict'}")
        
        # Save all data to database
        try:
            DatabaseService.save_all_garmin_data(db, target_date, data)
            logger.info(f"Successfully saved data to database for {target_date}")
        except Exception as db_error:
            logger.error(f"Error saving to database: {db_error}", exc_info=True)
            # Continue even if database save fails
        
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.error(f"ERROR in get_all_data: {e}", exc_info=True)
        print(f"ERROR in get_all_data: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/today", tags=["Combined Data"])
async def get_today_data():
    """
    Get all data for today
    
    Convenience endpoint that returns all data for the current date.
    """
    today = date.today().isoformat()
    return await get_all_data(today)


if __name__ == "__main__":
    import uvicorn
    print("Starting Garmin Dashboard API...")
    print("API available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
