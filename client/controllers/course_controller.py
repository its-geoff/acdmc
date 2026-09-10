# Standard library imports
from __future__ import annotations

from datetime import datetime

# Local imports
from controllers.assignment_controller import AssignmentController
from models.course import Course
from models.term import Term


class CourseController:
    """Controller for managing Course operations."""

    def __init__(self, term: Term) -> None:
        """Initialize the CourseController."""
        self._term = term
        # Maps title (lowercase) -> id; only used internally
        self._title_to_id: dict[str, str] = {}
        # Order of Courses by ID
        self._course_order: list[str] = []
        self._active_course: Course | None = None
        self._assignment_controller: AssignmentController | None = None

    @property
    def course_order(self) -> tuple[str]:
        """Get a read-only view of the Course order."""
        return tuple(self._course_order)

    @property
    def active_course(self) -> Course:
        """Get the active Course.
        
        Raises:
            ValueError: If no Course is selected.
        """
        if self._active_course is None:
            raise ValueError("No Course selected.")
        return self._active_course


    @property
    def assignment_controller(self) -> AssignmentController:
        """Get the Assignment controller.
        
        Raises:
            ValueError: If no Course is selected.
        """
        if self._assignment_controller is None:
            raise ValueError("No Course selected.")
        return self._assignment_controller

    def get_course_id(self, title: str) -> str:
        """Get the ID of a Course by its title.
        
        Args:
            title: The title of the Course.
            
        Returns:
            The ID of the Course.

        Raises:
            ValueError: If the Course is not found.
        """
        title_lower = title.lower()
        term_id = self._title_to_id.get(title_lower)
        if term_id is not None:
            return term_id
        raise ValueError("Course not found.")

    def add_course(
            self,
            title: str,
            description: str,
            start_date: datetime,
            end_date: datetime,
            num_credits: int,
            active: bool) -> None:
        """Add a Course to the Course list.

        Args:
            title: The title of the Course being added.
            description: The description of the Course being added.
            start_date: The start date of the Course being added.
            end_date: The end date of the Course being added.
            num_credits: The number of credits of the Course being added.
            active: Whether the Course being added is active.

        Raises:
            RuntimeError: If there is an unexpected error when trying to add the Course.
        """
        course = Course(title, description, start_date, end_date, num_credits, active)
        if title.lower() in self._title_to_id:
            raise ValueError(f"Course with the title '{title}' already exists.")

        try:
            self._term.add_course(course)
        except RuntimeError as e:
            raise RuntimeError("An unexpected error occurred when adding the course.") from e

        self._title_to_id[course.title.lower()] = course.id
        self._course_order.append(course.id)
