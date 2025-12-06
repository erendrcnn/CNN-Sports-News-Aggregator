#!/usr/bin/env python
import feedparser

feed_url = 'http://rss.cnn.com/rss/edition_sport.rss'
feed = feedparser.parse(feed_url)

print(f"Feed Title: {feed.feed.get('title', 'N/A')}")
print(f"Total Entries: {len(feed.entries)}")
print(f"Bozo: {feed.bozo}")
if feed.bozo:
    print(f"Bozo Exception: {feed.bozo_exception}")

print("\nFirst 3 articles:")
for i, entry in enumerate(feed.entries[:3]):
    print(f"\n{i+1}. Title: {entry.get('title', 'N/A')}")
    print(f"   Link: {entry.get('link', 'N/A')}")
    print(f"   Published: {entry.get('published', 'N/A')}")
