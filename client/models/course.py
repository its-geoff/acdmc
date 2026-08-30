# Standard library imports
import math
import sys
from datetime import date
from typing import Self, TextIO

# Local imports
import utils
from assignment import Assignment


class Course:
    """Client-side Course model."""

    # Class constants
    GRADE_WEIGHTS_DEFAULT: dict[str, float] = {
        "Homework": 0.25,
        "Midterm": 0.35,
        "Final Exam": 0.4
    }
    """Default grade weights if unset; must add up to 1.0."""

    GRADE_SCALE_DEFAULT: dict[float, str] = {
        97.0: "A+",
        93.0: "A",
        90.0: "A-",
        87.0: "B+",
        83.0: "B",
        80.0: "B-",
        77.0: "C+",
        73.0: "C",
        70.0: "C-",
        67.0: "D+",
        63.0: "D",
        60.0: "D-",
        0.0: "F"
    }
    """Associates each percentage range to a letter grade."""

    GPA_SCALE: dict[str, float] = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "D-": 0.7,
        "F": 0.0,
        "N/A": 0.0
    }
    """Associates each letter grade to a GPA value."""

    def __init__(
            self,
            title: str,
            description: str,
            start_date: date,
            end_date: date,
            num_credits: int,
            active: bool = True):
        # UUID v4 generated during creation
        self.id: str = utils.generate_uuid()
        self._title: str = utils.validate_req_string(title, "Title")
        # Only set description if it's not empty or whitespace
        self._description: str = description if description and not description.isspace() else ""
        self._start_date: date = utils.validate_date(start_date)
        self._end_date: date = utils.validate_date(end_date)
        utils.validate_date_order(start_date, end_date)

        # Maps id -> Assignment
        self._assignment_list: dict[str, Assignment] = {}
        self._num_credits: int = 3
        self._grade_percentage: float = 0.0
        self.active: bool = active

        self._grade_weights: dict[str, float] = Course.GRADE_WEIGHTS_DEFAULT.copy()
        self._grade_scale: dict[float, str] = Course.GRADE_SCALE_DEFAULT.copy()
        self._gpa_scale: dict[str, float] = Course.GPA_SCALE.copy()

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id

    @property
    def title(self) -> str:
        """Get the title of a Course."""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = utils.validate_req_string(value, "Title")

    @property
    def description(self) -> str:
        """Get the description of a Course."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value if value and not value.isspace() else ""

    @property
    def start_date(self) -> date:
        """Get the start date of a Course."""
        return self._start_date
    
    @start_date.setter
    def start_date(self, value: date) -> None:
        self._start_date = utils.validate_date(value)
    
    @property
    def end_date(self) -> date:
        """Get the end date of a Course."""
        return self._end_date
    
    @end_date.setter
    def end_date(self, value: date) -> None:
        self._end_date = utils.validate_date(value)

    @property
    def grade_weights(self) -> dict[str, float]:
        """Get the grade weights of a Course."""
        return self._grade_weights

    @grade_weights.setter
    def grade_weights(self, value: dict[str, float]) -> None:
        self._grade_weights = self._validate_grade_weights(value)

    @property
    def num_credits(self) -> int:
        """Get the number of credits of a Course."""
        return self._num_credits

    @num_credits.setter
    def num_credits(self, value: int) -> None:
        self._num_credits = self._validate_num_credits(value)

    @property
    def grade_percentage(self) -> float:
        """Get the grade percentage of a Course."""
        return self._grade_percentage

    @grade_percentage.setter
    def grade_percentage(self, value: float | None = None) -> None:
        if value is None:
            self._grade_percentage = self._calculate_grade_percentage()
        else:
            self._grade_percentage = self._validate_grade_percentage(value)

    @property
    def letter_grade(self) -> str:
        """Recalculate and return the letter grade of a Course."""
        return self._calculate_letter_grade(self.grade_percentage)

    @property
    def gpa_value(self) -> float:
        """Recalculate and return the GPA value of a Course."""
        return self._calculate_gpa_value(self.letter_grade)

    @property
    def grade_scale(self) -> dict[float, str]:
        """Get the grade scale of a Course."""
        return self._grade_scale

    @grade_scale.setter
    def grade_scale(self, value: dict[float, str]) -> None:
        self._grade_scale = self._validate_grade_scale(value)

    @property
    def grades_by_category(self) -> dict[str, float]:
        return self._calculate_grades_by_category()

    def _validate_grade_weights(self, grade_weights: dict[str, float]):
        """Checks that the new list of grade weights is valid.
        
        Args:
            grade_weights: The new grade weights.
        
        Raises:
            ValueError: If the grade weights do not add up to 1.0.
        """
        total = 0.0

        for _, weight in grade_weights:
            total += weight

        if math.isclose(total, 1.0):
            raise ValueError("Grade weights must equal 100%.\n"
                "Current total: " + str(total * 100) + "%")

    def _validate_num_credits(self, num_credits: int) -> None:
        """Checks that the new number of credits is valid.

        Args:
            num_credits: The new number of credits.

        Raises:
            ValueError: If the number of credits is less than 0.
        """
        if (num_credits < 0):
            raise ValueError("Number of credits must be greater than or equal to 0.")
        
    def _validate_grade_percentage(self, grade_percentage: float) -> None:
        """Checks that the new grade percentage is valid.

        Args:
            grade_percentage: The new grade percentage.

        Raises:
            ValueError: If the grade percentage is less than 0 or greater than 150.
        """
        if (grade_percentage < 0.0 or grade_percentage > 150.0):
            raise ValueError("Grade percentage must be between 0 and 150.")
        
    def _validate_grade_scale(self, grade_scale: dict[float, str]) -> None:
        """Checks that the new grade scale is valid.

        Args:
            grade_scale: The new grade scale.
        
        Raises:
            ValueError: If the grade scale is empty or does not provide grades for the range 0-100.
        """
        if not grade_scale:
            raise ValueError("Grade scale must not be empty.")

        if 0.0 not in grade_scale:
            raise ValueError("Grade scale must include 0.")

        if any(k >= 100.0 for k in grade_scale.keys()):
            raise ValueError("Grade scale must not include values greater than 100.")

    def _calculate_grades_by_category(self) -> dict[str, float]:
        """Calculates grades for each category.
        
        Iterates over all assignments in the Course, groups completed assignments by category,
        and computes raw percentage grade for each category. The per-category averages will be
        weighted for the total grade calculation.
        """
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        output: dict[str, float] = {}

        # Add values from assignment list to totals and counts
        for _, assignment in self._assignment_list.items():
            if not assignment.completed:
                continue

            category = assignment.category
            totals[category] += assignment.grade
            counts[category] += 1

        self._grades_by_category.clear()

        # Calculate category grades and store in dictionary
        for category_name in self.grade_weights:
            if category_name not in counts or counts[category_name] == 0:
                continue
            
            category_grade = totals[category_name] / counts[category_name]
            output[category_name] = utils.float_round(category_grade, 2)
        
        return output

    def _calculate_grade_percentage(self) -> float:
        """Calculates course grade percentage using grades from each category.

        Returns:
            float: The course grade percentage.
        """
        if not self._assignment_list or self._calculate_completed_assignments() == 0:
            return 0.0

        total = 0.0
        # Used to redistribute weights if 1 or more categories are empty
        active_weight_total = 0.0

        # Sum categories that have grades
        for category, weight in self.grade_weights.items():
            if category in self.grades_by_category:
                active_weight_total += weight

        # Return early if no active categories
        if math.isclose(active_weight_total, 0.0):
            return 0.0

        # Normalize weights and calculate active grade
        for category_name, grade in self.grades_by_category.items():
            normalized_weight = self.grade_weights[category_name] / active_weight_total
            weighted_grade = grade * normalized_weight
            total += weighted_grade

        return utils.float_round(total, 2)

    def _calculate_letter_grade(self, 
            grade_percentage: float, 
            grade_scale: dict[float, str] | None = None) -> str:
        """Calculate letter grade based on grade percentage and given grade scale.

        Args:
            grade_percentage: The numeric grade percentage to convert.
            grade_scale: A dictionary mapping grade thresholds to letter grades.

        Returns:
            str: The appropriate letter grade based on the grade percentage and grade scale.
                Returns "N/A" when no assignments are completed.
        """
        if grade_scale is None:
            grade_scale = self.grade_scale
        
        if (utils.float_equal(grade_percentage, 0.0) 
                and self._calculate_completed_assignments() == 0):
            # Grade not determined if all assignments are incomplete
            return "N/A"

        # Find the largest key that is <= grade_percentage
        valid_keys = [k for k in grade_scale if k <= grade_percentage]
        
        if not valid_keys:
            # grade_percentage > all keys, use the largest key
            return grade_scale[max(grade_scale.keys())]
        
        return grade_scale[max(valid_keys)]

    def _calculate_gpa_value(self, letter_grade: str) -> float:
        """Calculate GPA value based on the letter grade.

        Args:
            letter_grade: The letter grade to convert to a GPA value.
        
        Returns:
            float: The GPA value that corresponds to the letter grade.
        """
        return self.gpa_scale.get(letter_grade)

    def _calculate_completed_assignments(self) -> int:
        """Calculate the number of completed Assignments by checking the completed field of
        each Assignment.

        Returns:
            int: The number of completed Assignments.
        """
        completed_assignments = 0

        for _, assignment in self._assignment_list.items():
            if assignment.completed:
                completed_assignments += 1
            
        return completed_assignments

    def print_course_info(self, output_stream: TextIO = sys.stdout) -> None:
        """Print the Course information to the specified output stream.
        
        Args:
            output_stream: The output stream to write to.
        """
        print(f"ID: {self.id}", file=output_stream)
        print(f"Course: {self.title}", file=output_stream)
        if self._description:
            print(f"Description: {self.description}", file=output_stream)
        print(f"Duration: {self.start_date} - {self.end_date}", file=output_stream)
        print(f"Number of Credits: {self.num_credits}", file=output_stream)
        print(f"Grade Percentage: {self.grade_percentage:.2f}%", file=output_stream)
        print(f"Letter Grade: {self.letter_grade}", file=output_stream)
        print(f"GPA Value: {self.gpa_value:.1f}", file=output_stream)
        print(f"Total Assignments: {len(self._assignment_list)}", file=output_stream)
        print(f"Incomplete Assignments: "
            f"{len(self._assignment_list) - self._calculate_completed_assignments()}",
            file=output_stream)
        print(f"Current? {utils.bool_to_string(self.active)}", file=output_stream)

    def add_assignment(self, assignment: Assignment) -> None:
        """Adds an Assignment to assignment_list using the given input.

        Args:
            assignment: The Assignment that will be added to assignment_list.
        """
        key = assignment.id
        insert = key not in self._assignment_list

        if not insert:
            raise ValueError(f"Assignment with ID {key} already exists in Course {self.title}.")

        self._assignment_list[key] = assignment
        # Trigger recalculation of grade percentage by setting to None
        self.grade_percentage = None

    def remove_assignment(self, id: str) -> None:
        """Removes an Assignment with the specified UUID.

        Args:
            id: The UUID of the Assignment to remove.
        """
        try:
            del self._assignment_list[id]
        except KeyError as e:
            raise KeyError("Assignment not found.") from e

    def find_assignment(self, id: str) -> Assignment:
        """Finds an Assignment in assignment_list based on ID.

        Args:
            id: The UUID of the Assignment to find.

        Returns:
            Assignment: The Assignment object matching the given UUID. Throws error if not found.
        """
        if id in self._assignment_list:
            return self._assignment_list[id]
        else:
            raise KeyError("Assignment not found.")

    def from_row(
            self,
            id: str,
            title: str,
            description: str,
            start_date: date,
            end_date: date,
            num_credits: int,
            active: bool) -> Self:
        """Constructs a Course from a persisted record, using the existing ID instead
        of generating a new one.

        Args:
            id: The ID of the Course to construct.
            title: The title of the Course.
            description: A description of the Course.
            start_date: The start date of the Course.
            end_date: The end date of the Course.
            num_credits: The number of credits of the Course.
            active: Whether the Course is currently active.
        
        Returns:
            Course object with the specified attributes and copied ID.
        """
        c = Course(title, description, start_date, end_date, num_credits, active)
        c.id = id
        return c