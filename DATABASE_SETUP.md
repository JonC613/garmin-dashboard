# PostgreSQL Database Setup Guide

## Overview
PostgreSQL database integration has been added to automatically save all Garmin Connect data.

## What Was Added

### 1. Database Dependencies
- `sqlalchemy==2.0.25` - ORM for database operations
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `python-dotenv==1.0.0` - Environment variable management

### 2. New Files Created

#### `database.py`
- Database connection configuration
- SQLAlchemy engine and session management
- Connection URL from environment variables

#### `models.py`
- Database models for all Garmin data types:
  - `HeartRate` - Time-series heart rate data
  - `Stress` - Stress level measurements
  - `Sleep` - Sleep stages and quality metrics
  - `Activity` - Exercise activities
  - `BodyBattery` - Energy level tracking
  - `DailySteps` - Steps and activity summary
  - `RestingHeartRate` - Daily resting HR

#### `db_service.py`
- Service layer for database operations
- Methods to save each data type
- `save_all_garmin_data()` - Saves complete daily data

#### `init_db.py`
- Database initialization script
- Commands: `init`, `reset`, `drop`
- Creates all database tables

#### `.env.example` and `.env`
- Environment configuration template
- Database connection string

### 3. Modified Files

#### `api.py`
- Added database session dependency
- Updated `/api/data/{date}` endpoint to auto-save data
- Initializes database on startup

#### `README.md`
- Added PostgreSQL to prerequisites
- Updated setup instructions with database steps
- Added database initialization commands

## Setup Instructions

### 1. Install PostgreSQL
Download and install PostgreSQL 12 or higher from:
https://www.postgresql.org/download/

### 2. Create Database
```sql
CREATE DATABASE garmin_dashboard;
```

### 3. Configure Connection
Edit `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/garmin_dashboard
```

### 4. Initialize Database Tables
```bash
cd backend
python init_db.py init
```

### 5. Restart Backend Server
The server will automatically connect to the database and save all fetched data.

## Database Schema

### Tables Created:
1. **heart_rate** - Time-series heart rate data
2. **stress** - Stress measurements throughout the day
3. **sleep** - Sleep stages, duration, and quality
4. **activities** - Exercise activities with metrics
5. **body_battery** - Energy level tracking
6. **daily_steps** - Daily step count and calories
7. **resting_heart_rate** - Daily resting heart rate

## How It Works

1. When the frontend requests data via `/api/data/{date}`, the API:
   - Fetches data from Garmin Connect
   - **Automatically saves it to PostgreSQL**
   - Returns data to frontend

2. Data is deduplicated:
   - Existing records are updated
   - New records are inserted
   - Time-series data (heart rate, stress) replaces previous day's data

3. Database operations are logged for monitoring

## Database Management Commands

```bash
# Initialize database (create tables)
python init_db.py init

# Reset database (drop and recreate all tables)
python init_db.py reset

# Drop all tables
python init_db.py drop
```

## Environment Variables

Required in `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/garmin_dashboard
```

Format: `postgresql://[user]:[password]@[host]:[port]/[database]`

## Troubleshooting

### Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`

### Database Not Created
- Run `python init_db.py init` manually
- Check PostgreSQL logs for errors

## Next Steps

- All data is now being saved automatically
- You can query the database directly for analytics
- Consider adding data retention policies
- Set up database backups
