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
            KeyError: If the Course is not found.
        """
        title_lower = title.lower()
        term_id = self._title_to_id.get(title_lower)
        if term_id is not None:
            return term_id
        raise KeyError(f"Course with title '{title}' not found.")

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
        
    def edit_title(self, course_id: str, new_title: str) -> None:
        """Edit the title of a Course.
        
        Args:
            id: The ID of the Course to edit.
            new_title: The new title of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
            ValueError: If a Course with the same title already exists.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        old_title_lower = course.title.lower()
        
        if new_title.lower() in self._title_to_id:
            raise ValueError(f"Course with title {new_title} already exists.")

        course.title = new_title
        del self._title_to_id[old_title_lower]
        self._title_to_id[new_title.lower()] = course_id
        
    def edit_description(self, course_id: str, new_description: str) -> None:
        """Edit the description of a Course.
        
        Args:
            course_id: The ID of the Course to edit.
            new_description: The new description of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        course.description = new_description
        
    def edit_start_date(self, course_id: str, new_start_date: datetime) -> None:
        """Edit the start date of a Course.
        
        Args:
            course_id: The ID of the Course to edit.
            new_start_date: The new start date of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        course.start_date = new_start_date
        
    def edit_end_date(self, course_id: str, new_end_date: datetime) -> None:
        """Edit the end date of a Course.
        
        Args:
            course_id: The ID of the Course to edit.
            new_end_date: The new end date of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        course.end_date = new_end_date
        
    def edit_num_credits(self, course_id: str, new_num_credits: int) -> None:
        """Edit the number of credits of a Course.
        
        Args:
            course_id: The ID of the Course to edit.
            new_num_credits: The new number of credits of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        course.num_credits = new_num_credits
        
    def edit_active(self, course_id: str, new_active: bool) -> None:
        """Edit the active status of a Course.
        
        Args:
            course_id: The ID of the Course to edit.
            new_active: The new active status of the Course.
            
        Raises:
            KeyError: If a Course with the given ID is not found.
        """
        if course_id not in self._term._course_list:
            raise KeyError(f"Course with ID '{course_id}' not found.")
        course = self._term.find_course(course_id)
        course.active = new_active
        
    def remove_course(title: str) -> None:
        """Remove a Course by title.
        
        Args:
            title: The title of the Course to remove.
            
        Raises:
            KeyError: If a Course with the given title is not found.
        """
        if title not in self._title_to_id:
            raise KeyError(f"Course with title '{title}' not found.")
        course_id = self.get_course_id(title)
        
        if self._active_course is not None and self._active_course.id == course_id:
            self._active_course = None
            # self._assignment_controller = None
            
        self._term.remove_course(course_id)
        del self._title_to_id[title.lower()]
        self._course_order.remove(course_id)
        
    def find_course(self, title: str) -> Course:
        """Find a Course by title.
        
        Args:
            title: The title of the Course to find.
            
        Returns:
            Course: The Course with the given title.
        """
        course_id = self.get_course_id(title)
        if course_id not in 
        return self._term.find_course(course_id)
    
    def select_course(self, title: str) -> None:
        """Select a Course by title.
        
        Args:
            title: The title of the Course to select.
            
        Raises:
            KeyError: If the Course with the given ID is not found.
        """
        course_id = self.get_course_id(title)
        self._active_course = self._term.find_course(id)
        self._assignment_controller = AssignmentController(self._active_course)