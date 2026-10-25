# Standard library imports
import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta

default_start_date = datetime.now().date()
default_end_date = datetime.now() + relativedelta(months=4)

def generate_uuid() -> str:
    """Generates a unique ID across all objects and classes.
    
    Returns:
        str: A UUID v4 string.
    """
    return str(uuid.uuid4())


def validate_req_string(value: str, label: str) -> str:
    """Checks if a required string is valid. A string is considered valid if it is
    not empty and not entirely whitespace. Returns the validated string.

    Args:
        value: The string to validate.
        label: The label of the string.

    Returns:
        str: The valid string.

    Raises:
        ValueError: If the string is empty or is only whitespace.
    """
    if not value or value.isspace():
        raise ValueError(f"{label} must be non-empty and must not only contain whitespace.")

    return value


def validate_grade(grade: float) -> float:
    """Checks if a grade is valid. A grade is valid if it is between 0 and 150. Returns the 
    validated grade.
    
    Args:
        grade: The grade to validate.
        
    Returns:
        float: The validated grade.
        
    Raises:
        ValueError: If the grade is not between 0 and 150.
    """
    if grade < 0.0 or grade > 150.0:
        raise ValueError("Grade must be between 0 and 150.")
    return grade


def validate_date_order(start_date: datetime, end_date: datetime) -> None:
    """Checks if the start date is before the end date. Raises an error if the date order 
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


def bool_to_string(value: bool) -> str:
    """Converts bool value into a string for output.

    Args:
        value: The boolean to convert.

    Returns:
        str: The converted form of the boolean.
    """
    if value:
        return "Yes"
    else:
        return "No"
