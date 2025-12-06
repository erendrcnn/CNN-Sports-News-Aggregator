# Development Setup Script for Windows
# Run this script in PowerShell

Write-Host "Setting up Sports News Aggregator..." -ForegroundColor Green

# Check if Docker is installed
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker is installed" -ForegroundColor Green
} else {
    Write-Host "Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "Docker Compose is installed" -ForegroundColor Green
} else {
    Write-Host "Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ".env file created. Please update it with your settings." -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

# Build and start Docker containers
Write-Host "Building and starting Docker containers..." -ForegroundColor Yellow
docker-compose up --build -d

# Wait for services to be ready
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
Write-Host "Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000/api" -ForegroundColor Cyan
Write-Host "Admin Panel: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "To create a superuser, run:" -ForegroundColor Yellow
Write-Host "docker-compose exec backend python manage.py createsuperuser" -ForegroundColor White
