from src.utils import complex_to_simple_date, simple_to_readable_date, log_verbose


def test_complex_to_simple_date():
    """
    Tests the conversion from a complex date format to a simple YYYYMMDD format.
    """
    input_date = "Mon, 29 Jun 2020 22:10:00 +0300"
    expected_date = "20200629"
    assert complex_to_simple_date(input_date) == expected_date


def test_simple_to_readable_date():
    """
    Tests the conversion from a simple YYYYMMDD date format to a more readable format.
    """
    input_date = "20200629"
    expected_date = "2020-June-29"
    assert simple_to_readable_date(input_date) == expected_date


def test_log_verbose_output(capsys):
    """
    Verifies that `log_verbose` correctly outputs a message when in verbose mode and suppresses output otherwise.
    """
    # Test verbose output
    log_verbose("Verbose message", True)
    captured = capsys.readouterr()
    assert "Verbose message" in captured.out

    # Test non-verbose output
    log_verbose("Should not print", False)
    captured = capsys.readouterr()
    assert "Should not print" not in captured.out


def test_log_verbose_no_output(capsys):
    """
    Ensures that `log_verbose` produces no output when not in verbose mode.
    """
    log_verbose("No output expected", False)
    captured = capsys.readouterr()
    assert captured.out == ""
