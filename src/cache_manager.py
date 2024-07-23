import pandas as pd
from os import path
from typing import Dict, List
from src.utils import log_verbose


class CacheManager:
    """
    A cache manager for storing and retrieving news items using a CSV file as the storage medium.

    Attributes:
    - cache_file: The path to the CSV file used for caching news items.
    """
    def __init__(self, cache_file='data/news_cache.csv'):
        """Initializes the CacheManager with a specific cache file location."""
        self.cache_file = cache_file

    def cache_news(self, news_items: List[Dict[str, any]], source_url: str, verbose: bool) -> None:
        """
        Caches news items to the specified CSV file, adding a source URL to each item.

        Args:
        - news_items: A list of dictionaries, where each dictionary
         represents a news item with keys corresponding to news attributes.
        - source_url: The URL of the source from which the news items were fetched.

        Exception: If there's an error during the caching process.
        """
        try:
            if path.exists(self.cache_file):
                cache_df = pd.read_csv(self.cache_file)
            else:
                cache_df = pd.DataFrame(columns=["title", "author", "pubDate", "link", "category", "description"])

            new_items_df = pd.DataFrame.from_records(news_items)
            new_items_df['source_url'] = source_url

            cache_df = pd.concat([cache_df, new_items_df], ignore_index=True).drop_duplicates(subset=['link'])
            cache_df.to_csv(self.cache_file, index=False)

            log_verbose(message="News items cached successfully.", verbose=verbose)
        except Exception as e:
            print(f"Error caching news items: {e}")

    def retrieve_news_from_cache(self, date, source_url=None) -> Dict[str, any]:
        """
        Retrieves news items from the cache filtered by date and optionally by source URL.

        Args:
        - date: Publication date to filter by.
        - source_url: Source URL to further filter by, optional.

        Returns: Filtered list of news item dictionaries.
        """
        if not path.exists(self.cache_file):
            print("Cache file does not exist.")
            return []

        cache_df = pd.read_csv(self.cache_file, dtype={"pubDate": str})

        filter_condition = cache_df['pubDate'].str.contains(date)
        if source_url:
            filter_condition &= (cache_df['source_url'] == source_url)

        return cache_df[filter_condition].to_dict('records')
