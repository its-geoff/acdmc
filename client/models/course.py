# Standard library imports
import math
from datetime import date
from typing import Self

# Local imports
import utils
from assignment import Assignment


class Course:
    """Client-side Course model."""

    # Class constants
    GRADE_WEIGHTS_DEFAULT: dict[str, float] = {
        "Homework": 0.25,
        "Midterm": 0.35,
        "Final Exam": 0.4
    }
    """Default grade weights if unset; must add up to 1.0."""

    GRADE_SCALE_DEFAULT: dict[float, str] = {
        97.0: "A+",
        93.0: "A",
        90.0: "A-",
        87.0: "B+",
        83.0: "B",
        80.0: "B-",
        77.0: "C+",
        73.0: "C",
        70.0: "C-",
        67.0: "D+",
        63.0: "D",
        60.0: "D-",
        0.0: "F"
    }
    """Associates each percentage range to a letter grade."""

    GPA_SCALE: dict[str, float] = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "D-": 0.7,
        "F": 0.0,
        "N/A": 0.0
    }
    """Associates each letter grade to a GPA value."""

    def __init__(
            self,
            title: str,
            description: str,
            start_date: date,
            end_date: date,
            num_credits: int,
            active: bool = True):
        # UUID v4 generated during creation
        self._id: str = utils.generate_uuid()
        self._title: str = utils.validate_req_string(title, "Title")
        # Only set description if it's not empty or whitespace
        self.description: str = description if description and not description.isspace() else ""
        self._start_date: date = utils.validate_date(start_date)
        self._end_date: date = utils.validate_date(end_date)
        utils.validate_date_order(start_date, end_date)

        # Maps id -> Assignment
        self._assignment_list: dict[str, Assignment] = {}
        self.num_credits: int = 3
        self.grade_percentage: float = 0.0
        self._letter_grade: str = "N/A"
        self._gpa_val: float = 0.0
        self.active: bool = active

        self._grade_weights: dict[str, float] = Course.GRADE_WEIGHTS_DEFAULT.copy()
        self._grades_by_category: dict[str, float]
        self._grade_scale: dict[float, str] = Course.GRADE_SCALE_DEFAULT.copy()
        self._gpa_scale: dict[str, float] = Course.GPA_SCALE.copy()

    def __eq__(self, other: Self) -> bool:
        return self._id == other._id

    @property
    def title(self) -> str:
        """Get the title of a term."""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = utils.validate_req_string(value, "Title")
    
    @property
    def start_date(self) -> date:
        """Get the start date of a term."""
        return self._start_date
    
    @start_date.setter
    def start_date(self, value: date) -> None:
        self._start_date = utils.validate_date(value)
    
    @property
    def end_date(self) -> date:
        """Get the end date of a term."""
        return self._end_date
    
    @end_date.setter
    def end_date(self, value: date) -> None:
        self._end_date = utils.validate_date(value)

    def validate_grade_weights(self, grade_weights: dict[str, float]):
        """Checks that the new list of grade weights is valid.
        
        Args:
            grade_weights: The new grade weights.
        
        Raises:
            ValueError: If the grade weights do not add up to 1.0.
        """
        total = 0.0

        for _, weight in grade_weights:
            total += weight

        if math.isclose(total, 1.0):
            raise ValueError("Grade weights must equal 100%.\n"
                "Current total: " + str(total * 100) + "%")

    def validate_num_credits(self, num_credits: int):
        """Checks that the new number of credits is valid.

        Args:
            num_credits: The new number of credits.

        Raises:
            ValueError: If the number of credits is less than 0.
        """
        if (num_credits < 0):
            raise ValueError("Number of credits must be greater than or equal to 0.")
        
    def validate_grade_percentage(self, grade_percentage: float):
        """Checks that the new grade percentage is valid.

        Args:
            grade_percentage: The new grade percentage.

        Raises:
            ValueError: If the grade percentage is less than 0 or greater than 150.
        """
        if (grade_percentage < 0.0 or grade_percentage > 150.0):
            raise ValueError("Grade percentage must be between 0 and 150.")
        
    def validate_grade_scale(self, grade_scale: dict[float, str]):
        """Checks that the new grade scale is valid.

        Args:
            grade_scale: The new grade scale.
        
        Raises:
            ValueError: If the grade scale is empty or does not provide grades for the range 0-100.
        """
        if not grade_scale:
            raise ValueError("Grade scale must not be empty.")

        if 0.0 not in grade_scale:
            raise ValueError("Grade scale must include 0.")

        if any(k >= 100.0 for k in grade_scale.keys()):
            raise ValueError("Grade scale must not include values greater than 100.")

    def calculate_grades_by_category(self):
        """Calculates grades for each category.
        
        Iterates over all assignments in the Course, groups completed assignments by category,
        and computes raw percentage grade for each category. The per-category averages will be
        weighted for the total grade calculation.
        """
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}

        # Add values from assignment list to totals and counts
        for _, assignment in self._assignment_list.items():
            if not assignment.completed:
                continue

            category = assignment.get_category()
            totals[category] += assignment.get_grade()
            counts[category] += 1

        self._grades_by_category.clear()

        # calculate category grades and store in dictionary
        for category_name in self._grade_weights:
            if category_name not in counts or counts[category_name] == 0:
                continue
            
            category_grade = totals[category_name] / counts[category_name]
            self._grades_by_category[category_name] = utils.float_round(category_grade, 2)
