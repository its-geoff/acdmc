# Standard library imports
import sys
from datetime import date
from typing import Self, TextIO

# Local imports
import utils


class Assignment:
    """Client-side Assignment model."""

    def __init__(
            self,
            title: str,
            description: str,
            category: str,
            due_date: date,
            completed: bool,
            grade: float):
        self.id: str = utils.generate_uuid()
        self._title: str = utils.validate_req_string(title, "Title")
        # Only set description if it's not empty or whitespace
        self._description: str = description if description and not description.isspace() else ""
        self._category: str = utils.validate_req_string(category, "Category")
        self._due_date: date = utils.validate_date(due_date)
        self.completed: bool = completed
        # Grade is only set for completed Assignments
        if completed:
            self._grade: float = utils.float_round(utils.validate_grade(grade), 2)
        else:
            self._grade: float = 0.0

    def __eq__(self, other: object) -> bool:
        """Checks equality of this object with another Assignment.
        
        Args:
            other: The object to compare with. Intended to be an Assignment.

        Returns:
            bool: True if the objects are the same, False otherwise.
        """
        if not isinstance(other, Assignment):
            return False
        return self.id == other.id

    @property
    def title(self) -> str:
        """Get the title of an Assignment."""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = utils.validate_req_string(value, "Title")

    @property
    def description(self) -> str:
        """Get the description of an Assignment."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value if value and not value.isspace() else ""

    @property
    def category(self) -> str:
        """Get the category of an Assignment."""
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        self._category = utils.validate_req_string(value, "Category")

    @property
    def due_date(self) -> date:
        """Get the start date of an Assignment."""
        return self._start_date
    
    @due_date.setter
    def due_date(self, value: date) -> None:
        self._due_date = utils.validate_date(value)

    @property
    def grade(self) -> float:
        """Get the grade of an Assignment."""
        return self._grade

    @grade.setter
    def grade(self, value: float, total_points: float | None = None) -> None:
        """Set the grade of an Assignment.
        
        This setter works for both percentage-based and point-based grading. If only a
        value is entered, percentage-based grading is used and the percentage will be
        added as the grade. If both a value and total points are added, point-based grading
        is used and the percentage will be calculated before adding the grade.

        Args:
            value: The grade to be added or the number of points earned.
            total_points: The total points of the assignment.

        Raises:
            ValueError: If total points are less than or equal to 0.
        """
        if total_points:
            if total_points <= 0.0:
                raise ValueError("Total points must be greater than 0.")

            calculated_grade = (value / total_points) * 100.0
            self._grade = utils.float_round(calculated_grade, 2)
        else:
            self._grade = utils.float_round(utils.validate_grade(value), 2)

    def print_assignment_info(self, output_stream: TextIO = sys.stdout) -> None:
        """Print the Assignment information to the specified output stream.
        
        Args:
            output_stream: The output stream to write to.
        """
        print(f"ID: {self.id}", file=output_stream)
        print(f"Assignment: {self.title}", file=output_stream)
        if self._description:
            print(f"Description: {self.description}", file=output_stream)
        print(f"Category: {self.category}", file=output_stream)
        print(f"Due Date: {self.due_date}", file=output_stream)
        print(f"Completed? {utils.bool_to_string(self.active)}", file=output_stream)
        print(f"Grade: {self.grade:.2f}%", file=output_stream)

    @classmethod
    def from_row(
        cls,
        assignment_id: str,
        title: str,
        description: str,
        category: str,
        due_date: date,
        completed: bool,
        grade: float) -> Self:
        """Constructs a Assignment from a persisted record, using the existing ID instead
        of generating a new one.

        Args:
            assignment_id: The ID of the Assignment to construct.
            title: The title of the Assignment.
            description: A description of the Assignment.
            category: The category of the Assignment.
            due_date: The start date of the Assignment.
            completed: Whether the Course is completed.
            grade: The grade of the Assignment.
        
        Returns:
            Assignment object with the specified attributes and copied ID.
        """
        a = Assignment(title, description, category, due_date, completed, grade)
        a.id = assignment_id
        return a