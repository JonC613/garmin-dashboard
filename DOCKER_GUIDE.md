# Docker Setup Complete! 🎉

## What's Running

Your complete Garmin Dashboard stack is now running in Docker containers:

### Services
- **PostgreSQL**: Database server on port 5432
- **Backend API**: Python/FastAPI server on port 8000
- **Frontend**: React app on port 3000

## Access Your Application

- 🌐 **Frontend Dashboard**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 🗄️ **PostgreSQL**: localhost:5432

## Container Status

All containers are running and healthy:
```
✅ garmin-postgres  - PostgreSQL 15 (healthy)
✅ garmin-backend   - FastAPI server (healthy)
✅ garmin-frontend  - React dev server (starting)
```

Database tables have been initialized:
- activities
- body_battery
- daily_steps
- heart_rate
- resting_heart_rate
- sleep
- stress

## Docker Commands

### Basic Operations
```bash
# View status
docker compose ps

# View logs
docker compose logs -f
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Stop all services
docker compose down

# Start services
docker compose up -d

# Restart a service
docker compose restart backend

# Rebuild after code changes
docker compose up --build
```

### Database Operations
```bash
# Access PostgreSQL CLI
docker compose exec postgres psql -U postgres -d garmin_dashboard

# Backup database
docker compose exec postgres pg_dump -U postgres garmin_dashboard > backup.sql

# Restore database
docker compose exec -T postgres psql -U postgres garmin_dashboard < backup.sql

# Reset database
docker compose exec backend python init_db.py reset
```

### Development
```bash
# View real-time backend logs
docker compose logs -f backend

# Execute commands in backend container
docker compose exec backend python <script.py>

# Shell into backend
docker compose exec backend bash

# Shell into frontend
docker compose exec frontend sh
```

## Features

✅ **Automatic PostgreSQL setup** - No manual database installation needed
✅ **Data persistence** - Database data saved in Docker volume
✅ **Hot reloading** - Code changes automatically refresh
✅ **Network isolation** - All services on private Docker network
✅ **Health checks** - Automatic container health monitoring
✅ **Easy cleanup** - Remove everything with one command

## Data Persistence

Your Garmin data is automatically saved to PostgreSQL and persists even when containers are stopped. The data is stored in a Docker volume named `garmin-dashboard_postgres_data`.

## Development Workflow

1. **Make code changes** - Files are mounted, changes reflect immediately
2. **Backend** - Server auto-reloads on Python file changes
3. **Frontend** - Vite auto-reloads on React/TypeScript changes
4. **Database** - Data persists across container restarts

## Stopping Services

```bash
# Stop containers (data persists)
docker compose down

# Stop and remove volumes (deletes all data!)
docker compose down -v
```

## Troubleshooting

### Port Already in Use
If ports 3000, 8000, or 5432 are in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change left number only
```

### Container Not Starting
```bash
# Check logs
docker compose logs <service-name>

# Rebuild
docker compose up --build --force-recreate
```

### Database Connection Issues
```bash
# Restart services
docker compose restart backend postgres
```

## Next Steps

1. Open http://localhost:3000 in your browser
2. Your Garmin data will be fetched and saved to PostgreSQL automatically
3. View API docs at http://localhost:8000/docs

Enjoy your Garmin Dashboard! 🏃‍♂️📊
