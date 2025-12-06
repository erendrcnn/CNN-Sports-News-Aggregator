"""
Models for news application.

Following Single Responsibility Principle:
- NewsArticle: Represents a single news article entity
"""

from django.db import models
from django.utils import timezone


class NewsArticle(models.Model):
    """
    Model representing a news article from RSS feed.

    Attributes:
        title: Article headline
        link: URL to the full article
        published_date: Publication date and time
        description: Article summary/description
        source: Source of the article (e.g., 'CNN Sports')
        guid: Unique identifier from RSS feed
        fetched_at: Timestamp when article was fetched
    """

    title = models.CharField(max_length=500)
    link = models.URLField(max_length=1000, unique=True)
    published_date = models.DateTimeField()
    description = models.TextField(blank=True)
    source = models.CharField(max_length=100, default="CNN Sports")
    guid = models.CharField(max_length=500, unique=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["-published_date"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.published_date.strftime('%Y-%m-%d')}"

    def is_published_today(self):
        """Check if article was published today."""
        today = timezone.now().date()
        return self.published_date.date() == today
