# RSS Final Project

## Description 

RSS reader should store news in local cache and perform news filtering by publication date.

- The RSS news should be stored in a local storage while reading. 
  - The way and format of this storage you can choose yourself.
  - Please describe it in a separate section of README.md or in the documentation.

- Reader should support read news from cache, so news from the specified day will be printed out.

  - Date should be specified in a new optional argument `--date`. 
    - It should take a date in `%Y%m%d` format.
    - For example: `--date 20191020`

  - Here date means actual *publishing date* not the date when you fetched the news.
  - If the news are not found return an error.
  - If the `--date` argument is not provided, the utility should work like in the previous iterations, and store news to cache

- It is recommended to use PySpark or Pandas to work with local cache

**Task clarification**
1) Try to make your application crossplatform, meaning that it should work on both Linux and Windows. For example when working with filesystem, try to use `os.path` lib instead of manually concatenating file paths.
2) `--date` should **not** require internet connection to fetch news from local cache.
3) User should be able to use `--date` without specifying RSS source. For example:
 `python rss_reader.py --date 20191206`
4) If `--date` specified together with RSS source, then app should get news for this date from local cache that were fetched from specified source.
5) `--date` should work correctly with both `--json`, `--limit`, `--verbose` and their different combinations.


## Installation

To install the necessary dependencies for this project, make sure you have Python and pip installed on your system, then run:

```bash
pip install -r requirements.txt
```

## Usage
Certainly, here's a properly formatted "Usage" section for your `README.md`, highlighting the main flags and their applications in your RSS Reader:

---

## Usage

This RSS Reader is a command-line utility designed to fetch and cache news from specified RSS feeds. Here's how you can utilize the main flags to control its behavior:

### Fetching News from a Source

To fetch news from a specific RSS feed source, use the `--source` or `-s` flag followed by the RSS feed URL:

```sh
python -m src.main --source https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml
```

### Retrieving Cached News by Date

You can retrieve news from the local cache for a specific date using the `--date`- or `-d` flag with the date in `YYYYMMDD` format. This can be used without specifying a source to get news from all cached sources on that date:

```sh
python -m src.main --date 20240403
```

### Limiting the Number of Results

To limit the number of news results, utilize the `--limit` or `-l` flag followed by the number of news items you wish to retrieve or fetch:

```sh
python -m src.main --source https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml --limit 5
```

### Outputting Results in JSON Format

For outputting the news in JSON format, which is useful for processing by other programs, add the `--json` or `-j` flag:

```sh
python -m src.main --source https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml --json
```

### Increasing Output Verbosity

If you require more detailed output information, include the `--verbose` or `-v` flag. This will provide additional details about the news items and the fetching process:

```sh
python -m src.main --source https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml --verbose
```

### Combining Flags

Flags can be combined to tailor the RSS Reader's functionality to your needs. For example, to fetch up to 10 news items from a specific source for a given date, output them in JSON format, and include verbose output, you would run:

```sh
python -m src.main --source https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml --date 20240403 --limit 10 --json --verbose
```

---

This format provides a clean, easy-to-read guide on utilizing your RSS Reader's capabilities through its command-line interface, enabling users to quickly understand and use the tool's main features.


## Testing

The project includes comprehensive tests, covering approximately 93% of the code. To run the tests, ensure you're in the project's root directory and execute:

```bash
pytest
```

For detailed coverage reports, run:

```bash
pytest --cov=src tests/
```

This will generate a coverage report, outlining which parts of the code are covered by tests and any areas that might need additional testing.


