# Standard library imports
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import sys
import TextIO

# Local imports
from controllers.term_controller import TermController
from models.assignment import Assignment
from models.course import Course
from models.term import Term
import utils


@dataclass
class EditTermResult:
    """A class that shows the state of Term field updates for edit_term."""
    title_requested: bool = False
    title_updated: bool = False

    start_date_requested: bool = False
    start_date_updated: bool = False

    end_date_requested: bool = False
    end_date_updated: bool = False
    
    active_requested: bool = False
    active_updated: bool = False

    def any_requested(self) -> bool:
        """Return whether any Term field was requested for edit.
        
        Returns:
            True if any of the four fields is requested for edit, False otherwise.
        """
        return self.title_requested or self.start_date_requested or self.end_date_requested \
            or self.active_requested

    def dates_requested(self) -> bool:
        """Return whether any date field was requested for edit.

        Returns:
            True if start date or end date is requested for edit, False otherwise.
        """
        return self.start_date_requested or self.end_date_requested

    def dates_updated(self) -> bool:
        """Return whether any date field was successfully updated.
        
        Returns:
            True if start date or end date was successfully updated, False otherwise.
        """
        return self.start_date_updated or self.end_date_updated


@dataclass
class EditCourseResult:
    """A class that shows the state of Course field updates for edit_course."""
    title_requested: bool = False
    title_updated: bool = False

    description_requested: bool = False
    description_updated: bool = False

    start_date_requested: bool = False
    start_date_updated: bool = False

    end_date_requested: bool = False
    end_date_updated: bool = False

    active_requested: bool = False
    active_updated: bool = False

    def any_requested(self) -> bool:
        """Return whether any Course field was requested for edit.
        
        Returns:
            True if any of the five fields is requested for edit, False otherwise.
        """
        return self.title_requested or self.description_requested or self.start_date_requested \
            or self.end_date_requested or self.active_requested

    def dates_requested(self) -> bool:
        """Return whether any date field was requested for edit.

        Returns:
            True if start date or end date is requested for edit, False otherwise.
        """
        return self.start_date_requested or self.end_date_requested

    def dates_updated(self) -> bool:
        """Return whether any date field was successfully updated.
        
        Returns:
            True if start date or end date was successfully updated, False otherwise.
        """
        return self.start_date_updated or self.end_date_updated


@dataclass
class EditAssignmentResult:
    title_requested: bool = False
    title_updated: bool = False

    description_requested: bool = False
    description_updated: bool = False

    category_requested: bool = False
    category_updated: bool = False

    due_date_requested: bool = False
    due_date_updated: bool = False

    def any_requested(self) -> bool:
        """Return whether any Assignment field was requested for edit.
        
        Returns:
            True if any of the four fields is requested for edit, False otherwise.
        """
        return self.title_requested or self.description_requested or self.category_requested \
            or self.due_date_requested


class CliView:
    """Class that handles I/O and user interaction for the command line interface."""

    def __init__(
            self,
            controller: TermController,
            in_stream: TextIO = sys.stdin,
            out_stream: TextIO = sys.stdout) -> None:
        self._controller: TermController = controller
        self._selected_term: Term | None
        self._selected_course: Course | None
        self._selected_assignment: Assignment | None
        # Defines input stream
        self._in_stream: TextIO = in_stream
        # Defines output stream
        self._out_stream: TextIO = out_stream

        class MenuState(Enum):
            TERM = 0
            COURSE = 1
            ASSIGNMENT = 2
            EXIT = 3

    def _print(self, *args, **kwargs) -> None:
        """Prints to the output stream.
        
        Args:
            *args: Positional arguments to print.
            **kwargs: Keyword arguments to print.
        """
        print(*args, file=self._out_stream, **kwargs)

    def _print_centered(self, text: str) -> None:
        """Prints text centered in a 99-character wide field.
        
        Args:
            text: The text to center.
        """
        self._print(text.center(99))
    
    def display_delim(self) -> None:
        """Prints a delimiter line to separate different sections of information."""
        self._print("=" * 99)

    def display_secondary_delim(self) -> None:
        """Prints a delimiter line visually different from the first to separate subsections
        of information."""
        self._print("-" * 99)

    def display_intro(self) -> None:
        """Prints an introduction to the application."""
        self.display_delim()
        self._print_centered("Welcome to ACDMC!")
        self._print_centered("It's your personal academic sidekick.")

    def display_term_menu(self) -> None:
        """Prints a menu of choices for the user to select a Term."""
        self.display_delim()
        self._print_centered("Term Menu")
        self._print_centered("What would you like to do today?")

        # Check if there are terms in the list
        if (self._controller._term_list):
            self._print("[A] Add term")
            self._print("[E] Edit term")
            self._print("[S] Select term")
            self._print("[R] Remove term")
            self._print("[X] Exit program")
        else:
            self._print("[A] Add term")
            self._print("[X] Exit program")

    def display_course_menu(self) -> None:
        """Prints a menu of choices for the user to select a Course."""
        self.display_delim()
        self._print("Term: " + self._selected_term.title)
        self._print_centered("Course Menu")
        self._print_centered("What would you like to do today?")

        # Check if there are courses in the list
        if (self._selected_term._course_list):
            self._print("[A] Add course")
            self._print("[E] Edit course")
            self._print("[S] Select course")
            self._print("[R] Remove course")
            self._print("[X] Exit to term menu")
        else:
            self._print("[A] Add course")
            self._print("[X] Exit to term menu")

    def display_assignment_menu(self) -> None:
        """Prints a menu of choices for the user to select an Assignment."""
        self.display_delim()
        self._print("Term: " + self._selected_term.title)
        self._print("Course: " + self._selected_course.title)
        self._print_centered("Assignment Menu")
        self._print_centered("What would you like to do today?")

        # Check if there are assignments in the list
        if (self._selected_course._assignment_list):
            self._print("[A] Add assignment")
            self._print("[E] Edit assignment")
            self._print("[R] Remove assignment")
            self._print("[G] Add grade")
            self._print("[M] Remove grade")
            self._print("[V] View assignments")
            self._print("[X] Exit to course menu")
        else:
            self._print("[A] Add assignment")
            self._print("[X] Exit to course menu")

    def display_view_assignment_menu(self) -> None:
        """Prints a menu of choices for the user to view a group of Assignments."""
        self.display_delim()
        self._print_centered("View Assignment Menu")
        self._print_centered("What group of assignments would you like to view?")
        self._print("[A] All assignments")
        self._print("[C] Completed assignments")
        self._print("[I] Incomplete assignments")
        self._print("[X] Exit to assignment menu")
    
    def display_term_list_info(self) -> None:
        """Displays information about all terms from TermController."""
        terms = self._controller.term_list
        
        for term in terms.values():
            self.display_secondary_delim()
            term.print_term_info(self._out_stream)
            self.display_secondary_delim()

    def display_course_list_info(self) -> None:
        """Displays information about all courses from the selected Term."""
        courses = self._selected_term.course_list
        
        for course in courses.values():
            self.display_secondary_delim()
            course.print_course_info(self._out_stream)
            self.display_secondary_delim()
            
    def display_assignment_list_info(self) -> None:
        """Displays information about all assignments from the selected Course."""
        assignments = self._selected_course._assignment_list
        
        # Return early if there are no assignments
        if not assignments:
            self.display_secondary_delim()
            self._print("No assignments to display.")
            self.display_secondary_delim()
            return
        
        for assignment in assignments.values():
            self.display_secondary_delim()
            assignment.print_assignment_info(self._out_stream)
            self.display_secondary_delim()
            
    def display_completed_assignment_info(self) -> None:
        """Displays information about completed assignments from the selected Course."""
        assignments = self._selected_course._assignment_list
        completed_assignments = False
        
        for assignment in assignments.values():
            if assignment.completed:
                self.display_secondary_delim()
                assignment.print_assignment_info(self._out_stream)
                self.display_secondary_delim()
                completed_assignments = True
        
        if not completed_assignments:
            self.display_secondary_delim()
            self._print("No completed assignments to display.")
            self.display_secondary_delim()
            
    def display_incomplete_assignment_info(self) -> None:
        """Displays information about incomplete assignments from the selected Course."""
        assignments = self._selected_course._assignment_list
        incomplete_assignments = False
        
        for assignment in assignments.values():
            if not assignment.completed:
                self.display_secondary_delim()
                assignment.print_assignment_info(self._out_stream)
                self.display_secondary_delim()
                incomplete_assignments = True
        
        if not incomplete_assignments:
            self.display_secondary_delim()
            self._print("No incomplete assignments to display.")
            self.display_secondary_delim()
            
    def display_invalid_selection(self) -> None:
        """Displays a message indicating an invalid selection was made."""
        self._print("Invalid selection. Please try again.")
