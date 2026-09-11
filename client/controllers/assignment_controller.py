# Standard library imports
from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import Mapping

# Local imports
from models.course import Course
from models.assignment import Assignment


class AssignmentController:
    """Controller for managing Assignment operations."""
    
    def __init__(self, course: Course) -> None:
        self._course: Course = course
        # Maps title (lowercase) -> id; only used internally
        self._title_to_id: dict[str, str] = {}
        
    def get_assignment_list(self) -> dict[str, Assignment]:
        """Get the Assignment list of the current Course.
        
        Returns:
            dict[str, Assignment]: A dictionary mapping Assignment IDs to 
                Assignment objects.
        """
        return self._course.assignment_list()
    
    def get_assignment_id(self, title: str) -> str:
        """Get the ID of an Assignment by its title.
        
        Args:
            title: The title of the Assignment.
            
        Returns:
            str: The ID of the Assignment.
        
        Raises:
            KeyError: If the Assignment is not found.
        """
        title_lower = title.lower()
        assignment_id = self._title_to_id.get(title_lower)
        if assignment_id is not None:
            return assignment_id
        raise KeyError(f"Assignment with title '{title}' not found.")
    
    def add_assignment(
            self,
            title: str,
            description: str,
            category: str,
            due_date: datetime,
            completed: bool,
            grade: float) -> None:
        """Add an Assignment to the Assignment list.
        
        Args:
            title: The title of the Assignment being added.
            description: The description of the Assignment being added.
            category: The category of the Assignment being added.
            due_date: The due date of the Assignment being added.
            completed: The completion status of the Assignment being added.
            grade: The grade of the Assignment being added. If completed is False, this
                will default to 0.
                
        Raises:
            KeyError: If category is not in grade weights list.
            ValueError: If an Assignment with the same title already exists.
            RuntimeError: If there is an unexpected error when trying to add the Assignment.
        """
        if category not in self._course.grade_weights:
            raise KeyError("Invalid category. Category must be in grade weights.")
        if title.lower() in self._title_to_id:
            raise ValueError(f"Assignment with title '{title}' already exists.")
        
        assignment = Assignment(title, description, category, due_date, completed, grade)
        try:
            self._course.add_assignment(assignment)
        except RuntimeError as e:
            raise RuntimeError("An unexpected error occurred when adding the course.") from e
        
        self._title_to_id[assignment.title.lower()] = assignment.id
        
    def edit_title(self, assignment_id: str, new_title: str) -> None:
        """Edit the title of an Assignment.
        
        Args:
            assignment_id: The ID of the Assignment to edit.
            new_title: The new title of the Assignment.
            
        Raises:
            KeyError: If an Assignment with the given ID is not found.
            ValueError: If an Assignment with the same title already exists.
        """
        if assignment_id not in self._course._assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        course = self._course.find_assignment(assignment_id)
        old_title_lower = assignment.title.lower()
        
        if new_title.lower() in self._title_to_id:
            raise ValueError(f"Assignment with title {new_title} already exists.")

        assignment.title = new_title
        del self._title_to_id[old_title_lower]
        self._title_to_id[new_title.lower()] = assignment_id