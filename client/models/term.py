# Standard library imports
import sys
from datetime import date
from typing import Dict, Self, TextIO


# Local imports
from course import Course
import utils


class Term:
    """Client-side Term model."""

    def __init__(
            self,
            title: str,
            start_date: date,
            end_date: date):
        # UUID v4 generated during creation
        self._id = utils.generate_uuid()
        self._title = utils.validate_req_string(title, "Title")
        self._start_date = utils.validate_date(start_date)
        self._end_date = utils.validate_date(end_date)

        # Maps id -> Course
        self._course_list: Dict[str, Course] = {}
        self.total_credits: int = 0
        self.ovr_gpa: float = 0.0
        self.active: bool = True

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

    def calculate_total_credits(self) -> int:
        """Calculate the total number of credits for all courses in the term.
        
        Returns:
            int: The total number of credits.
        """
        result = 0

        for _, course in self.course_list.items():
            result += course.get_num_credits()

        return result

    def calculate_ovr_gpa(self) -> float:
        """Calculate the overall GPA for all courses in the term.
        
        Returns:
            float: The overall GPA.
        """
        total_gpa = 0.0
        credits = self.calculate_total_credits()

        # Default case to avoid division by zero
        if credits == 0:
            return 0.0

        for _, course in self.course_list.items():
            total_gpa += course.get_gpa_val() * course.get_num_credits()

        return utils.float_round(total_gpa / float(credits), 2)

    def print_term_info(self, output_stream: TextIO = sys.stdout) -> None:
        """Print the term information to the specified output stream.
        
        Args:
            output_stream: The output stream to write to.
        """
        print(f"ID: {self._id}", file=output_stream)
        print(f"Term: {self._title}", file=output_stream)
        print(f"Duration: {self._start_date} - {self._end_date}", file=output_stream)
        print(f"Total Credits: {self.total_credits}", file=output_stream)
        print(f"Overall GPA: {self.ovr_gpa}", file=output_stream)
        print(f"Current? {utils.bool_to_string(self.active)}", file=output_stream)

    def add_course(self, course: Course) -> None:
        """Adds a Course to course_list using the given input.

        Args:
            course: The Course that will be added to course_list.
        """
        key = course.get_id()
        insert = key not in self._course_list

        # Throw error if course is already in the term
        if not insert:
            raise ValueError(f"Course with ID {key} already exists in term {self._title}.")

        self._course_list[key] = course
        self.total_credits = self.calculate_total_credits()
        self.ovr_gpa = self.calculate_ovr_gpa()

    def remove_course(self, id: str) -> None:
        """Removes a Course with the specified UUID.

        Args:
            id: The UUID of the Course to remove.
        """
        try:
            del self._course_list[id]
        except KeyError as e:
            raise KeyError("Course not found.") from e

        self.total_credits = self.calculate_total_credits()
        self.ovr_gpa = self.calculate_ovr_gpa()

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
        if not start_date:
            raise ValueError("Start date must not be empty.")
        if not end_date:
            raise ValueError("End date must not be empty.")
        
        t = Term(title, start_date, end_date, active)
        t._id = self._id
        return t