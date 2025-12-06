from django.contrib import admin
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    """Admin interface for NewsArticle model."""

    list_display = ["title", "source", "published_date", "fetched_at"]
    list_filter = ["source", "published_date", "fetched_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["fetched_at"]
    date_hierarchy = "published_date"

    fieldsets = (
        ("Article Information", {"fields": ("title", "link", "description", "guid")}),
        ("Metadata", {"fields": ("source", "published_date", "fetched_at")}),
    )
