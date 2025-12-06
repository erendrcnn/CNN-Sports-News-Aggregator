"""
Views for news application.

Following Single Responsibility and Dependency Inversion Principles.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging

from .models import NewsArticle
from .serializers import NewsArticleSerializer, NewsArticleListSerializer
from .services import NewsService, CNNSportsFeedFetcher


logger = logging.getLogger(__name__)


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for news articles.

    Provides:
    - list: Get all news articles (with pagination)
    - retrieve: Get a single news article
    - today: Get today's news articles
    - refresh: Manually trigger news fetch
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == "list":
            return NewsArticleListSerializer
        return NewsArticleSerializer

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """List all news articles."""
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def today(self, request):
        """
        Get today's news articles.

        Endpoint: GET /api/news/today/
        """
        try:
            # Initialize service with CNN fetcher
            fetcher = CNNSportsFeedFetcher()
            service = NewsService(fetcher)

            # Get today's articles from database
            articles = service.get_today_news()

            # Serialize and return
            serializer = self.get_serializer(articles, many=True)

            return Response({"count": len(articles), "results": serializer.data})

        except Exception as e:
            logger.error(f"Error fetching today's news: {str(e)}")
            return Response(
                {"error": "Failed to fetch today's news"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        """
        Manually trigger news fetch from RSS feed.

        Endpoint: POST /api/news/refresh/
        Optional query params:
        - all=1          -> save all fetched items (no today-only filter)
        - days=<int>     -> when all=1, limit response to recent N days (default 7)
        """
        try:
            # Initialize service with CNN fetcher
            fetcher = CNNSportsFeedFetcher()
            service = NewsService(fetcher)

            # Determine filtering behavior
            all_param = request.query_params.get("all")
            days_param = request.query_params.get("days")
            fetch_all = str(all_param).lower() in ("1", "true", "yes")

            # Fetch and store news (disable today filter when fetching all)
            saved_count = service.fetch_and_store_news(filter_today=not fetch_all)

            # Build response dataset
            if fetch_all:
                try:
                    days = int(days_param) if days_param is not None else 7
                    days = max(1, min(days, 90))  # clamp 1..90
                except (TypeError, ValueError):
                    days = 7
                articles = service.repository.get_recent_articles(days=days)
            else:
                articles = service.get_today_news()
            serializer = self.get_serializer(articles, many=True)

            return Response(
                {
                    "message": f"Successfully fetched and saved {saved_count} new articles",
                    "count": len(articles),
                    "results": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error refreshing news: {str(e)}")
            return Response(
                {"error": "Failed to refresh news"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
