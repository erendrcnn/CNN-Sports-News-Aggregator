# Quick Start Guide

## Prerequisites
- Docker Desktop installed and running
- Git (optional, for version control)

## Getting Started in 5 Minutes

### 1. Navigate to the project directory
```powershell
cd c:\Users\username\Desktop\CNN-Sports-News-Aggregator
```

### 2. Create environment file
```powershell
Copy-Item .env.example .env
```

### 3. Start the application with Docker
```powershell
docker-compose up --build
```

This will:
- Build the backend (Django) container
- Build the frontend (React) container
- Start PostgreSQL database
- Run database migrations
- Start all services

### 4. Access the application

**Wait about 30-60 seconds for all services to start, then access:**

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/news/
- **Admin Panel:** http://localhost:8000/admin

### 5. Create an admin user (optional)

Open a new PowerShell window and run:
```powershell
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts to create your admin account.

---

## Testing the Standalone Script

If you want to test the news fetching without Docker:

### 1. Install Python dependencies
```powershell
pip install -r requirements-standalone.txt
```

### 2. Run the standalone script
```powershell
python fetch_news.py
```

This will fetch and display today's CNN sports news headlines.

---

## Common Commands

### View logs
```powershell
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Stop services
```powershell
docker-compose down
```

### Restart services
```powershell
docker-compose restart
```

### Rebuild after code changes
```powershell
docker-compose up --build
```

### Run tests

**Backend tests:**
```powershell
docker-compose exec backend pytest
```

**Frontend tests:**
```powershell
docker-compose exec frontend npm test
```

---

## Using the Application

### 1. View Today's News
- Open http://localhost:3000
- The page will automatically load today's sports news from CNN

### 2. Refresh News
- Click the "🔄 Refresh" button in the header
- This fetches the latest news from the CNN RSS feed

### 3. Manual API Testing

**Get today's news:**
```powershell
curl http://localhost:8000/api/news/today/
```

**Refresh news feed:**
```powershell
curl -X POST http://localhost:8000/api/news/refresh/
```

---

## Troubleshooting

### Services won't start
1. Make sure Docker Desktop is running
2. Check if ports 3000, 8000, or 5432 are already in use
3. Try: `docker-compose down` then `docker-compose up --build`

### No news articles showing
1. Click the "Refresh" button to fetch news
2. Check if CNN RSS feed is accessible: http://rss.cnn.com/rss/edition_sport.rss
3. Check backend logs: `docker-compose logs backend`

### Database errors
1. Reset the database:
```powershell
docker-compose down -v
docker-compose up --build
```

---

## Next Steps

1. **Explore the Admin Panel:** http://localhost:8000/admin
   - Create a superuser first (see step 5 above)
   - View and manage news articles

2. **Read the API Documentation:** `API_DOCUMENTATION.md`
   - Learn about all available endpoints
   - Test API calls

3. **Review the Code:**
   - Backend: `backend/news/` - Django models, views, services
   - Frontend: `frontend/src/` - React components
   - Check SOLID principles implementation

4. **Run Tests:**
   - Backend: `docker-compose exec backend pytest`
   - Frontend: `docker-compose exec frontend npm test`

5. **Set up Development Environment:**
   - Read `CONTRIBUTING.md` for contribution guidelines
   - Install pre-commit hooks for code quality

---

## Architecture Overview

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │─────▶│   Django    │─────▶│ PostgreSQL  │
│  Frontend   │      │   Backend   │      │  Database   │
│  (Port 3000)│      │  (Port 8000)│      │ (Port 5432) │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  CNN RSS    │
                     │    Feed     │
                     └─────────────┘
```

---

Enjoy using the CNN Sports News Aggregator! 🏀⚽🏈
