# CNN Sports News Aggregator

A full-stack application that fetches and displays today's sports news headlines from CNN.com using RSS feeds.

> 📚 **New here?** Check out [INDEX.md](INDEX.md) for a complete guide to all documentation!

## Architecture

- **Backend**: Python Django REST Framework
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL
- **Data Source**: CNN Sports RSS Feed

## Features

- Fetches sports news headlines from CNN RSS feed
- Filters articles published today
- Displays title, link, and publication date
- RESTful API architecture
- Dockerized development environment
- Automated testing and CI/CD pipeline
- Pre-commit hooks for code quality

## Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- feedparser for RSS parsing
- pytest for testing

### Frontend
- React 18
- Axios for API calls
- Modern ES6+ JavaScript

### DevOps
- Docker & Docker Compose
- Pre-commit hooks (black, flake8, eslint, prettier)
- GitHub Actions CI/CD
- pytest for backend tests
- Jest for frontend tests

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TEST
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Build and run with Docker:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin

### Development Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

### Running Tests

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm test
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## API Endpoints

- `GET /api/news/` - Fetch today's sports news headlines
- `GET /api/news/refresh/` - Manually trigger news fetch

## Project Structure

```
TEST/
├── backend/
│   ├── news/               # News app
│   │   ├── models.py       # Data models
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── services.py     # Business logic (RSS parser)
│   │   └── tests/          # Unit tests
│   ├── config/             # Django settings
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API integration
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## SOLID Principles Implementation

- **Single Responsibility**: Separate services for RSS fetching, data models for storage, views for API endpoints
- **Open/Closed**: Extendable news fetcher service supporting multiple RSS sources
- **Liskov Substitution**: Abstract base classes for news sources
- **Interface Segregation**: Focused serializers and service interfaces
- **Dependency Inversion**: Services depend on abstractions, not concrete implementations

## License

MIT License
