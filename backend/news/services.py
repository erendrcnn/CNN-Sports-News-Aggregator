"""
Service layer for news fetching and processing.

Following SOLID Principles:
- Single Responsibility: Each class has one specific purpose
- Open/Closed: Extensible for new feed sources without modification
- Liskov Substitution: Abstract base class for feed fetchers
- Interface Segregation: Focused interfaces for specific tasks
- Dependency Inversion: Depends on abstractions, not concrete implementations
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

import feedparser
import pytz
from dateutil import parser as date_parser
from django.conf import settings
from django.utils import timezone

from .models import NewsArticle


logger = logging.getLogger(__name__)


class INewsFeedFetcher(ABC):
    """
    Abstract base class for news feed fetchers.

    Implements Dependency Inversion Principle:
    - High-level modules depend on this abstraction
    - Can be extended for different feed sources
    """

    @abstractmethod
    def fetch_feed(self) -> List[Dict]:
        """Fetch and parse feed entries."""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the news source."""
        pass


class CNNSportsFeedFetcher(INewsFeedFetcher):
    """
    Concrete implementation for CNN Sports RSS feed.

    Single Responsibility: Fetches and parses CNN Sports RSS feed only.
    """

    def __init__(self, feed_url: Optional[str] = None):
        self.feed_url = feed_url or settings.CNN_SPORTS_RSS_URL

    def fetch_feed(self) -> List[Dict]:
        """
        Fetch and parse CNN Sports RSS feed.

        Returns:
            List of dictionaries containing article data
        """
        try:
            logger.info(f"Fetching RSS feed from {self.feed_url}")
            feed = feedparser.parse(self.feed_url)

            if feed.bozo:
                logger.error(f"Feed parsing error: {feed.bozo_exception}")
                return []

            articles = []
            for entry in feed.entries:
                article_data = self._parse_entry(entry)
                if article_data:
                    articles.append(article_data)

            logger.info(f"Successfully fetched {len(articles)} articles")
            return articles

        except Exception as e:
            logger.error(f"Error fetching RSS feed: {str(e)}")
            return []

    def _parse_entry(self, entry) -> Optional[Dict]:
        """
        Parse a single RSS entry.

        Args:
            entry: feedparser entry object

        Returns:
            Dictionary with article data or None if parsing fails
        """
        try:
            # Parse publication date
            published_date = self._parse_date(entry)
            if not published_date:
                return None

            return {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "published_date": published_date,
                "guid": entry.get("id", entry.get("link", "")),
            }
        except Exception as e:
            logger.warning(f"Error parsing entry: {str(e)}")
            return None

    def _parse_date(self, entry) -> Optional[datetime]:
        """
        Parse publication date from entry.

        Args:
            entry: feedparser entry object

        Returns:
            Timezone-aware datetime object or None
        """
        date_str = entry.get("published", entry.get("updated", ""))
        if not date_str:
            return None

        try:
            parsed_date = date_parser.parse(date_str)

            # Ensure timezone awareness
            if parsed_date.tzinfo is None:
                parsed_date = pytz.UTC.localize(parsed_date)

            return parsed_date
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {str(e)}")
            return None

    def get_source_name(self) -> str:
        """Return the source name."""
        return "CNN Sports"


class TodayArticleFilter:
    """
    Filter for articles published today.

    Single Responsibility: Filters articles based on publication date.
    """

    @staticmethod
    def filter(articles: List[Dict]) -> List[Dict]:
        """
        Filter articles to only those published today.

        Args:
            articles: List of article dictionaries

        Returns:
            Filtered list of articles published today
        """
        today = timezone.now().date()

        filtered = [
            article
            for article in articles
            if article.get("published_date")
            and article["published_date"].date() == today
        ]

        logger.info(f"Filtered to {len(filtered)} articles published today")
        return filtered


class NewsArticleRepository:
    """
    Repository for NewsArticle database operations.

    Single Responsibility: Handles all database operations for news articles.
    """

    @staticmethod
    def save_articles(articles: List[Dict], source: str) -> int:
        """
        Save articles to database, avoiding duplicates.

        Args:
            articles: List of article dictionaries
            source: Source name for the articles

        Returns:
            Number of new articles saved
        """
        saved_count = 0

        for article_data in articles:
            try:
                # Check if article already exists
                if NewsArticle.objects.filter(guid=article_data["guid"]).exists():
                    continue

                # Create new article
                NewsArticle.objects.create(
                    title=article_data["title"],
                    link=article_data["link"],
                    description=article_data["description"],
                    published_date=article_data["published_date"],
                    guid=article_data["guid"],
                    source=source,
                )
                saved_count += 1

            except Exception as e:
                logger.error(f"Error saving article: {str(e)}")
                continue

        logger.info(f"Saved {saved_count} new articles to database")
        return saved_count

    @staticmethod
    def get_today_articles() -> List[NewsArticle]:
        """
        Retrieve all articles published today.

        Returns:
            List of NewsArticle objects
        """
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        return list(
            NewsArticle.objects.filter(
                published_date__gte=today, published_date__lt=tomorrow
            ).order_by("-published_date")
        )

    @staticmethod
    def get_recent_articles(days: int = 7) -> List[NewsArticle]:
        """
        Retrieve articles from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of NewsArticle objects
        """
        start_date = timezone.now() - timedelta(days=days)

        return list(
            NewsArticle.objects.filter(published_date__gte=start_date).order_by(
                "-published_date"
            )
        )


class NewsService:
    """
    Main service for news operations.

    Open/Closed Principle: Open for extension (new fetchers) but closed for modification.
    Dependency Inversion: Depends on INewsFeedFetcher abstraction.
    """

    def __init__(self, fetcher: INewsFeedFetcher):
        self.fetcher = fetcher
        self.repository = NewsArticleRepository()

    def fetch_and_store_news(self, filter_today: bool = False) -> int:
        """
        Fetch news from feed and store in database.

        Args:
            filter_today: If True, only store articles published today (default False to fetch all recent)

        Returns:
            Number of articles saved
        """
        # Fetch articles from feed
        articles = self.fetcher.fetch_feed()

        if not articles:
            logger.warning("No articles fetched from feed")
            return 0

        # Filter to today's articles if requested
        if filter_today:
            articles = TodayArticleFilter.filter(articles)

        # Save to database
        source_name = self.fetcher.get_source_name()
        saved_count = self.repository.save_articles(articles, source_name)

        return saved_count

    def get_today_news(self) -> List[NewsArticle]:
        """
        Get today's news articles from database.

        Returns:
            List of NewsArticle objects
        """
        return self.repository.get_today_articles()
