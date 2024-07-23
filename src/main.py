import argparse
import requests
import json
from src.cache_manager import CacheManager
from src.rss_reader import rss_parser
from src.utils import simple_to_readable_date, log_verbose
from typing import Dict, List


def fetch_rss_xml(url: str) -> str:
    """Fetches RSS XML data from the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return ""


def print_news(news_items: List[Dict[str, str]], to_json: bool = False, verbose: bool = False) -> None:
    """
    Prints the news items in JSON format or a formatted string based on the input flags.

    Args:
    - news_items: A list of dictionaries, where each dictionary represents a news item.
    - to_json: If True, prints news items in JSON format. Otherwise, prints as formatted strings.
    - verbose: Determines the level of detail in the printed output. Less detail if False.

    For non-JSON output in non-verbose mode, only the title, link, and publication date are printed.
    """

    if not verbose:
        concise_keys = ("title", "link", "pubDate")
        news_items = [{tag: value for tag, value in item.items() if tag in concise_keys} for item in news_items]

    for item in news_items:
        item["pubDate"] = simple_to_readable_date(date_str=item.get("pubDate", ""))

    if to_json:
        print(json.dumps(news_items, indent=2))
    else:
        tags_map = {
            "title": "Title",
            "author": "Authors",
            "link": "Link",
            "pubDate": "Publish Date",
            "description": "Description",
            "category": "Categories",
            "source_url": "Source URL"
        }
        for item in news_items:
            print("\n".join([f"{tags_map[key]}: {value}" for key, value in item.items()]), end="\n\n")


def main():
    """
    Parses command line arguments and fetches or displays news based on those arguments.

    Supports fetching news from an RSS source or retrieving cached news by date. Output can
    be formatted as JSON or as a more human-readable string, with optional verbosity.
    """
    parser = argparse.ArgumentParser(description='RSS Reader - Fetch and read RSS feeds.')
    parser.add_argument('-s', '--source', help='RSS URL source', default=None)
    parser.add_argument('-d', '--date', help='Date in YYYYMMDD format to retrieve news from cache', default=None)
    parser.add_argument('-l', '--limit', help='Limit the number of news results', type=int, default=None)
    parser.add_argument('-j', '--json', action='store_true', help='Print result as JSON in stdout', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='Increases verbosity of output', default=False)
    args = parser.parse_args()

    verbose_mode = args.verbose

    cache_manager = CacheManager()

    if args.date:
        log_verbose(message="Fetching news from cache...", verbose=verbose_mode)
        # Fetching news from cache based on date (and source if provided)
        if cached_news := cache_manager.retrieve_news_from_cache(date=args.date, source_url=args.source):
            print_news(news_items=cached_news, to_json=args.json, verbose=verbose_mode)
        else:
            print("No news found for the specified date.")

    elif args.source:
        log_verbose(message=f"Fetching news from source: {args.source}", verbose=verbose_mode)
        # Fetching news from the specified RSS source and caching it
        if xml_data := fetch_rss_xml(url=args.source):
            news_items = rss_parser(xml=xml_data, limit=args.limit)
            cache_manager.cache_news(news_items=news_items, source_url=args.source, verbose=verbose_mode)
            print_news(news_items=news_items, to_json=args.json, verbose=verbose_mode)
        else:
            print("Failed to fetch news from the source.")

    else:
        print("Please provide an RSS source URL or a date to fetch news from cache.")


if __name__ == "__main__":
    main()
