# Usage Examples

This document provides practical examples of using the CNN Sports News Aggregator.

---

## 1. Starting the Application

### Using Docker (Recommended)

```powershell
# Navigate to project
cd c:\Users\username\Desktop\CNN-Sports-News-Aggregator

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

### Using the Standalone Script

```powershell
# Install dependencies
pip install -r requirements-standalone.txt

# Run the script
python fetch_news.py
```

**Output:**
```
================================================================================
CNN SPORTS NEWS AGGREGATOR
Fetching today's sports headlines...
================================================================================

Fetching sports news from CNN RSS feed...
URL: http://rss.cnn.com/rss/edition_sport.rss

Found 5 article(s) published today:

================================================================================

1. NBA: Lakers defeat Warriors in overtime thriller
   Link: https://cnn.com/sport/nba-lakers-warriors
   Published: 2024-01-01 18:30:00 UTC
   Description: In an electrifying overtime showdown, the Los Angeles Lakers...
--------------------------------------------------------------------------------

2. Premier League: Manchester United secures top-four spot
   Link: https://cnn.com/sport/premier-league-man-utd
   Published: 2024-01-01 16:45:00 UTC
   Description: Manchester United's victory over Arsenal ensures their...
--------------------------------------------------------------------------------
```

---

## 2. Using the Web Interface

### View Today's Headlines

1. Open http://localhost:3000
2. The page automatically loads today's sports news
3. Scroll to view all articles

### Refresh News Feed

1. Click the "🔄 Refresh" button in the header
2. Wait for the loading indicator
3. New articles will appear

### Read Full Article

1. Click on any article title
2. Opens the full article on CNN.com in a new tab

---

## 3. Using the REST API

### Get Today's News (curl)

```bash
curl http://localhost:8000/api/news/today/
```

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "NBA: Lakers defeat Warriors in overtime thriller",
      "link": "https://cnn.com/sport/nba-lakers-warriors",
      "published_date": "2024-01-01T18:30:00Z",
      "source": "CNN Sports"
    }
  ]
}
```

### Refresh News Feed (curl)

```bash
curl -X POST http://localhost:8000/api/news/refresh/
```

**Response:**
```json
{
  "message": "Successfully fetched and saved 3 new articles",
  "count": 8,
  "results": [...]
}
```

### Get All News with Pagination (curl)

```bash
curl http://localhost:8000/api/news/?page=1
```

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/news/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 4. Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Get today's news
def get_todays_news():
    response = requests.get(f"{BASE_URL}/news/today/")
    data = response.json()
    
    print(f"Found {data['count']} articles today:\n")
    
    for article in data['results']:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Published: {article['published_date']}")
        print("-" * 80)

# Refresh news feed
def refresh_news():
    response = requests.post(f"{BASE_URL}/news/refresh/")
    data = response.json()
    
    print(data['message'])
    print(f"Total articles: {data['count']}")

# Get specific article
def get_article(article_id):
    response = requests.get(f"{BASE_URL}/news/{article_id}/")
    article = response.json()
    
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Description: {article['description']}")
    print(f"Published: {article['published_date']}")
    print(f"Source: {article['source']}")

# Usage
if __name__ == "__main__":
    get_todays_news()
    # refresh_news()
    # get_article(1)
```

---

## 5. Using JavaScript Fetch

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Get today's news
async function getTodaysNews() {
  try {
    const response = await fetch(`${BASE_URL}/news/today/`);
    const data = await response.json();
    
    console.log(`Found ${data.count} articles today:`);
    
    data.results.forEach(article => {
      console.log(`Title: ${article.title}`);
      console.log(`Link: ${article.link}`);
      console.log(`Published: ${article.published_date}`);
      console.log('-'.repeat(80));
    });
  } catch (error) {
    console.error('Error fetching news:', error);
  }
}

// Refresh news feed
async function refreshNews() {
  try {
    const response = await fetch(`${BASE_URL}/news/refresh/`, {
      method: 'POST',
    });
    const data = await response.json();
    
    console.log(data.message);
    console.log(`Total articles: ${data.count}`);
  } catch (error) {
    console.error('Error refreshing news:', error);
  }
}

// Get specific article
async function getArticle(articleId) {
  try {
    const response = await fetch(`${BASE_URL}/news/${articleId}/`);
    const article = await response.json();
    
    console.log(`Title: ${article.title}`);
    console.log(`Link: ${article.link}`);
    console.log(`Description: ${article.description}`);
  } catch (error) {
    console.error('Error fetching article:', error);
  }
}

// Usage
getTodaysNews();
// refreshNews();
// getArticle(1);
```

---

## 6. Using the Django Admin Panel

### Access Admin Panel

1. Create a superuser:
```powershell
docker-compose exec backend python manage.py createsuperuser
```

2. Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

3. Access admin panel: http://localhost:8000/admin

4. Login with your credentials

### Manage Articles

- **View all articles:** Click "News articles"
- **Search articles:** Use the search bar
- **Filter articles:** Use the right sidebar filters
- **Edit article:** Click on an article title
- **Delete article:** Select articles and choose "Delete selected"

---

## 7. Running Tests

### Backend Tests

```powershell
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=news

# Run specific test file
docker-compose exec backend pytest news/tests/test_services.py

# Run specific test
docker-compose exec backend pytest news/tests/test_models.py::TestNewsArticleModel::test_create_news_article

# Verbose output
docker-compose exec backend pytest -v
```

### Frontend Tests

```powershell
# Run all tests
docker-compose exec frontend npm test

# Run with coverage
docker-compose exec frontend npm test -- --coverage

# Run in CI mode (no watch)
docker-compose exec frontend npm test -- --watchAll=false
```

---

## 8. Development Workflow

### Make Code Changes

1. Edit files in `backend/` or `frontend/`
2. Changes are automatically reflected (hot reload)

### Add New Dependencies

**Backend:**
```powershell
# Add to requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt

# Rebuild container
docker-compose up --build backend
```

**Frontend:**
```powershell
# Install package
docker-compose exec frontend npm install new-package

# Or rebuild
docker-compose up --build frontend
```

### Database Migrations

```powershell
# Create migration
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# View migrations
docker-compose exec backend python manage.py showmigrations
```

---

## 9. Troubleshooting

### No Articles Showing

```powershell
# Check backend logs
docker-compose logs -f backend

# Manually refresh news
curl -X POST http://localhost:8000/api/news/refresh/

# Check database
docker-compose exec backend python manage.py shell
>>> from news.models import NewsArticle
>>> NewsArticle.objects.count()
```

### Port Already in Use

```powershell
# Change ports in docker-compose.yml
# For example, change 3000:80 to 3001:80

# Or stop conflicting services
docker ps
docker stop <container-id>
```

### Database Connection Issues

```powershell
# Reset database
docker-compose down -v
docker-compose up --build

# Check database logs
docker-compose logs db
```

---

## 10. Production Deployment Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=0` in `.env`
- [ ] Update `DJANGO_ALLOWED_HOSTS`
- [ ] Configure proper database credentials
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up rate limiting
- [ ] Review security settings
- [ ] Run security audit
- [ ] Set up CI/CD pipeline

---

## Additional Resources

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [SOLID_PRINCIPLES.md](SOLID_PRINCIPLES.md) - Architecture guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide

---

Happy coding! 🚀
