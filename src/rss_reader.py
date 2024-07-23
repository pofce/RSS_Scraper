from bs4 import BeautifulSoup, Tag
from typing import List, Optional, Dict, Any
from src.utils import complex_to_simple_date


def parse_item(item: Tag) -> Dict[str, Any]:
    """
    Extracts details from a single RSS feed item into a dictionary.

    Args: - item: A BeautifulSoup Tag of the RSS feed item.
    """
    tags = ("title", "author", "pubDate", "link", "category", "description")

    item_info = {}
    for tag in tags:
        element = item.find(tag)
        if element and element.text:
            match tag:
                case "author" | "category":
                    item_info[tag] = [cat.text for cat in item.find_all(tag)]
                case "pubDate":
                    item_info[tag] = complex_to_simple_date(element.text)
                case _:
                    item_info[tag] = element.text
    return item_info


def rss_parser(xml: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Parses RSS feed XML, returning a list of item dictionaries.

    Args:
    - xml: XML string of the RSS feed.
    - limit: Max number of items to parse (None for no limit).

    Returns: List of dictionaries, each representing an RSS feed item.
    """
    soup = BeautifulSoup(xml, 'lxml-xml')
    return [parse_item(item) for item in soup.find_all('item', limit=limit)]


if __name__ == "__main__":
    # Ctearted for the testing purpose
    import requests
    print(*rss_parser(requests.get("https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml").text, limit=5), sep="\n")
