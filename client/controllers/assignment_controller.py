# Standard library imports
from __future__ import annotations

from datetime import datetime

# Local imports
from models.assignment import Assignment
from models.course import Course


class AssignmentController:
    """Controller for managing Assignment operations."""
    
    def __init__(self, course: Course) -> None:
        self._course: Course = course
        # Maps title (lowercase) -> id; only used internally
        self._title_to_id: dict[str, str] = {}
        
        # Initialize controller indexes from existing Assignments in the term
        self._initialize_indexes_from_term()
        
    def _initialize_indexes_from_term(self) -> None:
        """Initialize controller indexes from existing Assignments in the term.
        
        This ensures that when a CourseController is created for a term that
        already has Assignments, the controller's indexes are populated correctly.
        """
        for assignment_id, assignment in self._course.assignment_list.items():
            self._title_to_id[assignment.title.lower()] = assignment_id
            self._assignment_order.append(assignment_id)
        
    def get_assignment_list(self) -> dict[str, Assignment]:
        """Get the Assignment list of the current Course.
        
        Returns:
            dict[str, Assignment]: A dictionary mapping Assignment IDs to 
                Assignment objects.
        """
        return self._course.assignment_list
    
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
        # Set Course grade_percentage to None and trigger percentage recalculation
        self._course.grade_percentage = None
        
    def edit_title(self, assignment_id: str, new_title: str) -> None:
        """Edit the title of an Assignment.
        
        Args:
            assignment_id: The ID of the Assignment to edit.
            new_title: The new title of the Assignment.
            
        Raises:
            KeyError: If an Assignment with the given ID is not found.
            ValueError: If an Assignment with the same title already exists.
        """
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        old_title_lower = assignment.title.lower()
        
        if new_title.lower() in self._title_to_id:
            raise ValueError(f"Assignment with title {new_title} already exists.")

        assignment.title = new_title
        del self._title_to_id[old_title_lower]
        self._title_to_id[new_title.lower()] = assignment_id
        
    def edit_description(self, assignment_id: str, new_description: str) -> None:
        """Edit the description of an Assignment.
        
        Args:
            assignment_id: The ID of the Assignment to edit.
            new_description: The new description of the Assignment.
            
        Raises:
            KeyError: If an Assignment with the given ID is not found.
        """
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        # Checks that description is not empty, whitespace, or unchanged
        assignment.description = new_description if new_description \
            and not new_description.isspace() \
            and new_description != assignment.description \
            else assignment.description
            
    def edit_category(self, assignment_id: str, new_category: str) -> None:
        """Edit the category of an Assignment.
        
        Args:
            assignment_id: The ID of the Assignment to edit.
            new_category: The new category of the Assignment.
            
        Raises:
            KeyError: If an Assignment with the given ID is not found.
            ValueError: If the new category is empty, whitespace, or not found in grade weights.
        """
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        
        # Filters out empty or whitespace categories
        if not new_category or new_category.isspace():
            raise ValueError("Category cannot be empty or whitespace.")
        
        # Ensures that category is valid and listed in grade weights for alignment
        if new_category not in self._course.grade_weights:
            raise ValueError(f"Category '{new_category}' not found in grade weights.")
        
        assignment.category = new_category
        # Set Course grade_percentage to None and trigger percentage recalculation
        self._course.grade_percentage = None

    def edit_due_date(self, assignment_id: str, new_due_date: datetime) -> None:
        """Edit the due date of an Assignment.
        
        Args:
            assignment_id: The ID of the Assignment to edit.
            new_due_date: The new due date of the Assignment.
            
        Raises:
            KeyError: If an Assignment with the given ID is not found.
        """
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        assignment.due_date = new_due_date

    def add_grade(self,
            title: str,
            *,
            grade: float | None = None,
            points_earned: float | None = None,
            total_points: float | None = None) -> None:
        """Adds a grade to a selected assignment and sets it as complete.
        
        Args:
            title: The title of the assignment to add a grade to.
            * grade: The grade to add to the assignment.
            * points_earned: The number of points earned for the assignment.
            * total_points: The total number of points for the assignment.
            
        Raises:
            KeyError: If an Assignment with the given title is not found.
            ValueError: If the grade is not a valid float or is outside the range [0, 100].
        """
        assignment_id = self.get_assignment_id(title)
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        
        # Branch for percentage-based grading
        if points_earned is not None and total_points is not None:
            if total_points == 0:
                raise ValueError("Division by zero not allowed.")
            grade = (points_earned / total_points) * 100.0
        elif grade is None:
            raise ValueError("Either grade or (points_earned, total_points) must be provided")
        
        grade = round(grade, 2)
        assignment.grade = grade
        assignment.completed = True
        # Set Course grade_percentage to None and trigger percentage recalculation
        self._course.grade_percentage = None
        
    def remove_grade(self, title: str) -> None:
        """Removes the grade from an Assignment and sets it as incomplete.
        
        Args:
            title: The title of the Assignment to remove the grade from.
            
        Raises:
            KeyError: If an Assignment with the given title is not found.
        """
        assignment_id = self.get_assignment_id(title)
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        assignment = self._course.find_assignment(assignment_id)
        assignment.grade = 0.0
        assignment.completed = False
        # Set Course grade_percentage to None and trigger percentage recalculation
        self._course.grade_percentage = None
        
    def remove_assignment(self, title: str) -> None:
        """Removes an Assignment from the Course.
        
        Args:
            title: The title of the Assignment to remove.
            
        Raises:
            KeyError: If an Assignment with the given title is not found.
        """
        assignment_id = self.get_assignment_id(title)
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        self._course.remove_assignment(assignment_id)
        del self._title_to_id[title.lower()]
        # Set Course grade_percentage to None and trigger percentage recalculation
        self._course.grade_percentage = None
        
    def find_assignment(self, title: str) -> Assignment:
        """Finds an Assignment by its title.
        
        Args:
            title: The title of the Assignment to find.
            
        Returns:
            The Assignment with the given title.
            
        Raises:
            KeyError: If an Assignment with the given title is not found.
        """
        assignment_id = self.get_assignment_id(title)
        if assignment_id not in self._course.assignment_list:
            raise KeyError(f"Assignment with ID '{assignment_id}' not found.")
        return self._course.find_assignment(assignment_id)