# Standard library imports
from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import TextIO
import utils

# Local imports
from controllers.term_controller import TermController
from models.assignment import Assignment
from models.course import Course
from models.term import Term


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

    number_of_credits_requested: bool = False
    number_of_credits_updated: bool = False

    active_requested: bool = False
    active_updated: bool = False

    def any_requested(self) -> bool:
        """Return whether any Course field was requested for edit.
        
        Returns:
            True if any of the five fields is requested for edit, False otherwise.
        """
        return self.title_requested or self.description_requested or self.start_date_requested \
            or self.end_date_requested or self.number_of_credits_requested or self.active_requested

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
    """A class that shows the state of Assignment field updates for edit_assignment."""
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


class MenuState(Enum):
    """An enum that represents the current menu state of the CLI."""
    TERM = 0
    COURSE = 1
    ASSIGNMENT = 2
    EXIT = 3


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

    def _read_line(self, prompt: str) -> str:
        """Write a prompt to the output stream and read one line from the input stream.

        Args:
            prompt: The prompt text to display.

        Returns:
            The line read, without the trailing newline.
        """
        self._out_stream.write(prompt)
        self._out_stream.flush()
        return self._in_stream.readline().rstrip("\n")

    def _get_char_input(self, label: str, default_val: str) -> str:
        """Ask the user for a char input, using the default value 
        in the case of an invalid input.
        
        Args:
            label: The label to display to the user.
            default_val: The default value to use if the user provides no input.
            
        Returns:
            The user's input or the default value.
        """
        user_input = self._read_line(f"{label} [default: {default_val}]: ")

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
        user_input = self._read_line(f"{label} [default: {default_val}]: ")

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
        user_input = self._read_line(f"{label}: ")

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
        user_input = self._read_line(f"{label} [default: {default_val}]: ")

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
        user_input = self._read_line(f"{label} [default: {default_val}]: ")

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
        user_input = self._read_line(f"{label} [default: {default_to_string}]: ")

        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val

        # Convert string to lowercase, then convert string to bool
        input_lower = user_input.lower()
        
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
        user_input = self._read_line(f"{label} [default: {default_val}]: ")
        
        # Check if input is empty
        if not user_input.strip():
            self._print("No input provided, using default value.")
            return default_val
        
        if "/" in user_input:
            # Slash found, use point-based version
            return self._get_grade_points_input(user_input, default_val)
        else:
            # Slash not found, use percentage-based version
            return self._get_grade_pct_input(user_input, default_val)
    
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
        
    def _get_grade_points_input(self, user_input: str, default_val: float) -> float:
        """Parse point-based grade input in the form 0.0/0.0 and output the calculation,
        using the default value if the input is invalid.
        
        Args:
            user_input: The user's input.
            default_val: The default value to use if the input is invalid.
            
        Returns:
            The user's input or the default value.
        """
        values = user_input.split("/")
        if len(values) != 2:
            self._print("Invalid grade input, using default value.")
            return default_val
        try:
            points_earned = float(values[0])
            total_points = float(values[1])
            calculated_grade = (points_earned / total_points) * 100
            return round(calculated_grade, 2)
        except (ValueError, ZeroDivisionError):
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
        invalid_active = True
        
        self._print("Enter the following information for the term you want to add: ")
        
        while title_empty:
            title = self._get_string_input("Title", "")
            
            if title.strip():
                title_empty = False
            else:
                self._print("Title cannot be empty. Please try again.")
        
        while invalid_start_date:
            start_date = self._get_date_input("Start Date (MM-DD-YYYY)", \
                utils.default_start_date)
            invalid_start_date = False
        
        while invalid_end_date:
            end_date = self._get_date_input("End Date (MM-DD-YYYY)", \
                utils.default_end_date)

            try:
                utils.validate_date_order(start_date, end_date)
                invalid_end_date = False
            except ValueError:
                self._print("End date must be after start date. Please try again.")
        
        while invalid_active:
            try:
                active = self._get_bool_input("Current term? (yes/no)", True)
                invalid_active = False
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
        
        self._print("Enter the following information for the term you want to edit:")
        title = self._get_string_input("Title", "")
        
        try:
            self._selected_term = self._controller.find_term(title)
        except ValueError:
            self._print("Term not found. Operation cancelled.")
            return
        term_id = self._selected_term.id
        
        # Get fields that need to be updated and normalize input
        self._print("Fields available: title, start date, end date, active")
        to_update = self._get_string_input("Fields to update (comma-separated)", "").lower()
        edit_fields = [f.strip() for f in to_update.split(",")]
        
        for field in edit_fields:
            if field == "title":
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
            elif field == "start date" or field == "startdate":
                result_flags.start_date_requested = True
                
                try:
                    new_start_date = self._get_date_input("New start date (MM-DD-YYYY)", "")
                    # Check date order if only start date is being edited
                    if "end date" not in edit_fields:
                        utils.validate_date_order(new_start_date, self._selected_term.end_date)
                    # Only update if start date is different
                    if new_start_date != self._selected_term.start_date:
                        self._controller.edit_start_date(term_id, new_start_date)
                        result_flags.start_date_updated = True
                except ValueError:
                    self._print("Invalid date value. Cannot update start date.")
            elif field == "end date" or field == "enddate":
                result_flags.end_date_requested = True
                
                try:
                    new_end_date = self._get_date_input("New end date (MM-DD-YYYY)", "")
                    # Check date order
                    utils.validate_date_order(self._selected_term.start_date, new_end_date)
                    # Only update if end date is different
                    if new_end_date != self._selected_term.end_date:
                        self._controller.edit_end_date(term_id, new_end_date)
                        result_flags.end_date_updated = True
                except ValueError:
                    self._print("Invalid date value. Cannot update end date.")
            elif field == "active":
                result_flags.active_requested = True
                
                try:
                    new_active = self._get_bool_input("Is this a current term? (yes/no)", True)
                    # Only update if active flag is different
                    if new_active != self._selected_term.active:
                        self._controller.edit_active(term_id, new_active)
                        result_flags.active_updated = True
                except ValueError:
                    self._print("Invalid boolean value. Cannot update active flag.")
            else:
                self._print(f"Unknown field: {field}. Skipping.")
        
        # Update result output
        if result_flags.any_requested():
            self._print("Update results:")
            
            if result_flags.title_requested:
                if result_flags.title_updated:
                    self._print(f"Title: {self._selected_term.title}")
                else:
                    self._print("Title: (unchanged)")
                    
            if result_flags.dates_requested():
                if result_flags.dates_updated():
                    self._print(f"Duration: {self._selected_term.start_date} "
                        f"- {self._selected_term.end_date}")
                else:
                    self._print("Duration: (unchanged)")
                    
            if result_flags.active_requested:
                if result_flags.active_updated:
                    self._print(f"Current? {utils.bool_to_string(self._selected_term.active)}")
                else:
                    self._print("Current? (unchanged)")

        # Reset selected_term to allow the selection of a new one
        self._selected_term = None

    def prompt_select_term(self) -> None:
        """Prompt the user for the title to select a Term from the list."""
        self._print("Here is a list of all terms:")
        self.display_term_list_info()

        self._print("Enter the title of the term you want to select:")
        title = self._get_string_input("Title", "")
        
        try:
            self._selected_term = self._controller.find_term(title)
            self._print(f"Term '{title}' was selected.")
        except ValueError:
            self._print("Term not found. No selection made.")
            self._selected_term = None

    def prompt_remove_term(self) -> None:
        """Prompt the user for the title to remove a Term from the list."""
        invalid_bool = True

        self._print("Enter the title of the term you want to remove:")
        title = self._get_string_input("Title", "")
        
        # Confirmation before removal
        confirm = False
        while invalid_bool:
            try:
                confirm = self._get_bool_input("Are you sure you want to remove "
                    "this term? (yes/no)", False)
                invalid_bool = False
            except ValueError:
                self._print("Invalid response. Please enter 'yes' or 'no'.")

        if confirm:
            try:
                self._controller.remove_term(title)
                self._print(f"Term '{title}' was removed.")
            except ValueError:
                self._print("Term not found. No term was removed.")
        else:
            self._print(f"Operation cancelled. Term '{title}' was not removed.")

    def prompt_add_course(self) -> None:
        """Prompt the user for information to add a Course into the list."""
        title_empty = True
        invalid_start_date = True
        invalid_end_date = True
        invalid_num_credits = True
        invalid_active = True

        self._print("Enter the following information for the course you want to add:")
        
        while title_empty:
            title = self._get_string_input("Title", "")

            if title:
                title_empty = False
            else:
                self._print("Title cannot be empty. Please try again.")
        
        description = self._get_string_input("Description", "")
        # Set description to empty string if it only contains whitespace
        if description.isspace():
            description = ""

        while invalid_start_date:
            start_date = self._get_date_input("Start Date (MM-DD-YYYY)", \
                utils.default_start_date)
            invalid_start_date = False
        
        while invalid_end_date:
            end_date = self._get_date_input("End Date (MM-DD-YYYY)", \
                utils.default_end_date)
            
            try:
                utils.validate_date_order(start_date, end_date)
                invalid_end_date = False
            except ValueError:
                self._print("End date must be after start date. Please try again.")

        while invalid_num_credits:
            num_credits = self._get_int_input("Number of Credits", 0)
            
            if num_credits < 0:
                self._print("Invalid number of credits. Number of credits must be greater"
                    "than or equal to 0. Please try again.")
            else:
                invalid_num_credits = False

        while invalid_active:
            try:
                active = self._get_bool_input("Current term? (yes/no)", True)
                invalid_active = False
            except ValueError:
                self._print("Invalid input. Please try again.")

        try:
            course_controller = self._controller.get_course_controller()
            course_controller.add_course(title, description, start_date, end_date,
                num_credits, active)
            self._print(f"Course '{title}' successfully added.")
        except ValueError:
            self._print("A course with this title already exists. Please choose a new title.")

    def prompt_edit_course(self) -> None:
        """Prompt the user for information to edit a Course in the current list."""
        result_flags = EditCourseResult()
        course_controller = self._controller.get_course_controller()

        self._print("Enter the following information for the course you want to edit:")
        title = self._get_string_input("Title", "")
        
        try:
            self._selected_course = course_controller.find_course(title)
        except ValueError:
            self._print("Course not found. Operation cancelled.")
            return
        course_id = self._selected_course.id

        # Get fields that need to be updated and normalize input
        self._print("Fields available: title, description, start date, end date, "
            "number of credits, active")
        to_update = self._get_string_input("Fields to update (comma-separated)", "").lower()
        edit_fields = [f.strip() for f in to_update.split(",")]

        for field in edit_fields:
            if field == "title":
                result_flags.title_requested = True
                
                try:
                    new_title = self._get_string_input("New title", "")
                    utils.validate_req_string(new_title, "Title")
                    course_controller.edit_title(course_id, new_title)
                    result_flags.title_updated = True
                except ValueError:
                    if not new_title or new_title.isspace():
                        self._print("Empty title not allowed. Cannot update title.")
                    else:
                        self._print("A course with this title already exists. "
                            "Cannot update title.")
            elif field == "description":
                result_flags.description_requested = True
                
                try:
                    old_description = self._selected_course.description
                    new_description = self._get_string_input("New description", "")
                    course_controller.edit_description(course_id, new_description)

                    # Only set description_updated if old and new descriptions are different
                    if new_description != old_description:
                        result_flags.description_updated = True
                except ValueError:
                    if not new_description or new_description.isspace():
                        self._print("Empty description not allowed. "
                            "Cannot update description.")
            elif field == "start date" or field == "startdate":
                result_flags.start_date_requested = True
                
                try:
                    new_start_date = self._get_date_input("New start date (MM-DD-YYYY)", "")
                    # Check date order if only start date is being edited
                    if "end date" not in edit_fields:
                        utils.validate_date_order(new_start_date, 
                            self._selected_course.end_date)
                    # Only update if start date is different
                    if new_start_date != self._selected_course.start_date:
                        course_controller.edit_start_date(course_id, new_start_date)
                        result_flags.start_date_updated = True
                except ValueError:
                    self._print("Invalid date value. Cannot update start date.")
            elif field == "end date" or field == "enddate":
                result_flags.end_date_requested = True
                
                try:
                    new_end_date = self._get_date_input("New end date (MM-DD-YYYY)", "")
                    # Check date order
                    utils.validate_date_order(self._selected_course.start_date, new_end_date)
                    # Only update if end date is different
                    if new_end_date != self._selected_course.end_date:
                        course_controller.edit_end_date(course_id, new_end_date)
                        result_flags.end_date_updated = True
                except ValueError:
                    self._print("Invalid date value. Cannot update end date.")
            elif field == "number of credits" or field == "numberofcredits" \
                    or field == "numcredits":
                result_flags.num_credits_requested = True
                
                try:
                    new_num_credits = self._get_int_input("New number of credits", 3)
                    if new_num_credits < 0:
                        self._print("Invalid number of credits. Number of credits must be "
                            "greater than or equal to 0. Cannot update number of credits.")
                    else:
                        # Only update if number of credits is different
                        if new_num_credits != self._selected_course.num_credits:
                            course_controller.edit_num_credits(course_id, new_num_credits)
                            result_flags.num_credits_updated = True
                except ValueError:
                    self._print("Number of credits must be a valid integer. Cannot update "
                        "number of credits.")
            elif field == "active":
                result_flags.active_requested = True
                
                try:
                    new_active = self._get_bool_input("Is this a current course? (yes/no)",
                        True)
                    # Only update if active flag is different
                    if new_active != self._selected_course.active:
                        course_controller.edit_active(course_id, new_active)
                        result_flags.active_updated = True
                except ValueError:
                    self._print("Invalid boolean value. Cannot update active flag.")
            else:
                self._print(f"Unknown field '{field}'. Skipping.")

        # Update result output
        if result_flags.any_requested():
            self._print("Update results:")

            if result_flags.title_requested:
                if result_flags.title_updated:
                    self._print(f"Title: {self._selected_course.title}")
                else:
                    self._print("Title: (unchanged)")

            if result_flags.description_requested:
                if result_flags.description_updated:
                    self._print(f"Description: {self._selected_course.description}")
                else:
                    self._print("Description: (unchanged)")

            if result_flags.dates_requested():
                if result_flags.dates_updated():
                    self._print(f"Duration: {self._selected_course.start_date} - "
                        f"{self._selected_course.end_date}")
                else:
                    self._print("Duration: (unchanged)")

            if result_flags.num_credits_requested:
                if result_flags.num_credits_updated:
                    self._print(f"Number of credits: {self._selected_course.num_credits}")
                else:
                    self._print("Number of credits: (unchanged)")
                    
            if result_flags.active_requested:
                if result_flags.active_updated:
                    self._print(f"Current? {self._selected_course.active}")
                else:
                    self._print("Current? (unchanged)")

        # Reset selected_course to allow the selection of a new one
        self._selected_course = None

    def prompt_select_course(self) -> None:
        """Prompt the user to select a Course from the list."""
        course_controller = self._controller.get_course_controller()
        
        self._print("Here is a list of all courses:")
        self.display_course_list_info()

        self._print("Enter the following information for the course you want to select:")
        title = self._get_string_input("Title", "")
        
        try:
            self._selected_course = course_controller.find_course(title)
            self._print(f"Course '{title}' was selected.")
        except ValueError:
            self._print("Course not found. No selection made.")
            self._selected_course = None

    def prompt_remove_course(self) -> None:
        """Prompt the user to remove a Course from the list."""
        invalid_bool = True
        course_controller = self._controller.get_course_controller()
        
        self._print("Enter the following information for the course you want to remove:")
        title = self._get_string_input("Title", "")
        
        # Confirmation before removal
        confirm = False
        while invalid_bool:
            try:
                confirm = self._get_bool_input("Are you sure you want to remove "
                    "this course? (yes/no)", False)
                invalid_bool = False
            except ValueError:
                self._print("Invalid response. Please enter 'yes' or 'no'.")

        if confirm:
            try:
                course_controller.remove_course(title)
                self._print(f"Course '{title}' was removed.")
            except ValueError:
                self._print("Course not found. No Course was removed.")
        else:
            self._print(f"Operation cancelled. Course '{title}' was not removed.")

    def prompt_add_assignment(self) -> None:
        """Prompt the user for information to add an Assignment into the list."""
        title_empty = True
        invalid_category = True
        invalid_due_date = True
        invalid_completed = True
        invalid_grade = True

        self._print("Enter the following information for the assignment you want to add:")

        while title_empty:
            title = self._get_string_input("Title", "")

            if title:
                title_empty = False
            else:
                self._print("Title cannot be empty. Please try again.")

        description = self._get_string_input("Description", "")
        # Set description to empty string if it only contains whitespace
        if description.isspace():
            description = ""

        while invalid_category:
            try:
                category = self._get_string_input("Category", "")
                utils.validate_req_string(category, "Category")
                category = category.strip()

                if category not in self._selected_course.grade_weights:
                    raise KeyError("Category must be in grade weights.")

                invalid_category = False
            except KeyError:
                self._print("Category must be in grade weights. Please try again.")
            except ValueError:
                self._print("Invalid category. Category cannot be empty. Please try again.")
        
        while invalid_due_date:
            try:
                due_date = self._get_date_input("Due Date (MM/DD/YYYY)", "")

                if not due_date:
                    self._print("Due date is empty. Using default date.")
                invalid_due_date = False
            except ValueError:
                self._print("Invalid due date. Please enter a valid date.")

        while invalid_completed:
            try:
                completed = self._get_bool_input("Completed assignment? (yes/no)", False)
                invalid_completed = False
            except ValueError:
                self._print("Invalid input. Please try again.")
        
        # Only set grade if completed is True; otherwise, use default
        if completed:
            while invalid_grade:
                grade = self._get_grade_input("Grade", 0.0)

                if grade > 150.0 or grade < 0.0:
                    self._print("Invalid grade. Grade must be from 0 to 150. Please try again.")
                else:
                    invalid_grade = False
        else:
            grade = 0.0

        try:
            assignment_controller = (
                self
                ._controller
                .get_course_controller()
                .get_assignment_controller()
            )
            assignment_controller.add_assignment(title, description, category, due_date,
                completed, grade)
            self._print(f"Assignment '{title}' successfully added.")
        except Exception:
            self._print("An Assignment with this title already exists. Please choose a new title.")

    def prompt_edit_assignment(self) -> None:
        """Prompt the user for information to edit an Assignment in the current list."""
        result_flags = EditAssignmentResult()
        assignment_controller = (
            self
            ._controller
            .get_course_controller()
            .get_assignment_controller()
        )

        self._print("Enter the following information for the Assignment you want to edit:")
        title = self._get_string_input("Title", "")

        try:
            self._selected_assignment = assignment_controller.get_assignment_by_title(title)
        except Exception:
            self._print("Assignment not found. Operation cancelled.")
            return
        assignment_id = self._selected_assignment.assignment_id

        # Get fields that need to be updated and normalize input
        self._print("Fields available: title, description, category, due date")
        to_update = self._get_string_input("Fields to update (comma-separated)", "").lower()
        edit_fields = [field.strip() for field in to_update.split(",")]
        
        # Get updated info and perform update
        for field in edit_fields:
            if field == "title":
                result_flags.title_requested = True

                try:
                    new_title = self._get_string_input("New title", "")
                    utils.validate_req_string(new_title, "Title")
                    assignment_controller.edit_title(assignment_id, new_title)
                    result_flags.title_updated = True
                except ValueError:
                    if not new_title or new_title.isspace():
                        self._print("Empty title not allowed. Cannot update title.")
                    else:
                        self._print("A course with this title already exists. "
                            "Cannot update title.")
            elif field == "description":
                result_flags.description_requested = True
                
                old_description = self._selected_assignment.description
                new_description = self._get_string_input("New description", "")
                assignment_controller.edit_description(assignment_id, new_description)

                # Only set description_updated if old and new descriptions are different
                if old_description != new_description:
                    result_flags.description_updated = True
            elif field == "category":
                result_flags.category_requested = True

                try:
                    new_category = self._get_string_input("New category", "")

                    # Only update if category is different
                    if new_category != self._selected_assignment.category:
                        assignment_controller.edit_category(assignment_id, new_category)
                        result_flags.category_updated = True
                except ValueError:
                    self._print("Invalid category. Category must be in grade weights. "
                        "Cannot update category.")
            elif field == "due date" or field == "duedate":
                result_flags.due_date_requested = True

                try:
                    new_due_date = self._get_date_input("New due date (MM-DD-YYYY)", "")
                    
                    # Only update if due date is different
                    if new_due_date != self._selected_assignment.due_date:
                        assignment_controller.edit_due_date(assignment_id, new_due_date)
                        result_flags.due_date_updated = True
                except ValueError:
                    self._print("Invalid date value. Cannot update due date.")
            else:
                self._print(f"Unknown field: {field}. Skipping.")

        if result_flags.any_requested():
            self._print("Update results:")

            if result_flags.title_requested:
                if result_flags.title_updated:
                    self._print(f"Title: {self._selected_assignment.title}")
                else:
                    self._print("Title: (unchanged)")
            
            if result_flags.description_requested:
                if result_flags.description_updated:
                    self._print(f"Description: {self._selected_assignment.description}")
                else:
                    self._print("Description: (unchanged)")
            
            if result_flags.category_requested:
                if result_flags.category_updated:
                    self._print(f"Category: {self._selected_assignment.category}")
                else:
                    self._print("Category: (unchanged)")
            
            if result_flags.due_date_requested:
                if result_flags.due_date_updated:
                    self._print(f"Due Date: {self._selected_assignment.due_date}")
                else:
                    self._print("Due Date: (unchanged)")

            # Reset selected_assignment to allow the selection of a new one
            self._selected_assignment = None

    def prompt_remove_assignment(self) -> None:
        """Prompt the user for the title to remove an Assignment from the list."""
        invalid_bool = True
        assignment_controller = (
            self
            ._controller.get_course_controller()
            .get_assignment_controller()
        )

        self._print("Enter the following information for the assignment you want to remove:")
        title = self._get_string_input("Title", "")
        
        # Confirmation before removal
        confirm = False
        while invalid_bool:
            try:
                confirm = self._get_bool_input("Are you sure you want to remove "
                    "this assignment? (yes/no): ", False)
                invalid_bool = False
            except ValueError:
                self._print("Invalid input. Please enter 'yes' or 'no'.")

        if confirm:
            try:
                assignment_controller.remove_assignment(title)
                self._print(f"Assignment '{title}' was removed.")
            except ValueError:
                self._print("Assignment not found. Operation cancelled.")
        else:
            self._print(f"Operation cancelled. Assignment '{title}' was not removed.")

    def prompt_add_assignment_grade(self) -> None:
        """Prompt the user for the Assignment and grade they want to add."""
        assignment_controller = (
            self
            ._controller
            .get_course_controller()
            .get_assignment_controller()
        )

        self._print("Enter the following information for the assignment grade you want to add:")
        title = self._get_string_input("Title", "")
        try:
            assignment_controller.find_assignment(title)
        except ValueError:
            self._print("Assignment not found. Operation cancelled.")
            return
        
        try:
            grade = self._get_float_input("Grade", -1.0)
            assignment_controller.add_grade(title, grade)
            self._print(f"Grade {grade} added to assignment '{title}'.")
        except ValueError:
            self._print("Invalid grade. Grade must be in range 0 to 150. Operation cancelled.")
            return

    def prompt_remove_assignment_grade(self) -> None:
        """Prompt the user for the Assignment and grade they want to remove."""
        invalid_bool = True
        assignment_controller = (
            self
            ._controller
            .get_course_controller()
            .get_assignment_controller()
        )

        self._print("Enter the following information for the assignment grade you want to remove:")
        title = self._get_string_input("Title", "")
        
        # Confirmation before removal
        confirm = False
        while (invalid_bool):
            try:
                confirm = self._get_bool_input("Are you sure you want to remove the "
                    "grade from this assignment? (yes/no): ", False)
                invalid_bool = False
            except ValueError:
                self._print("Invalid input. Please enter 'yes' or 'no'.")
        
        if confirm:
            try:
                assignment_controller.remove_grade(title)
                self._print(f"Grade removed from assignment '{title}'.")
            except ValueError:
                self._print("Assignment not found. Operation cancelled.")
        else:
            self._print(f"Operation cancelled. The grade of assignment '{title}' was not removed.")

    def prompt_view_assignment(self) -> None:
        """Prompt the user for the group of Assignments they want to view."""
        self.display_view_assignment_menu()

        user_input = self._get_char_input("Response", "X").upper()

        match user_input:
            case "A":
                self.display_assignment_list_info()
            case "C":
                self.display_completed_assignment_info()
            case "I":
                self.display_incomplete_assignment_info()
            case "X":
                return
            case _:
                self.display_invalid_selection()

    def run(self) -> None:
        """Starts the main CLI loop and handles user interaction for the program."""
        state = MenuState.TERM
        self.display_intro()

        while state != MenuState.EXIT:
            while state == MenuState.TERM:
                self.display_term_menu()
                user_input = self._get_char_input("Response", "X").upper()

                match user_input:
                    case "A":
                        # Add Term
                        self.prompt_add_term()
                    case "E":
                        # Edit Term
                        if len(self._controller.term_list) > 0:
                            self.prompt_edit_term()
                        else:
                            self.display_invalid_selection()
                    case "S":
                        # Select Term
                        if len(self._controller.term_list) > 0:
                            self.prompt_select_term()

                            if self._selected_term:
                                self._controller.select_term(self._selected_term.title)
                                state = MenuState.COURSE
                        else:
                            self.display_invalid_selection()
                    case "R":
                        # Remove Term
                        if len(self._controller.term_list) > 0:
                            self.prompt_remove_term()
                        else:
                            self.display_invalid_selection()
                    case "X":
                        # Exit
                        state = MenuState.EXIT
                    case _:
                        # Invalid selection
                        self.display_invalid_selection()

            while state == MenuState.COURSE:
                self.display_course_menu()
                user_input = self._get_char_input("Response", "X").upper()
                
                match user_input:
                    case "A":
                        # Add Course
                        self.prompt_add_course()
                    case "E":
                        # Edit Course
                        if len(self._selected_term.course_list) > 0:
                            self.prompt_edit_course()
                        else:
                            self.display_invalid_selection()
                    case "S":
                        # Select Course
                        if len(self._selected_term.course_list) > 0:
                            self.prompt_select_course()
                            
                            if self._selected_course:
                                (
                                    self
                                    ._controller
                                    .get_course_controller()
                                    .select_course(self._selected_course.title)
                                )
                                state = MenuState.ASSIGNMENT
                        else:
                            self.display_invalid_selection()
                    case "R":
                        # Remove Course
                        if len(self._selected_term.course_list) > 0:
                            self.prompt_remove_course()
                        else:
                            self.display_invalid_selection()
                    case "X":
                        # Exit
                        self._selected_term = None
                        state = MenuState.TERM
                    case _:
                        # Invalid selection
                        self.display_invalid_selection()

            while state == MenuState.ASSIGNMENT:
                self.display_assignment_menu()
                user_input = self._get_char_input("Response", "X").upper()
                
                match user_input:
                    case "A":
                        # Add Assignment
                        self.prompt_add_assignment()
                    case "E":
                        # Edit Assignment
                        if len(self._selected_course.assignment_list) > 0:
                            self.prompt_edit_assignment()
                        else:
                            self.display_invalid_selection()
                    case "R":
                        # Remove Assignment
                        if len(self._selected_course.assignment_list) > 0:
                            self.prompt_remove_assignment()
                        else:
                            self.display_invalid_selection()
                    case "G":
                        # Add grade
                        if len(self._selected_course.assignment_list) > 0:
                            self.prompt_add_assignment_grade()
                        else:
                            self.display_invalid_selection()
                    case "M":
                        # Remove grade
                        if len(self._selected_course.assignment_list) > 0:
                            self.prompt_remove_assignment_grade()
                        else:
                            self.display_invalid_selection()
                    case "V":
                        # View assignment
                        if len(self._selected_course.assignment_list) > 0:
                            self.prompt_view_assignment()
                        else:
                            self.display_invalid_selection()
                    case "X":
                        # Exit
                        self._selected_course = None
                        self._selected_assignment = None
                        state = MenuState.COURSE
                    case _:
                        # Invalid selection
                        self.display_invalid_selection()
