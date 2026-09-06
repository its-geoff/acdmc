# Standard library imports
from __future__ import annotations

from datetime import datetime

from controllers.course_controller import CourseController

# Local imports
from models.term import Term


class TermController:
    """Controller for managing Term operations."""
    
    def __init__(self) -> None:
        """Initialize the TermController."""
        self.term_list: dict[str, Term] = {}
        self.title_to_id: dict[str, str] = {}
        self.term_order: list[str] = []
        self._active_term: Term | None = None
        self._course_controller: CourseController | None = None

    @property
    def course_controller(self) -> CourseController:
        """Get the course controller."""
        if self._course_controller is None:
            raise ValueError("No term selected.")
        return self._course_controller

    @property
    def active_term(self) -> Term:
        """Get the active term."""
        if self._active_term is None:
            raise ValueError("No term selected.")
        return self._active_term

    def get_term_id(self, title: str) -> str:
        """Get the ID of a term by its title.
        
        Args:
            title: The title of the term.
            
        Returns:
            The ID of the term.
        """
        title_lower = title.lower()
        for term_id, term_title in self.term_list.items():
            if term_title.lower() == title_lower:
                return term_id
        raise ValueError("Term not found.")

    def add_term(self, title: str, start_date: datetime, end_date: datetime, active: bool) -> None:
        """Add a term to the term list and verify term title uniqueness.

        Args:
            title: The title of the term being added.
            start_date: The start date of the term being addes.
            end_date: The end date of the term being added.
            active: Whether the term being added is active.
        """
        term = Term(title, start_date, end_date, active)
        if title.lower() in self.title_to_id:
            raise ValueError(f"Term with the title '{title}' already exists.")
        self.term_list[term.id] = term
        self.title_to_id[term.title.lower()] = term.id
        self.term_order.append(term.id)
        
    def edit_title(self, term_id: str, new_title: str) -> None:
        """Edit the title of a term.
        
        Args:
            term_id: The ID of the term to edit.
            new_title: The new title of the term.
        """
        if term_id not in self.term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        if new_title in self.title_to_id:
            raise ValueError(f"Term with the title '{new_title}' already exists.")
        self.term_list[term_id].title = new_title
        del self.title_to_id[self.term_list[term_id].title.lower()]
        self.title_to_id[new_title.lower()] = term_id

    def edit_start_date(self, term_id: str, new_start_date: datetime) -> None:
        """Edit the start date of a term.
        
        Args:
            term_id: The ID of the term to edit.
            new_start_date: The new start date of the term.
        """
        if term_id not in self.term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self.term_list[term_id].start_date = new_start_date

    def edit_end_date(self, term_id: str, new_end_date: datetime) -> None:
        """Edit the end date of a term.
        
        Args:
            term_id: The ID of the term to edit.
            new_end_date: The new end date of the term.
        """
        if term_id not in self.term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self.term_list[term_id].end_date = new_end_date

    def edit_active(self, term_id: str, active: bool) -> None:
        """Edit the active status of a term.
        
        Args:
            term_id: The ID of the term to edit.
            active: The new active status of the term.
        """
        if term_id not in self.term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self.term_list[term_id].active = active

    def remove_term(self, title: str) -> None:
        """Remove a term from the term list.

        Args:
            title: The title of the term to remove.
        """
        term_id = self.get_term_id(title)

        if term_id not in self.term_list:
            raise ValueError(f"Term with title '{title}' not found.")

        if (self._active_term is not None and self._active_term.id == term_id):
            self._active_term = None
            self._course_controller = None
        
        del self.term_list[term_id]
        del self.title_to_id[title.lower()]
        self.term_order.remove(term_id)

    def find_term(self, title: str) -> Term:
        """Find a term by title.
        
        Args:
            title: The title of the term to find.
            
        Returns:
            The term with the given title.
        """
        id = self.get_term_id(title)
        return self.term_list[id]

    def select_term(self, title: str) -> None:
        """Select a term by title.
        
        Args:
            title: The title of the term to select.
        """
        try:
            term = self.find_term(title)
            self._active_term = term
            self._course_controller = CourseController(self._active_term)
        except ValueError as e:
            raise ValueError(f"Term with title '{title}' not found.") from e