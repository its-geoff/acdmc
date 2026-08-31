# Standard library imports
import datetime
import sys
import uuid

# Local imports
from assignment import Assignment


def generate_uuid() -> str:
    """Generates a unique ID across all objects and classes.
    
    Returns:
        str: A UUID v4 string.
    """
    return str(uuid.uuid4())


def validate_req_string(str: str, label: str) -> str | None:
    """Checks if a required string is valid. A string is considered valid if it is
    not empty and not entirely whitespace. Returns the validated string.

    Args:
        str: The string to validate.
        label: The label of the string.

    Returns:
        str: The valid string.

    Raises:
        ValueError: If the string is empty or is only whitespace.
    """
    if not str or str.isspace():
        raise ValueError(f"{label} must be non-empty and must not only contain whitespace.")

    return str


def validate_date(date: datetime.datetime) -> datetime.datetime | None:
    """Checks if a date is valid. A date is valid if it can be parsed from a string to a
    datetime object. Returns the validated date.

    Args:
        date: The date to validate.

    Returns:
        date: The validated date.

    Raises:
        ValueError: If the date is not a valid date.
    """
    try:
        format = "%m-%d-%Y"
        return datetime.strptime(date, format)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date}. Use MM-DD-YYYY format.") from e


def validate_date_order(start_date: datetime.datetime, end_date: datetime.datetime) -> None:
    """Checks if the start date is before the end date. Throws an error if the date order 
    is invalid.

    Args:
        start_date: The start date of an object.
        end_date: The end date of an object.
    
    Raises:
        ValueError: If the end date is before the start date.
    """
    dates = [start_date, end_date]

    if dates != sorted(dates):
        raise ValueError("End date cannot be before start date.")