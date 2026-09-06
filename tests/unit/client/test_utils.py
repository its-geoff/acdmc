"""Tests for the utils module."""

# Standard library imports
import math
import re
from datetime import datetime

import pytest

# Local imports
import utils


@pytest.fixture
def today_date() -> datetime:
    """Fixture that provides today's date as a datetime object.
    
    Returns:
        datetime: Today's date at midnight.
    """
    midnight = datetime.min.time()
    return datetime.combine(datetime.now().date(), midnight)


@pytest.mark.utils_smoke
def test_generate_uuid_not_empty():
    """Test that generate_uuid returns a non-empty string."""
    uuid_str = utils.generate_uuid()
    assert uuid_str, "UUID should not be empty"


@pytest.mark.utils_smoke
def test_generate_uuid_format():
    """Test that generate_uuid returns a properly formatted UUID."""
    uuid_str = utils.generate_uuid()
    uuid_regex = re.compile(
        r"^[0-9a-f]{8}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{12}$"
    )
    assert uuid_regex.match(uuid_str), "UUID should match standard format"


@pytest.mark.utils_smoke
def test_generate_uuid_length():
    """Test that generate_uuid returns a UUID of correct length."""
    uuid_str = utils.generate_uuid()
    assert len(uuid_str) == 36, "UUID should be 36 characters long"


@pytest.mark.utils_smoke
def test_validate_date_order():
    """Test that validate_date_order raises error when start date is after end date."""
    start_date = datetime(2026, 2, 20)
    end_date = datetime(2026, 1, 18)
    with pytest.raises(ValueError, match="End date cannot be before start date"):
        utils.validate_date_order(start_date, end_date)


@pytest.mark.utils_smoke
def test_bool_to_string():
    """Test that bool_to_string converts boolean values correctly."""
    assert utils.bool_to_string(True) == "Yes"
    assert utils.bool_to_string(False) == "No"


@pytest.mark.utils_smoke
def test_default_start_date(today_date):
    """Test that default_start_date returns today's date."""
    result = utils.default_start_date()
    assert result == today_date, "Default start date should be today"


@pytest.mark.utils_smoke
def test_default_end_date(today_date):
    """Test that default_end_date returns start date + 4 months."""
    result = utils.default_end_date(today_date)
    # Calculate expected date by adding 4 months
    year = today_date.year + (today_date.month + 4 - 1) // 12
    month = (today_date.month + 4 - 1) % 12 + 1
    expected = datetime(year, month, today_date.day)
    assert result == expected


@pytest.mark.utils_smoke
def test_validate_req_string():
    """Test that validate_req_string returns valid string."""
    result = utils.validate_req_string("test", "Test field")
    assert result == "test"


@pytest.mark.utils_smoke
def test_validate_date():
    """Test that validate_date returns valid datetime object."""
    result = utils.validate_date("01-15-2025")
    expected = datetime(2025, 1, 15)
    assert result == expected


@pytest.mark.utils_smoke
def test_validate_grade():
    """Test that validate_grade returns valid grade."""
    result = utils.validate_grade(95.5)
    assert result == 95.5


@pytest.mark.utils_edge
def test_uuid_uniqueness():
    """Test that generate_uuid produces unique UUIDs."""
    uuids = set()
    n = 1000
    for _ in range(n):
        uuid_str = utils.generate_uuid()
        uuids.add(uuid_str)
    assert len(uuids) == n, "All UUIDs should be unique"


@pytest.mark.utils_edge
def test_validate_date_order_same_day():
    """Test that validate_date_order allows same day for start and end dates."""
    date1 = datetime(2026, 1, 18)
    date2 = datetime(2026, 1, 18)
    utils.validate_date_order(date1, date2)  # Should not raise


@pytest.mark.utils_edge
def test_validate_req_string_empty():
    """Test that validate_req_string raises error for empty string."""
    with pytest.raises(ValueError, match="must be non-empty"):
        utils.validate_req_string("", "Test field")


@pytest.mark.utils_edge
def test_validate_req_string_whitespace():
    """Test that validate_req_string raises error for whitespace-only string."""
    with pytest.raises(ValueError, match="must not only contain whitespace"):
        utils.validate_req_string("   ", "Test field")


@pytest.mark.utils_edge
def test_validate_date_invalid_format():
    """Test that validate_date raises error for invalid date format."""
    with pytest.raises(ValueError, match="Invalid date format"):
        utils.validate_date("2025-01-15")


@pytest.mark.utils_edge
def test_validate_date_invalid_date():
    """Test that validate_date raises error for invalid date."""
    with pytest.raises(ValueError, match="Invalid date format"):
        utils.validate_date("02-30-2025")


@pytest.mark.utils_edge
def test_validate_grade_negative():
    """Test that validate_grade raises error for negative grade."""
    with pytest.raises(ValueError, match="Grade must be between 0 and 150"):
        utils.validate_grade(-5.0)


@pytest.mark.utils_edge
def test_validate_grade_too_high():
    """Test that validate_grade raises error for grade above 150."""
    with pytest.raises(ValueError, match="Grade must be between 0 and 150"):
        utils.validate_grade(200.0)


@pytest.mark.utils_edge
def test_validate_grade_boundary_low():
    """Test that validate_grade accepts grade at lower boundary (0)."""
    result = utils.validate_grade(0.0)
    assert result == 0.0


@pytest.mark.utils_edge
def test_validate_grade_boundary_high():
    """Test that validate_grade accepts grade at upper boundary (150)."""
    result = utils.validate_grade(150.0)
    assert result == 150.0


@pytest.mark.utils_edge
def test_validate_grade_boundary_very_small():
    """Test that validate_grade accepts very small positive grade."""
    result = utils.validate_grade(0.01)
    assert math.isclose(result, 0.01, abs_tol=1e-9)


@pytest.mark.utils_edge
def test_validate_grade_float_precision():
    """Test that validate_grade handles float precision correctly."""
    result = utils.validate_grade(95.123456789)
    assert math.isclose(result, 95.123456789, abs_tol=1e-9)
