"""
Tests for API views.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from unittest.mock import patch, Mock

from news.models import NewsArticle


@pytest.mark.django_db
class TestNewsArticleViewSet:
    """Test cases for NewsArticle ViewSet."""

    @pytest.fixture
    def api_client(self):
        """Create API client."""
        return APIClient()

    @pytest.fixture
    def sample_articles(self):
        """Create sample articles."""
        articles = []
        for i in range(3):
            article = NewsArticle.objects.create(
                title=f"Test Article {i}",
                link=f"https://example.com/article-{i}",
                published_date=timezone.now(),
                description=f"Description {i}",
                guid=f"guid-{i}",
                source="Test Source",
            )
            articles.append(article)
        return articles

    def test_list_articles(self, api_client, sample_articles):
        """Test listing all articles."""
        url = reverse("news-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3

    def test_retrieve_article(self, api_client, sample_articles):
        """Test retrieving a single article."""
        article = sample_articles[0]
        url = reverse("news-detail", kwargs={"pk": article.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == article.title
        assert response.data["link"] == article.link

    def test_today_endpoint(self, api_client, sample_articles):
        """Test today's news endpoint."""
        url = reverse("news-today")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data
        assert "results" in response.data

    @patch("news.views.CNNSportsFeedFetcher")
    @patch("news.views.NewsService")
    def test_refresh_endpoint(self, mock_service_class, mock_fetcher_class, api_client):
        """Test news refresh endpoint."""
        # Setup mocks
        mock_service = Mock()
        mock_service.fetch_and_store_news.return_value = 5
        mock_service.get_today_news.return_value = []
        mock_service_class.return_value = mock_service

        url = reverse("news-refresh")
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
        assert response.data["count"] == 0

    def test_today_endpoint_empty(self, api_client):
        """Test today endpoint with no articles."""
        url = reverse("news-today")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0
