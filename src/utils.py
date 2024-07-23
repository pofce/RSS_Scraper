from datetime import datetime


def complex_to_simple_date(date_str: str) -> str:
    """Converts input date format to the simplet one use in command line"""
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')


def simple_to_readable_date(date_str: str) -> str:
    """Converts command line data format to more readable format"""
    return datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%B-%d')


def log_verbose(message: str, verbose) -> None:
    """Prints a message only if verbose mode is enabled."""
    if verbose:
        print(message)
