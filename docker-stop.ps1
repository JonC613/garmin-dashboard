# Docker stop script for Garmin Dashboard

Write-Host "Stopping Garmin Dashboard Docker Stack..." -ForegroundColor Yellow

docker-compose down

Write-Host "✅ All services stopped." -ForegroundColor Green
