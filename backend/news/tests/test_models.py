"""
Tests for NewsArticle model.
"""

import pytest
from django.utils import timezone
from datetime import timedelta

from news.models import NewsArticle


@pytest.mark.django_db
class TestNewsArticleModel:
    """Test cases for NewsArticle model."""

    def test_create_news_article(self):
        """Test creating a news article."""
        article = NewsArticle.objects.create(
            title="Test Article",
            link="https://example.com/test",
            published_date=timezone.now(),
            description="Test description",
            source="Test Source",
            guid="test-guid-123",
        )

        assert article.title == "Test Article"
        assert article.link == "https://example.com/test"
        assert article.source == "Test Source"
        assert article.guid == "test-guid-123"

    def test_is_published_today(self):
        """Test is_published_today method."""
        today_article = NewsArticle.objects.create(
            title="Today's Article",
            link="https://example.com/today",
            published_date=timezone.now(),
            guid="today-guid",
        )

        yesterday_article = NewsArticle.objects.create(
            title="Yesterday's Article",
            link="https://example.com/yesterday",
            published_date=timezone.now() - timedelta(days=1),
            guid="yesterday-guid",
        )

        assert today_article.is_published_today() is True
        assert yesterday_article.is_published_today() is False

    def test_unique_constraints(self):
        """Test unique constraints on link and guid."""
        NewsArticle.objects.create(
            title="First Article",
            link="https://example.com/unique",
            published_date=timezone.now(),
            guid="unique-guid",
        )

        # Attempting to create with same link should fail
        with pytest.raises(Exception):
            NewsArticle.objects.create(
                title="Second Article",
                link="https://example.com/unique",
                published_date=timezone.now(),
                guid="another-guid",
            )

        # Attempting to create with same guid should fail
        with pytest.raises(Exception):
            NewsArticle.objects.create(
                title="Third Article",
                link="https://example.com/different",
                published_date=timezone.now(),
                guid="unique-guid",
            )

    def test_string_representation(self):
        """Test __str__ method."""
        article = NewsArticle.objects.create(
            title="Test Title",
            link="https://example.com/test",
            published_date=timezone.now(),
            guid="test-guid",
        )

        str_repr = str(article)
        assert "Test Title" in str_repr
        assert article.published_date.strftime("%Y-%m-%d") in str_repr

    def test_ordering(self):
        """Test articles are ordered by published_date descending."""
        old_article = NewsArticle.objects.create(
            title="Old Article",
            link="https://example.com/old",
            published_date=timezone.now() - timedelta(days=2),
            guid="old-guid",
        )

        new_article = NewsArticle.objects.create(
            title="New Article",
            link="https://example.com/new",
            published_date=timezone.now(),
            guid="new-guid",
        )

        articles = list(NewsArticle.objects.all())
        assert articles[0] == new_article
        assert articles[1] == old_article
