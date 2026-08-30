# Standard library imports
import sys
from datetime import date
from typing import Self, TextIO

# Local imports
import utils
from course import Course


class Term:
    """Client-side Term model."""

    def __init__(
            self,
            title: str,
            start_date: date,
            end_date: date,
            active: bool = True):
        # UUID v4 generated during creation
        self.id: str = utils.generate_uuid()
        self._title: str = utils.validate_req_string(title, "Title")
        self._start_date: date = utils.validate_date(start_date)
        self._end_date: date = utils.validate_date(end_date)
        utils.validate_date_order(start_date, end_date)

        # Maps id -> Course
        self._course_list: dict[str, Course] = {}
        self.active: bool = active

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id

    @property
    def title(self) -> str:
        """Get the title of a Term."""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = utils.validate_req_string(value, "Title")
    
    @property
    def start_date(self) -> date:
        """Get the start date of a Term."""
        return self._start_date
    
    @start_date.setter
    def start_date(self, value: date) -> None:
        self._start_date = utils.validate_date(value)
    
    @property
    def end_date(self) -> date:
        """Get the end date of a Term."""
        return self._end_date
    
    @end_date.setter
    def end_date(self, value: date) -> None:
        self._end_date = utils.validate_date(value)

    @property
    def total_credits(self) -> int:
        """Recalculate and return the total number of credits taken in a Term."""
        return self._calculate_total_credits()

    @property
    def ovr_gpa(self) -> float:
        """Recalculate and return the overall GPA for a Term."""
        return self._calculate_ovr_gpa() 

    def _calculate_total_credits(self) -> int:
        """Calculate the total number of credits for all Courses in the Term.
        
        Returns:
            int: The total number of credits.
        """
        result = 0

        for _, course in self.course_list.items():
            result += course.num_credits

        return result

    def _calculate_ovr_gpa(self) -> float:
        """Calculate the overall GPA for all Courses in the Term.
        
        Returns:
            float: The overall GPA.
        """
        total_gpa = 0.0
        credits = self.total_credits

        # Default case to avoid division by zero
        if credits == 0:
            return 0.0

        for _, course in self._course_list.items():
            total_gpa += course.gpa_value * course.num_credits

        return utils.float_round(total_gpa / float(credits), 2)

    def print_term_info(self, output_stream: TextIO = sys.stdout) -> None:
        """Print the Term information to the specified output stream.
        
        Args:
            output_stream: The output stream to write to.
        """
        print(f"ID: {self.id}", file=output_stream)
        print(f"Term: {self.title}", file=output_stream)
        print(f"Duration: {self.start_date} - {self.end_date}", file=output_stream)
        print(f"Total Credits: {self.total_credits}", file=output_stream)
        print(f"Overall GPA: {self.ovr_gpa}", file=output_stream)
        print(f"Current? {utils.bool_to_string(self.active)}", file=output_stream)

    def add_course(self, course: Course) -> None:
        """Adds a Course to course_list using the given input.

        Args:
            course: The Course that will be added to course_list.
        """
        key = course.id
        insert = key not in self._course_list

        # Throw error if course is already in the Term
        if not insert:
            raise ValueError(f"Course with ID {key} already exists in Term {self.title}.")

        self._course_list[key] = course

    def remove_course(self, id: str) -> None:
        """Removes a Course with the specified UUID.

        Args:
            id: The UUID of the Course to remove.
        """
        try:
            del self._course_list[id]
        except KeyError as e:
            raise KeyError("Course not found.") from e

    def find_course(self, id: str) -> Course:
        """Finds a Course in course_list based on ID.

        Args:
            id: The UUID of the Course to find.

        Returns:
            Course: The Course object matching the given UUID. Throws error if not found.
        """
        if id in self._course_list:
            return self._course_list[id]
        else:
            raise KeyError("Course not found.")

    def from_row(
            self,
            id: str,
            title: str,
            start_date: date,
            end_date: date,
            active: bool) -> Self:
        """Constructs a Term from a persisted record, using the existing ID instead
        of generating a new one.

        Args:
            id: The ID of the Term to construct.
            start_date: The start date of the Term.
            end_date: The end date of the Term.
            active: Whether the Term is currently active.
        
        Returns:
            Term object with the specified attributes and copied ID.
        """
        t = Term(title, start_date, end_date, active)
        t.id = id
        return t