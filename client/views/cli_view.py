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

    def _get_char_input(self, label: str, default_val: str) -> str:
        """Ask the user for a char input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label} [default: {default_val}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        if len(user_input) == 1:
            return user_input
        
        # Error message for multiple character input
        self._print("Invalid input. Please enter a single character.")
        return ""
    
    def _get_string_input(self, label: str, default_val: str) -> str:
        """Ask the user for a string input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label} [default: {default_val}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val
        
        return user_input
    
    def _get_date_input(self, label: str, default_val: str) -> datetime:
        """Ask the user for a date input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label}: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        try:
            return datetime.strptime(user_input, '%m-%d-%Y')
        except ValueError:
            self._print("Invalid date format. Please use MM-DD-YYYY.")
            return default_val

    def _get_float_input(self, label: str, default_val: float) -> float:
        """Ask the user for a float input, using the default value 
        in the case of an invalid input
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label} [default: {default_val}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        try:
            return float(user_input)
        except ValueError:
            self._print("Invalid float input, using default value.")
            return default_val

    def _get_int_input(self, label: str, default_val: int) -> int:
        """Ask the user for an int input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label} [default: {default_val}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        try:
            return int(user_input)
        except ValueError:
            self._print("Invalid integer input, using default value.")
            return default_val

    def _get_bool_input(self, label: str, default_val: bool) -> bool:
        """Ask the user for a bool input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        default_to_string = utils.bool_to_string(default_val).lower()
        user_input = input(f"{label} [default: {default_to_string}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        # Convert string to loewrcase, then convert string to bool
        input_lower = input.lower()
        
        if input_lower == "true" or input_lower == "1" or \
                input_lower == "yes" or input_lower == "y":
            return True
        elif input_lower == "false" or input_lower == "0" or \
                input_lower == "no" or input_lower == "n":
            return False
        else:
            raise ValueError("Invalid boolean string.")

    def _get_grade_input(self, label: str, default_val: float) -> float:
        """Ask the user for grade input and detect the format based on the input string.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = input(f"{label} [default: {default_val}]: ")
        
        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val
        
        if "/" in user_input:
            # Slash found, use point-based version
            return get_grade_points_input(input, default_val)
        else:
            # Slash not found, use percentage-based version
            return get_grade_pct_input(input, default_val)
    
    def _get_grade_pct_input(self, user_input: str, defualt_val: float) -> float:
        """Parse percentage-based grade input in float form (0.0) and output the value,
        using the default value if the input is invalid.
        
        Args:
            user_input: The user's input.
            defualt_val: The default value to use if the input is invalid.
            
        Returns:
            The user's input or the default value.
        """
        try:
            return round(float(user_input), 2)
        except ValueError:
            self._print("Invalid grade input, using default value.")
            return defualt_val
        
    def _get_grade_points_input(self, input: str, default_val: float) -> float:
        """Parse point-based grade input in the form 0.0/0.0 and output the calculation,
        using the default value if the input is invalid.
        
        Args:
            input: The user's input.
            default_val: The default value to use if the input is invalid.
            
        Returns:
            The user's input or the default value.
        """
        values = input.split("/")
        if len(values) != 2:
            self._print("Invalid grade input, using default value.")
            return default_val
        try:
            points_earned = values[0]
            total_points = values[1]
            calculated_grade = (points_earned / total_points) * 100
            return round(calculated_grade, 2)
        except (ValueError, IndexError):
            self._print("Invalid grade input, using default value.")
            return default_val

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

    def prompt_add_term(self) -> None:
        """Prompt the user for information to add a Term to the list."""
        title_empty = True
        invalid_start_date = True
        invalid_end_date = True
        invalid_date_order = True
        invalid_active = True
        
        self._print("Enter the following information for the term you'd like to add: ")
        
        while title_empty:
            title = self._get_string_input("Title", "")
            
            if title.strip():
                title_empty = False
            else:
                self._print("Title cannot be empty. Please try again.")
        
        while invalid_start_date:
            start_date = self._get_date_input("Start Date (MM-DD-YYYY)", \
                utils.default_start_date)

            try:
                datetime.strptime(start_date, "%m-d-%Y")
                invalid_start_date = False
            except ValueError:
                self._print("Invalid date format. Please try again.")
        
        while invalid_end_date:
            end_date = self._get_date_input("End Date (MM-DD-YYYY)", \
                utils.default_end_date)
            
            
            try:
                datetime.strptime(end_date, "%m-%d-%Y")
                invalid_end_date = False
                utils.validate_date_order(start_date, end_date)
                invalid_date_order = False
            except ValueError:
                if invalid_date_order:
                    self._print("Invalid date format. Please try again.")
                else:
                    self._print("End date must be after start date. Please try again.")
        
        while invalid_active:
            try:
                active = self._get_bool_input("Current term? (yes/no)", True)
            except ValueError:
                self._print("Invalid input. Please try again.")
        
        try:
            self._controller.add_term(title, start_date, end_date, active)
            self._print(f"Term '{title}' successfully added.")
        except ValueError:
            self._print("A term with this title already exists. Please choose a new title.")

    def prompt_edit_term(self) -> None:
        """Prompt the user for information to edit a Term in the current list."""
        result_flags = EditTermResult()
        edit_fields = []
        
        self._print("Enter the following information for the term you'd like to edit:")
        title = self._get_string_input("Title", "")
        
        try:
            selected_term = self._controller.find_term(title)
        except ValueError:
            self._print("Term not found. Operation cancelled.")
            return
        term_id = selected_term.id
        
        # Get fields that need to be updated and normalize input
        self._print("Fields available: title, start date, end date, active")
        to_update = self._get_string_input("Fields to update (comma-separated)", "")
        edit_fields = [f.strip() for f in to_update.split(",")]
        
        for field in edit_fields:
            match field:
                case "title":
                    result_flags.title_requested = True
                    
                    try:
                        new_title = self._get_string_input("New title", "")
                        utils.validate_req_string(new_title, "Title")
                        self._controller.edit_title(term_id, new_title)
                        result_flags.title_updated = True
                    except ValueError:
                        if not new_title or new_title.isspace():
                            self._print("Empty title not allowed. Cannot update title.")
                        else:
                            self._print("A term with this title already exists. "
                                "Cannot update title.")
                case "start date" | "startdate":
                    result_flags.start_date_requested = True
                    
                    try:
                        new_start_date = self._get_date_input("New start date (MM-DD-YYYY)", "")
                        # Check date order if only start date is being edited
                        if "end date" not in edit_fields:
                            utils.validate_date_order(new_start_date, selected_term.end_date)
                        # Only update if start date is different
                        if new_start_date != selected_term.start_date:
                            self._controller.edit_start_date(term_id, new_start_date)
                            result_flags.start_date_updated = True
                    except ValueError:
                        self._print("Invalid date value. Cannot update start date.")
                case "end date" | "enddate":
                    result_flags.end_date_requested = True
                    
                    try:
                        new_end_date = self._get_date_input("New end date (MM-DD-YYYY)", "")
                        # Check date order
                        utils.validate_date_order(selected_term.start_date, new_end_date)
                        # Only update if end date is different
                        if new_end_date != selected_term.end_date:
                            self._controller.edit_end_date(term_id, new_end_date)
                            result_flags.end_date_updated = True
                    except ValueError:
                        self._print("Invalid date value. Cannot update end date.")
                case "active":
                    result_flags.active_requested = True
                    
                    try:
                        new_active = self._get_bool_input("Is this a current term? (yes/no)", True)
                        # Only update if active flag is different
                        if new_active != selected_term.is_active:
                            self._controller.edit_active(term_id, new_active)
                            result_flags.active_updated = True
                    except ValueError:
                        self._print("Invalid boolean value. Cannot update active flag.")
                case _:
                    self._print(f"Unknown field: {field}. Skipping.")
        
        # Update result output
        if result_flags.any_requested():
            self._print("Update results:")
            
            if result_flags.title_requested:
                if result_flags.title_updated:
                    self._print(f"Title: {selected_term.title}")
                else:
                    self._print("Title: (unchanged)")
                    
            if result_flags.dates_requested():
                if result_flags.dates_updated():
                    self._print(f"Duration: {selected_term.start_date} - {selected_term.end_date}")
                else:
                    self._print("Duration: (unchanged)")
                    
            if result_flags.active_requested:
                if result_flags.active_updated:
                    self._print(f"Current? {utils.bool_to_string(selected_term.active)}")
                else:
                    self._print("Current? (unchanged)")

        # Reset selected_term to allow the selection of a new one
        selected_term.reset()
