from bs4 import BeautifulSoup
from src.rss_reader import parse_item, rss_parser
from src.utils import complex_to_simple_date


sample_item_xml = """
<item>
    <title>Sample Title</title>
    <link>http://example.com/sample-post</link>
    <description>Sample Description</description>
    <author>Sample Author</author>
    <category>Sample Category</category>
    <pubDate>Wed, 02 Oct 2002 15:00:00 +0200</pubDate>
</item>
"""


def create_tag_from_string(xml_string):
    """
    Creates a BeautifulSoup Tag from an XML string.
    """
    soup = BeautifulSoup(xml_string, 'lxml-xml')
    return soup.find('item')


def test_parse_item():
    """
    Validates parsing of an RSS item into a structured dictionary.

    Checks that each field of an RSS item is correctly extracted and
    converted as expected, including complex fields like dates.
    """
    item_tag = create_tag_from_string(sample_item_xml)
    parsed_item = parse_item(item_tag)

    assert parsed_item['title'] == 'Sample Title'
    assert parsed_item['link'] == 'http://example.com/sample-post'
    assert parsed_item['description'] == 'Sample Description'
    assert parsed_item['author'] == ['Sample Author']
    assert parsed_item['category'] == ['Sample Category']
    assert parsed_item['pubDate'] == complex_to_simple_date('Wed, 02 Oct 2002 15:00:00 +0200')
    assert len(parsed_item) == 6


def test_rss_parser():
    """
    Tests the RSS feed parsing with a limit on the number of items.

    Verifies that the 'rss_parser' function correctly parses a given
    XML string representing an RSS feed and respects the specified item limit.
    """
    sample_feed_xml = f"""<rss><channel>{sample_item_xml * 3}</channel></rss>"""
    parsed_feed = rss_parser(sample_feed_xml, limit=2)
    assert len(parsed_feed) == 2
