"""
Serializers for news application.

Following Interface Segregation Principle:
- Each serializer has a focused, specific purpose
"""

from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for NewsArticle model.

    Provides JSON representation of news articles for API responses.
    """

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "link",
            "published_date",
            "description",
            "source",
            "fetched_at",
        ]
        read_only_fields = ["id", "fetched_at"]


class NewsArticleListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing news articles.

    Excludes description for better performance in list views.
    """

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "link",
            "published_date",
            "source",
        ]
        read_only_fields = fields
