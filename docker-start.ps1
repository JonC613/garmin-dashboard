# Docker startup script for Garmin Dashboard
# PowerShell script to start all services

Write-Host "Starting Garmin Dashboard Docker Stack..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Build and start services
Write-Host "`nBuilding and starting services..." -ForegroundColor Yellow
docker-compose up --build -d

# Wait for services to be ready
Write-Host "`nWaiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "`nService Status:" -ForegroundColor Green
docker-compose ps

# Initialize database
Write-Host "`nInitializing database..." -ForegroundColor Yellow
docker-compose exec -T backend python init_db.py init

Write-Host "`n✅ Garmin Dashboard is ready!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend:    http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nTo view logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "To stop:      docker-compose down" -ForegroundColor Yellow
