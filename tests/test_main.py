from src.main import fetch_rss_xml, print_news, main
from requests.exceptions import HTTPError
from unittest.mock import patch
import json
import pytest


@pytest.fixture()
def mock_args(monkeypatch):
    """
    Fixture to mock command-line arguments using monkeypatch.
    """
    def _mock_args(args_list):
        monkeypatch.setattr('sys.argv', args_list)
    return _mock_args


@patch('src.main.fetch_rss_xml')
def test_main_fetch_from_source(mock_fetch, mock_args, capsys):
    """
    Test `main` function's ability to handle '--source' argument and fetch RSS XML.
    """
    mock_args(['main.py', '--source', 'https://example.com/feed'])
    mock_fetch.return_value = """<rss><channel><item><title>Test Title</title>
    <pubDate>Wed, 02 Oct 2002 15:00:00 +0200</pubDate></item></channel></rss>"""

    main()
    mock_fetch.assert_called_with(url='https://example.com/feed')
    captured = capsys.readouterr()

    assert "Test Title" in captured.out
    assert "2002-October-02" in captured.out


@patch('src.main.CacheManager')
def test_main_fetch_from_cache(mock_cache_manager, mock_args, capsys):
    """
    Test `main` function's ability to retrieve news from cache using '--date' argument.
    """
    mock_args(['main.py', '--date', '20210101'])
    instance = mock_cache_manager.return_value
    instance.retrieve_news_from_cache.return_value = [{
        'title': 'Cached Title',
        'link': 'http://cached.example.com',
        'pubDate': '20210101'
    }]

    main()
    instance.retrieve_news_from_cache.assert_called_with(date='20210101', source_url=None)
    captured = capsys.readouterr()

    assert "Cached Title" in captured.out


@patch('src.main.fetch_rss_xml')
def test_main_with_json_output(mock_fetch, mock_args, capsys):
    """
    Test `main` function's ability to output news in JSON format with '--json' argument.
    """
    mock_args(['main.py', '--source', 'https://example.com/feed', '--json'])
    mock_fetch.return_value = """<rss><channel><item><title>Test Title</title>
    <pubDate>Wed, 02 Oct 2002 15:00:00 +0200</pubDate></item></channel></rss>"""
    main()
    assert '2002-October-02' in capsys.readouterr().out


@patch('src.main.requests.get')
def test_fetch_rss_xml_success(mock_get):
    """
    Test successful RSS XML fetch operation from a URL.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<rss>some content</rss>"
    url = "http://example.com/rss"
    result = fetch_rss_xml(url)
    assert result == "<rss>some content</rss>"
    mock_get.assert_called_with(url)


@patch('src.main.requests.get')
def test_fetch_rss_xml_http_error(mock_get):
    """
    Test handling of HTTP errors during RSS XML fetch operation.
    """
    mock_get.side_effect = HTTPError
    url = "http://example.com/rss"
    result = fetch_rss_xml(url)
    assert result == ""


def test_print_news_json(capsys):
    """
    Test `print_news` function's ability to print news items in JSON format.
    """
    news_items = [
        {'title': 'Test Title 1', 'link': 'http://example.com/1', 'pubDate': '20210101'},
        {'title': 'Test Title 2', 'link': 'http://example.com/2', 'pubDate': '20210102'}
    ]

    proper_output = [
        {'title': 'Test Title 1', 'link': 'http://example.com/1', 'pubDate': '2021-January-01'},
        {'title': 'Test Title 2', 'link': 'http://example.com/2', 'pubDate': '2021-January-02'}
    ]

    print_news(news_items, to_json=True)

    captured = capsys.readouterr()
    output = json.loads(captured.out)

    assert output == proper_output


def test_print_news_text(capsys):
    """
    Test `print_news` function's ability to print news items as formatted text.
    """
    news_items = [{'title': 'Test Title', 'link': 'http://example.com', 'pubDate': '20210101'}]
    print_news(news_items, to_json=False)

    captured = capsys.readouterr()
    expected_output = "Title: Test Title\nLink: http://example.com\nPublish Date: 2021-January-01\n\n"
    assert captured.out == expected_output


def test_print_news_text_verbose(capsys):
    """
    Test `print_news` function's verbose mode, ensuring additional information is printed.
    """
    news_items = [
        {
            'title': 'Test Title',
            'link': 'http://example.com',
            'pubDate': '20210101',
            'description': 'Test Description',
            'author': 'Test Author',
            'category': 'Test Category',
            'source_url': 'http://source.com'
        }
    ]

    print_news(news_items, to_json=False, verbose=True)

    captured = capsys.readouterr()

    assert "Description: Test Description" in captured.out
    assert "Authors: Test Author" in captured.out
    assert "Categories: Test Category" in captured.out
    assert "Source URL: http://source.com" in captured.out
