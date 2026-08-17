# Garmin Connect Dashboard

A full-stack web application for visualizing health and fitness data from Garmin Connect.

## Features

- **Heart Rate Monitoring**: View heart rate throughout the day with average and peak values
- **Stress Tracking**: Monitor stress levels with visualization and statistics
- **Sleep Analysis**: Track sleep stages (deep, light, REM, awake) and quality
- **Activity Tracking**: Steps, calories, distance, and intensity minutes
- **Body Battery**: Energy level monitoring throughout the day
- **Resting Heart Rate**: Daily resting HR with min/max values
- **PostgreSQL Database**: Automatic data persistence

## Tech Stack

### Backend
- **Python 3.12+**
- **FastAPI** - Modern web framework
- **garminconnect** - Garmin Connect API client
- **uvicorn** - ASGI server
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database for storing health data

### Frontend
- **React 18** with TypeScript
- **Vite** - Build tool
- **Fluent UI React Components** - Microsoft's design system
- **Recharts** - Data visualization
- **Axios** - HTTP client

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop
- Garmin Connect account

### Setup

1. **Clone or navigate to the project:**
```bash
cd garmin-dashboard
```

2. **Add your Garmin credentials:**
Create `backend/garmin_credentials.json`:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

3. **Start all services:**
```powershell
.\docker-start.ps1
```

Or manually:
```bash
docker-compose up --build
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart a service
docker-compose restart backend

# Rebuild after code changes
docker-compose up --build
```

---

## Manual Setup (Without Docker)

### Prerequisites
- Python 3.12 or higher
- Node.js 18 or higher
- Garmin Connect account
- **PostgreSQL 12 or higher**

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. **Setup PostgreSQL Database:**

Create a PostgreSQL database:
```sql
CREATE DATABASE garmin_dashboard;
```

6. **Configure Environment Variables:**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your database connection:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/garmin_dashboard
```

7. **Initialize Database Tables:**
```bash
python init_db.py init
```

8. Create `garmin_credentials.json` with your Garmin Connect credentials:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

9. Start the backend server:
```bash
uvicorn api:app --reload --port 8000
```

The backend will be available at http://localhost:8000

**Note:** All data fetched from Garmin Connect is automatically saved to the PostgreSQL database.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
garmin-dashboard/
├── backend/
│   ├── api.py                      # FastAPI application
│   ├── garmin_service.py           # Garmin Connect API integration
│   ├── requirements.txt            # Python dependencies
│   └── garmin_credentials.json     # Your credentials (not in git)
├── frontend/
│   ├── src/
│   │   ├── main.tsx               # React entry point
│   │   ├── components/
│   │   │   ├── Dashboard.tsx      # Main dashboard component
│   │   │   ├── HeartRateChart.tsx
│   │   │   ├── StressChart.tsx
│   │   │   ├── SleepChart.tsx
│   │   │   ├── BodyBatteryChart.tsx
│   │   │   └── StepsCaloriesCard.tsx
│   │   └── services/
│   │       └── api.ts             # API client
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Security Notes

⚠️ **Important**: Never commit `garmin_credentials.json` to version control. This file is included in `.gitignore`.

## Privacy and safe sharing

Garmin data can contain sensitive health metrics, activity routes, timestamps, and account metadata. This repository contains application code only—never commit Garmin exports, database dumps, screenshots with real data, `.env` files, or credentials.

For demos and screenshots, use synthetic or fully anonymized data. Before deploying a copy, configure credentials locally through ignored files or environment variables and restrict database access appropriately.

## License

MIT
