import pytest
from src.cache_manager import CacheManager
import pandas as pd
from pathlib import Path


@pytest.fixture
def cache_manager(tmp_path):
    """
    Provides a CacheManager instance with a temporary cache file for isolation in tests.
    """
    cache_file = tmp_path / "test_news_cache.csv"
    return CacheManager(cache_file=str(cache_file))


@pytest.fixture
def sample_news_items():
    """
    Returns a list of sample news items for testing cache operations.
    """
    return [
        {
            "title": "Test News 1",
            "author": "Author 1",
            "pubDate": "20240101",
            "link": "http://example.com/news1",
            "category": "Category 1",
            "description": "Description 1"
        },
        {
            "title": "Test News 2",
            "author": "Author 2",
            "pubDate": "20240102",
            "link": "http://example.com/news2",
            "category": "Category 2",
            "description": "Description 2"
        },
    ]


def test_cache_news_creates_new_file(cache_manager, sample_news_items):
    """
    Ensures CacheManager creates a new cache file if one doesn't already exist.
    """
    cache_file_path = Path(cache_manager.cache_file)
    assert not cache_file_path.exists()
    cache_manager.cache_news(sample_news_items, "http://example.com", verbose=False)
    assert cache_file_path.exists()


def test_cache_news_adds_to_existing_cache(cache_manager, sample_news_items):
    """
    Tests that news items are added to an existing cache without creating duplicates.
    """
    cache_manager.cache_news(sample_news_items, "http://example.com", verbose=False)
    cache_manager.cache_news(sample_news_items, "http://example.com", verbose=False)

    cached_data = pd.read_csv(cache_manager.cache_file)

    assert cached_data.duplicated(subset=['link']).sum() == 0
    assert len(cached_data) == len(sample_news_items)


def test_retrieve_news_from_cache_by_date(cache_manager, sample_news_items):
    """
    Verifies that news items can be retrieved from the cache based on their publication date.
    """
    cache_manager.cache_news(sample_news_items, "http://example.com", verbose=False)
    filtered_news = cache_manager.retrieve_news_from_cache("20240101")

    assert all(item['pubDate'] == "20240101" for item in filtered_news)


def test_retrieve_news_from_cache_by_date_and_source(cache_manager, sample_news_items):
    """
    Checks retrieval of news items from the cache by both publication date and source URL.
    """
    cache_manager.cache_news(sample_news_items, "http://example.com", verbose=False)
    filtered_news = cache_manager.retrieve_news_from_cache("20240101", source_url="http://example.com")

    assert all(item['pubDate'] == "20240101" and item['source_url'] == "http://example.com" for item in filtered_news)
