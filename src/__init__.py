"""
RSS Reader Package

This package implements a command-line RSS reader. The RSS Reader fetches news articles from specified RSS feed URLs,
caches them locally, and allows users to filter news by date, limit the number of articles displayed, and choose between
textual or JSON output. The package supports increased verbosity for debugging purposes and can retrieve cached news
from all sources for a given date.

Modules:
    main.py: Parses command-line arguments and orchestrates the fetching, caching, and displaying of news articles.
    rss_reader.py: Contains functions for parsing RSS feeds.
    cache_manager.py: Manages the local cache of news articles, including saving and retrieving.
    utils.py: Provides utility functions.

"""
