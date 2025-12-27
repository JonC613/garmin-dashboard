"""
Database initialization and setup script
Creates tables and optionally seeds initial data
"""

from database import engine, Base, SessionLocal
from models import (
    HeartRate, Stress, Sleep, Activity, BodyBattery,
    DailySteps, RestingHeartRate
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database tables"""
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # Display created tables
        logger.info("Created tables:")
        for table in Base.metadata.sorted_tables:
            logger.info(f"  - {table.name}")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_all_tables():
    """Drop all database tables - USE WITH CAUTION!"""
    logger.warning("Dropping all database tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        raise


def reset_database():
    """Drop and recreate all tables - USE WITH CAUTION!"""
    logger.warning("Resetting database...")
    drop_all_tables()
    init_database()
    logger.info("Database reset complete")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_database()
        elif command == "reset":
            confirm = input("Are you sure you want to reset the database? This will delete all data! (yes/no): ")
            if confirm.lower() == "yes":
                reset_database()
            else:
                logger.info("Reset cancelled")
        elif command == "drop":
            confirm = input("Are you sure you want to drop all tables? This will delete all data! (yes/no): ")
            if confirm.lower() == "yes":
                drop_all_tables()
            else:
                logger.info("Drop cancelled")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: init, reset, drop")
    else:
        # Default: initialize database
        init_database()
