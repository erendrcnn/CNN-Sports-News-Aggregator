"""
Simple standalone script to fetch and display CNN Sports headlines.
This demonstrates the core functionality without Django.

Usage:
    python fetch_news.py
"""

import feedparser
import pytz
from datetime import datetime
from dateutil import parser as date_parser


def fetch_cnn_sports_news():
    """
    Fetch sports news headlines from CNN RSS feed.
    
    Returns:
        List of articles published today
    """
    RSS_URL = "http://rss.cnn.com/rss/edition_sport.rss"
    
    print(f"Fetching sports news from CNN RSS feed...")
    print(f"URL: {RSS_URL}\n")
    
    try:
        # Parse the RSS feed
        feed = feedparser.parse(RSS_URL)
        
        if feed.bozo:
            print(f"Error parsing feed: {feed.bozo_exception}")
            return []
        
        # Get today's date
        today = datetime.now(pytz.UTC).date()
        
        # Filter and display articles
        today_articles = []
        
        for entry in feed.entries:
            # Parse publication date
            pub_date_str = entry.get('published', entry.get('updated', ''))
            if not pub_date_str:
                continue
            
            try:
                # Convert to string if it's a list or other type
                if isinstance(pub_date_str, list):
                    pub_date_str = pub_date_str[0] if pub_date_str else ''
                pub_date_str = str(pub_date_str)
                
                pub_date = date_parser.parse(pub_date_str)
                if pub_date.tzinfo is None:
                    pub_date = pytz.UTC.localize(pub_date)
                
                # Check if published today
                if pub_date.date() == today:
                    article = {
                        'title': entry.get('title', 'No Title'),
                        'link': entry.get('link', 'No Link'),
                        'published_date': pub_date,
                        'description': entry.get('summary', 'No Description'),
                    }
                    today_articles.append(article)
            except Exception as e:
                print(f"Error parsing date: {e}")
                continue
        
        return today_articles
        
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []


def display_articles(articles):
    """
    Display articles in a formatted way.
    
    Args:
        articles: List of article dictionaries
    """
    if not articles:
        print("No articles published today.")
        return
    
    print(f"Found {len(articles)} article(s) published today:\n")
    print("=" * 80)
    
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Link: {article['link']}")
        print(f"   Published: {article['published_date'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
        if article['description']:
            # Truncate description to 200 characters
            desc = article['description'][:200]
            if len(article['description']) > 200:
                desc += "..."
            print(f"   Description: {desc}")
        print("-" * 80)


def main():
    """Main function."""
    print("\n" + "=" * 80)
    print("CNN SPORTS NEWS AGGREGATOR")
    print("Fetching today's sports headlines...")
    print("=" * 80 + "\n")
    
    articles = fetch_cnn_sports_news()
    display_articles(articles)
    
    print(f"\n{'=' * 80}")
    print("End of results")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
