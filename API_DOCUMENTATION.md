# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. List All News Articles

**Endpoint:** `GET /news/`

**Description:** Retrieve all news articles with pagination.

**Parameters:**
- `page` (optional): Page number for pagination

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Sports News Title",
      "link": "https://cnn.com/article",
      "published_date": "2024-01-01T12:00:00Z",
      "source": "CNN Sports"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/news/
```

---

### 2. Get Single Article

**Endpoint:** `GET /news/{id}/`

**Description:** Retrieve details of a specific article.

**Response:**
```json
{
  "id": 1,
  "title": "Sports News Title",
  "link": "https://cnn.com/article",
  "published_date": "2024-01-01T12:00:00Z",
  "description": "Article description...",
  "source": "CNN Sports",
  "fetched_at": "2024-01-01T12:05:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/api/news/1/
```

---

### 3. Get Today's News

**Endpoint:** `GET /news/today/`

**Description:** Retrieve all articles published today.

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Today's Sports News",
      "link": "https://cnn.com/article",
      "published_date": "2024-01-01T12:00:00Z",
      "source": "CNN Sports"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/news/today/
```

---

### 4. Refresh News Feed

**Endpoint:** `POST /news/refresh/`

**Description:** Manually trigger fetching news from the RSS feed.

**Response:**
```json
{
  "message": "Successfully fetched and saved 5 new articles",
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Latest Sports News",
      "link": "https://cnn.com/article",
      "published_date": "2024-01-01T12:00:00Z",
      "source": "CNN Sports"
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/news/refresh/
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Failed to fetch news"
}
```

---

## Data Models

### NewsArticle
```typescript
{
  id: number;
  title: string;
  link: string;
  published_date: string (ISO 8601);
  description?: string;
  source: string;
  fetched_at: string (ISO 8601);
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. This should be added in production.

---

## Authentication

Currently, the API is public and does not require authentication. For production use, consider implementing:
- API Keys
- JWT tokens
- OAuth 2.0

---

## CORS

The API allows CORS requests from:
- `http://localhost:3000` (development)

Configure `CORS_ALLOWED_ORIGINS` in settings for production.

---

## Testing the API

### Using curl

```bash
# Get today's news
curl http://localhost:8000/api/news/today/

# Refresh news feed
curl -X POST http://localhost:8000/api/news/refresh/

# Get all news (paginated)
curl http://localhost:8000/api/news/

# Get specific article
curl http://localhost:8000/api/news/1/
```

### Using Python requests

```python
import requests

# Get today's news
response = requests.get('http://localhost:8000/api/news/today/')
data = response.json()
print(f"Found {data['count']} articles")

# Refresh news feed
response = requests.post('http://localhost:8000/api/news/refresh/')
data = response.json()
print(data['message'])
```

### Using JavaScript fetch

```javascript
// Get today's news
fetch('http://localhost:8000/api/news/today/')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.count} articles`);
    console.log(data.results);
  });

// Refresh news feed
fetch('http://localhost:8000/api/news/refresh/', {
  method: 'POST',
})
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
  });
```
