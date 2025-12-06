#!/bin/bash
# Development Setup Script for Unix/Linux/Mac

echo "Setting up Sports News Aggregator..."

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
else
    echo "✗ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose is installed"
else
    echo "✗ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please update it with your settings."
else
    echo "✓ .env file already exists"
fi

# Build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo ""
echo "✓ Setup complete!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000/api"
echo "Admin Panel: http://localhost:8000/admin"
echo ""
echo "To create a superuser, run:"
echo "docker-compose exec backend python manage.py createsuperuser"
