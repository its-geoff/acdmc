# Standard library imports
from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import Mapping

# from controllers.course_controller import CourseController

# Local imports
from models.term import Term


class TermController:
    """Controller for managing Term operations."""
    
    def __init__(self) -> None:
        """Initialize the TermController."""
        # Maps id -> Term
        self._term_list: dict[str, Term] = {}
        # Maps title (lowercase) -> id; only used internally
        self._title_to_id: dict[str, str] = {}
        # Order of terms by ID
        self._term_order: list[str] = []
        self._active_term: Term | None = None
        # self._course_controller: CourseController | None = None

    @property
    def term_list(self) -> Mapping[str, Term]:
        """Get a read-only view of the Term list."""
        return MappingProxyType(self._term_list)

    @property
    def term_order(self) -> tuple[str]:
        """Get a read-only view of the term order."""
        return tuple(self._term_order)

    # @property
    # def course_controller(self) -> CourseController:
    #     """Get the Course controller.
        
    #     Raises:
    #         ValueError: If no Term is selected.
    #     """
    #     if self._course_controller is None:
    #         raise ValueError("No Term selected.")
    #     return self._course_controller

    @property
    def active_term(self) -> Term:
        """Get the active Term.
        
        Raises:
            ValueError: If no Term is selected.
        """
        if self._active_term is None:
            raise ValueError("No Term selected.")
        return self._active_term

    def get_term_id(self, title: str) -> str:
        """Get the ID of a Term by its title.
        
        Args:
            title: The title of the Term.
            
        Returns:
            The ID of the Term.

        Raises:
            ValueError: If the Term is not found.
        """
        title_lower = title.lower()
        term_id = self._title_to_id.get(title_lower)
        if term_id is not None:
            return term_id
        raise ValueError("Term not found.")

    def add_term(self, title: str, start_date: datetime, end_date: datetime, active: bool) -> None:
        """Add a Term to the Term list and verify Term title uniqueness.

        Args:
            title: The title of the Term being added.
            start_date: The start date of the Term being addes.
            end_date: The end date of the Term being added.
            active: Whether the Term being added is active.

        Raises:
            ValueError: If a Term with the same title already exists.
        """
        term = Term(title, start_date, end_date, active)
        if title.lower() in self._title_to_id:
            raise ValueError(f"Term with the title '{title}' already exists.")
        self._term_list[term.id] = term
        self._title_to_id[term.title.lower()] = term.id
        self._term_order.append(term.id)
        
    def edit_title(self, term_id: str, new_title: str) -> None:
        """Edit the title of a Term.
        
        Args:
            term_id: The ID of the Term to edit.
            new_title: The new title of the Term.

        Raises:
            ValueError: If a Term with the given ID is not found or if a Term with the same
                title already exists.
        """
        if term_id not in self._term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        term = self._term_list.get(term_id)
        old_title_lower = term.title.lower()
        existing_term_id = self._title_to_id.get(new_title.lower())
        if existing_term_id is not None and existing_term_id != term_id:
            raise ValueError(f"Term with the title '{new_title}' already exists.")
        term.title = new_title
        del self._title_to_id[old_title_lower]
        self._title_to_id[term.title.lower()] = term_id

    def edit_start_date(self, term_id: str, new_start_date: datetime) -> None:
        """Edit the start date of a Term.
        
        Args:
            term_id: The ID of the Term to edit.
            new_start_date: The new start date of the Term.

        Raises:
            ValueError: If a Term with the given ID is not found.
        """
        if term_id not in self._term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self._term_list[term_id].start_date = new_start_date

    def edit_end_date(self, term_id: str, new_end_date: datetime) -> None:
        """Edit the end date of a Term.
        
        Args:
            term_id: The ID of the Term to edit.
            new_end_date: The new end date of the Term.

        Raises:
            ValueError: If a Term with the given ID is not found.
        """
        if term_id not in self._term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self._term_list[term_id].end_date = new_end_date

    def edit_active(self, term_id: str, active: bool) -> None:
        """Edit the active status of a Term.
        
        Args:
            term_id: The ID of the Term to edit.
            active: The new active status of the Term.

        Raises:
            ValueError: If a Term with the given ID is not found.
        """
        if term_id not in self._term_list:
            raise ValueError(f"Term with ID '{term_id}' not found.")
        self._term_list[term_id].active = active

    def remove_term(self, title: str) -> None:
        """Remove a term from the Term list.

        Args:
            title: The title of the Term to remove.

        Raises:
            ValueError: If a Term with the given title is not found.
        """
        term_id = self.get_term_id(title)

        if term_id not in self._term_list:
            raise ValueError(f"Term with title '{title}' not found.")

        if (self._active_term is not None and self._active_term.id == term_id):
            self._active_term = None
            # self._course_controller = None

        del self._term_list[term_id]
        del self._title_to_id[title.lower()]
        self._term_order.remove(term_id)

    def find_term(self, title: str) -> Term:
        """Find a Term by title.
        
        Args:
            title: The title of the Term to find.
            
        Returns:
            The Term with the given title.
        """
        id = self.get_term_id(title)
        return self._term_list[id]

    # def select_term(self, title: str) -> None:
    #     """Select a Term by title.
        
    #     Args:
    #         title: The title of the Term to select.

    #     Raises:
    #         ValueError: If a Term with the given ID is not found.
    #     """
    #     try:
    #         term = self.find_term(title)
    #         self._active_term = term
    #         self._course_controller = CourseController(self._active_term)
    #     except ValueError as e:
    #         raise ValueError(f"Term with title '{title}' not found.") from e