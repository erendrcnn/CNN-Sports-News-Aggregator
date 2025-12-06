"""
Tests for news services.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import pytz

from news.services import (
    CNNSportsFeedFetcher,
    TodayArticleFilter,
    NewsArticleRepository,
    NewsService,
)
from news.models import NewsArticle


@pytest.mark.django_db
class TestCNNSportsFeedFetcher:
    """Test cases for CNN Sports feed fetcher."""

    def test_get_source_name(self):
        """Test getting source name."""
        fetcher = CNNSportsFeedFetcher()
        assert fetcher.get_source_name() == "CNN Sports"

    @patch("news.services.feedparser.parse")
    def test_fetch_feed_success(self, mock_parse):
        """Test successful feed fetching."""
        mock_entry = Mock()
        mock_entry.get.side_effect = lambda key, default="": {
            "title": "Test Sports News",
            "link": "https://example.com/news",
            "summary": "Test description",
            "id": "test-id",
            "published": "Mon, 01 Jan 2024 12:00:00 GMT",
        }.get(key, default)

        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed

        fetcher = CNNSportsFeedFetcher()
        articles = fetcher.fetch_feed()

        assert len(articles) == 1
        assert articles[0]["title"] == "Test Sports News"
        assert articles[0]["link"] == "https://example.com/news"

    @patch("news.services.feedparser.parse")
    def test_fetch_feed_error(self, mock_parse):
        """Test feed fetching with error."""
        mock_feed = Mock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("Feed error")
        mock_parse.return_value = mock_feed

        fetcher = CNNSportsFeedFetcher()
        articles = fetcher.fetch_feed()

        assert len(articles) == 0


class TestTodayArticleFilter:
    """Test cases for article date filtering."""

    def test_filter_today_articles(self):
        """Test filtering articles published today."""
        today = datetime.now(pytz.UTC)
        yesterday = today.replace(day=today.day - 1)

        articles = [
            {"title": "Today 1", "published_date": today},
            {"title": "Yesterday", "published_date": yesterday},
            {"title": "Today 2", "published_date": today},
        ]

        filtered = TodayArticleFilter.filter(articles)

        assert len(filtered) == 2
        assert all(
            article["published_date"].date() == today.date() for article in filtered
        )


@pytest.mark.django_db
class TestNewsArticleRepository:
    """Test cases for NewsArticle repository."""

    def test_save_articles(self):
        """Test saving articles to database."""
        articles = [
            {
                "title": "Article 1",
                "link": "https://example.com/1",
                "description": "Description 1",
                "published_date": datetime.now(pytz.UTC),
                "guid": "guid-1",
            },
            {
                "title": "Article 2",
                "link": "https://example.com/2",
                "description": "Description 2",
                "published_date": datetime.now(pytz.UTC),
                "guid": "guid-2",
            },
        ]

        repo = NewsArticleRepository()
        saved_count = repo.save_articles(articles, "Test Source")

        assert saved_count == 2
        assert NewsArticle.objects.count() == 2

    def test_save_duplicate_articles(self):
        """Test that duplicate articles are not saved."""
        article_data = {
            "title": "Article",
            "link": "https://example.com/article",
            "description": "Description",
            "published_date": datetime.now(pytz.UTC),
            "guid": "guid-unique",
        }

        repo = NewsArticleRepository()

        # Save first time
        saved_count = repo.save_articles([article_data], "Test Source")
        assert saved_count == 1

        # Try to save again
        saved_count = repo.save_articles([article_data], "Test Source")
        assert saved_count == 0
        assert NewsArticle.objects.count() == 1

    def test_get_today_articles(self):
        """Test retrieving today's articles."""
        from django.utils import timezone
        from datetime import timedelta

        # Create today's article
        NewsArticle.objects.create(
            title="Today",
            link="https://example.com/today",
            published_date=timezone.now(),
            guid="today-guid",
        )

        # Create yesterday's article
        NewsArticle.objects.create(
            title="Yesterday",
            link="https://example.com/yesterday",
            published_date=timezone.now() - timedelta(days=1),
            guid="yesterday-guid",
        )

        repo = NewsArticleRepository()
        today_articles = repo.get_today_articles()

        assert len(today_articles) == 1
        assert today_articles[0].title == "Today"


@pytest.mark.django_db
class TestNewsService:
    """Test cases for NewsService."""

    def test_fetch_and_store_news(self):
        """Test fetching and storing news."""
        mock_fetcher = Mock()
        mock_fetcher.fetch_feed.return_value = [
            {
                "title": "Test Article",
                "link": "https://example.com/test",
                "description": "Test description",
                "published_date": datetime.now(pytz.UTC),
                "guid": "test-guid",
            }
        ]
        mock_fetcher.get_source_name.return_value = "Test Source"

        service = NewsService(mock_fetcher)
        saved_count = service.fetch_and_store_news(filter_today=False)

        assert saved_count == 1
        assert NewsArticle.objects.count() == 1

    def test_get_today_news(self):
        """Test getting today's news."""
        from django.utils import timezone

        NewsArticle.objects.create(
            title="Today's News",
            link="https://example.com/today",
            published_date=timezone.now(),
            guid="today-guid",
        )

        mock_fetcher = Mock()
        service = NewsService(mock_fetcher)
        articles = service.get_today_news()

        assert len(articles) == 1
        assert articles[0].title == "Today's News"
