# Standard library imports
import math
import re
from datetime import datetime
from io import StringIO

import pytest

# Local imports
from models.assignment import Assignment
from models.course import Course
from models.term import Term


# Helper function to mask UUIDs in output
def mask_uuids(output: str) -> str:
    """Replace UUIDs in output string with <UUID> placeholder.
    
    Args:
        output: The output string to mask.
        
    Returns:
        str: The output string with UUIDs replaced by <UUID>.
    """
    uuid_pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    return re.sub(uuid_pattern, "<UUID>", output)


class TestCourse:
    """Test suite for Course model."""

    @pytest.fixture
    def course1(self) -> Course:
        """Create a sample Course for testing."""
        return Course(
            "CMPE 142",
            "Operating Systems",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3,
            False
        )

    @pytest.fixture
    def assignment1(self) -> Assignment:
        """Create a sample Assignment for testing."""
        return Assignment(
            "Homework 3",
            "Focus on variables and strings.",
            "Homework",
            datetime(2025, 11, 20),
            True,
            95.18
        )

    @pytest.fixture
    def assignment2(self) -> Assignment:
        """Create a second sample Assignment for testing."""
        return Assignment(
            "Homework 1",
            "",
            "Homework",
            datetime(2025, 10, 31),
            False,
            90.50
        )

    @pytest.mark.course_smoke
    def test_id_getter(self, course1):
        """Ensure ID is not empty."""
        assert course1.id and not course1.id.isspace()

    @pytest.mark.course_smoke
    def test_title_getter(self, course1):
        """Test title getter returns correct value."""
        assert course1.title == "CMPE 142"

    @pytest.mark.course_smoke
    def test_description_getter(self, course1):
        """Test description getter returns correct value."""
        assert course1.description == "Operating Systems"

    @pytest.mark.course_smoke
    def test_start_date_getter(self, course1):
        """Test start date getter returns correct value."""
        assert course1.start_date == datetime(2025, 8, 12)

    @pytest.mark.course_smoke
    def test_end_date_getter(self, course1):
        """Test end date getter returns correct value."""
        assert course1.end_date == datetime(2025, 12, 5)

    @pytest.mark.course_smoke
    def test_assignment_list_getter(self, course1, assignment1, assignment2):
        """Test assignment list getter returns correct assignments."""
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        id1 = assignment1.id
        id2 = assignment2.id

        assert course1.find_assignment(id1).title == "Homework 3"
        assert course1.find_assignment(id2).due_date == datetime(2025, 10, 31)

    @pytest.mark.course_smoke
    def test_assignment_list_getter_check_size(self, course1, assignment1, assignment2):
        """Test assignment list getter returns correct size."""
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        assert len(course1._assignment_list) == 2

    @pytest.mark.course_smoke
    def test_grade_weights_getter(self, course1):
        """Test grade weights getter returns correct weights."""
        weights = course1.grade_weights

        assert "Homework" in weights
        assert "Final Exam" in weights

    @pytest.mark.course_smoke
    def test_num_credits_getter(self, course1):
        """Test num credits getter returns correct value."""
        assert course1.num_credits == 3

    @pytest.mark.course_smoke
    def test_grade_pct_getter(self, course1):
        """Test grade percentage getter returns correct value."""
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_letter_grade_getter(self, course1):
        """Test letter grade getter returns correct value."""
        course1.grade_percentage = 86.0
        assert course1.letter_grade == "B"

    @pytest.mark.course_smoke
    def test_gpa_val_getter(self, course1):
        """Test GPA value getter returns correct value."""
        course1.grade_percentage = 88.3
        assert math.isclose(course1.gpa_value, 3.3, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_active_getter(self, course1):
        """Test active getter returns correct value."""
        assert course1.active is False

    @pytest.mark.course_smoke
    def test_grade_scale_getter(self, course1):
        """Test grade scale getter returns correct scale."""
        grade_scale2 = {
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

        assert course1.grade_scale == grade_scale2

    @pytest.mark.course_smoke
    def test_title_setter(self, course1):
        """Test title setter updates the title."""
        course1.title = "HSPM 149"
        assert course1.title == "HSPM 149"

    @pytest.mark.course_smoke
    def test_description_setter(self, course1):
        """Test description setter updates the description."""
        course1.description = "Beer Appreciation"
        assert course1.description == "Beer Appreciation"

    @pytest.mark.course_smoke
    def test_start_date_setter(self, course1):
        """Test start date setter updates the start date."""
        course1.start_date = datetime(2025, 9, 25)
        assert course1.start_date == datetime(2025, 9, 25)

    @pytest.mark.course_smoke
    def test_end_date_setter(self, course1):
        """Test end date setter updates the end date."""
        course1.end_date = datetime(2025, 11, 7)
        assert course1.end_date == datetime(2025, 11, 7)

    @pytest.mark.course_smoke
    def test_num_credits_setter(self, course1):
        """Test num credits setter updates the num credits."""
        course1.num_credits = 2
        assert course1.num_credits == 2

    @pytest.mark.course_smoke
    def test_grade_weights_setter(self, course1):
        """Test grade weights setter updates the weights."""
        grade_weights2 = {
            "Homework": 0.2,
            "Midterm": 0.4,
            "Final Exam": 0.4
        }

        course1.grade_weights = grade_weights2
        weights = course1.grade_weights
        assert math.isclose(weights["Homework"], 0.2, abs_tol=1e-9)
        assert math.isclose(weights["Midterm"], 0.4, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_grade_pct_setter_automatic(self, course1):
        """Test grade percentage setter calculates automatically when no value provided."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 18), True, 89.17)
        course1.add_assignment(assignment1)
        course1.grade_percentage = None
        assert math.isclose(course1.grade_percentage, 89.17, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_grade_pct_setter_manual(self, course1):
        """Test grade percentage setter sets value when provided."""
        course1.grade_percentage = 89.17
        assert math.isclose(course1.grade_percentage, 89.17, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_letter_grade_setter(self, course1):
        """Test letter grade property calculates correctly."""
        course1.grade_percentage = 90.18
        assert course1.letter_grade == "A-"

    @pytest.mark.course_smoke
    def test_gpa_val_setter(self, course1):
        """Test GPA value property calculates correctly."""
        course1.grade_percentage = 75.28
        assert math.isclose(course1.gpa_value, 2.0, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_active_setter(self, course1):
        """Test active setter updates the active status."""
        course1.active = True
        assert course1.active is True

    @pytest.mark.course_smoke
    def test_grade_scale_setter(self, course1):
        """Test grade scale setter updates the scale."""
        grade_scale2 = {
            70.0: "P",
            0.0: "NP"
        }

        course1.grade_scale = grade_scale2
        assert course1.grade_scale == grade_scale2

    @pytest.mark.course_smoke
    def test_print_course_info(self, course1):
        """Test print_course_info outputs correct format."""
        ss = StringIO()

        course1.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\nDescription: Operating Systems\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 0.00%\nLetter Grade: N/A\n" \
                   "GPA Value: 0.0\nTotal Assignments: 0\nIncomplete Assignments: 0\nCurrent? No\n"
        assert output == expected

    @pytest.mark.course_smoke
    def test_add_assignment(self, course1, assignment1):
        """Test adding an assignment to course."""
        course1.add_assignment(assignment1)
        assert len(course1._assignment_list) == 1

        assert math.isclose(course1.grade_percentage, 95.18, abs_tol=1e-9)
        assert course1.letter_grade == "A"
        assert math.isclose(course1.gpa_value, 4.0, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_remove_assignment(self, course1, assignment1, assignment2):
        """Test removing an assignment from course."""
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        id = assignment1.id
        course1.remove_assignment(id)

        assert len(course1._assignment_list) == 1
        assert id not in course1._assignment_list

        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)
        assert course1.letter_grade == "N/A"
        assert math.isclose(course1.gpa_value, 0.0, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_remove_assignment_remaining_completed(self, course1, assignment1, assignment2):
        """Test removing an assignment when one completed assignment remains."""
        assignment3 = Assignment("Homework 2", "", "Homework", datetime(2025, 10, 31), True, 85.5)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment3)
        course1.add_assignment(assignment2)
        
        # Verify initial state with two completed assignments
        assert math.isclose(course1.grade_percentage, 90.34, abs_tol=1e-9)
        assert course1.letter_grade == "A-"
        assert math.isclose(course1.gpa_value, 3.7, abs_tol=1e-9)
        
        # Remove one completed assignment
        id = assignment1.id
        course1.remove_assignment(id)
        
        # Verify grade recalculates based on remaining completed assignment
        assert len(course1._assignment_list) == 2
        assert id not in course1._assignment_list
        assert math.isclose(course1.grade_percentage, 85.5, abs_tol=1e-9)
        assert course1.letter_grade == "B"
        assert math.isclose(course1.gpa_value, 3.0, abs_tol=1e-9)

    @pytest.mark.course_smoke
    def test_find_assignment(self, course1, assignment1, assignment2):
        """Test finding an assignment by ID."""
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        id = assignment1.id

        assert course1.find_assignment(id) == assignment1

    @pytest.mark.course_smoke
    def test_find_assignment_modifiable(self, course1, assignment1, assignment2):
        """Test that found assignment can be modified."""
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        id = assignment1.id
        course1.find_assignment(id).completed = False
        assignment1.completed = False

        assert course1.find_assignment(id) == assignment1

    @pytest.mark.course_smoke
    def test_overloaded_equals(self, course1):
        """Test Course equality operator."""
        course2 = Course("ENGR 195A", "", datetime(2025, 8, 14), datetime(2025, 12, 18), 3, True)
        course3 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, False)
        course4 = course1

        assert course1 != course2
        assert course1 != course3
        assert course1 == course4

    @pytest.mark.course_smoke
    def test_from_row_all_fields(self):
        """Test Course.from_row class method with all fields."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        course = Course.from_row(
            test_id, "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, False
        )

        assert course.id == test_id
        assert course.title == "CMPE 142"
        assert course.description == "Operating Systems"
        assert course.start_date == datetime(2025, 8, 12)
        assert course.end_date == datetime(2025, 12, 5)
        assert course.num_credits == 3
        assert course.active is False

    @pytest.mark.course_smoke
    def test_from_row_preserves_id(self):
        """Test that from_row preserves the provided ID (key invariant)."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        course = Course.from_row(
            test_id, "CMPE 142", "",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, False
        )

        assert course.id == test_id

    @pytest.mark.course_smoke
    def test_from_row_active_true(self):
        """Test Course.from_row with active=True."""
        course = Course.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "CMPE 142", "",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, True
        )

        assert course.active is True

    @pytest.mark.course_smoke
    def test_from_row_empty_description(self):
        """Test Course.from_row with empty description."""
        course = Course.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "CMPE 142", "",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, False
        )

        assert course.description == ""

    @pytest.mark.course_smoke
    def test_from_row_does_not_equal_new_course(self):
        """Test that from_row Course and new Course with same params are not equal."""
        from_row_course = Course.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, False
        )
        new_course = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            3, False
        )

        assert from_row_course != new_course

    @pytest.mark.course_edge
    def test_description_getter_empty(self):
        """Test description getter with empty description."""
        course2 = Course("ENGR 195A", "", datetime(2025, 8, 14), datetime(2025, 12, 18), 3, True)
        assert course2.description == ""

    @pytest.mark.course_edge
    def test_num_credits_getter_empty(self):
        """Test num credits getter with default value."""
        course2 = Course("ENGR 195A", "", datetime(2025, 8, 14), datetime(2025, 12, 18), 3, True)
        assert course2.num_credits == 3

    @pytest.mark.course_edge
    def test_active_getter_empty(self):
        """Test active getter with default value."""
        course2 = Course("ENGR 195A", "", datetime(2025, 8, 14), datetime(2025, 12, 18), 3, True)
        assert course2.active is True

    @pytest.mark.course_edge
    def test_title_setter_invalid(self, course1):
        """Test title setter with empty string raises ValueError."""
        with pytest.raises(ValueError):
            course1.title = ""
        assert course1.title == "CMPE 142"

    @pytest.mark.course_edge
    def test_title_setter_whitespace_invalid(self, course1):
        """Test title setter with whitespace raises ValueError."""
        with pytest.raises(ValueError):
            course1.title = " "
        assert course1.title == "CMPE 142"

    @pytest.mark.course_edge
    def test_description_setter_empty(self, course1):
        """Test description setter with empty string."""
        course1.description = ""
        assert course1.description == ""

    @pytest.mark.course_edge
    def test_description_setter_whitespace(self, course1):
        """Test description setter with whitespace."""
        course1.description = "  "
        assert course1.description == ""

    @pytest.mark.course_edge
    def test_grade_weights_setter_invalid(self, course1):
        """Test grade weights setter with invalid total raises ValueError."""
        grade_weights2 = {
            "Homework": 0.4,
            "Midterm": 0.4,
            "Final Exam": 0.4
        }

        with pytest.raises(ValueError):
            course1.grade_weights = grade_weights2
        weights = course1.grade_weights
        assert math.isclose(weights["Homework"], 0.25, abs_tol=1e-9)
        assert math.isclose(weights["Midterm"], 0.35, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_num_credits_setter_invalid(self, course1):
        """Test num credits setter with negative value raises ValueError."""
        with pytest.raises(ValueError):
            course1.num_credits = -3
        assert course1.num_credits == 3

    @pytest.mark.course_edge
    def test_num_credits_setter_zero(self, course1):
        """Test num credits setter with zero value."""
        course1.num_credits = 0
        assert course1.num_credits == 0

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_no_complete_assignments(self, course1):
        """Test grade percentage automatic calculation with no complete assignments."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), False, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 1, 31), False, 0.0)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_different_categories(self, course1):
        """Test grade percentage automatic calculation with different categories."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Midterm", "", "Midterm", datetime(2026, 2, 28), True, 88.74)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        assert math.isclose(course1.grade_percentage, 89.35, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_all_categories(self, course1):
        """Test grade percentage automatic calculation with all categories."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Midterm", "", "Midterm", datetime(2026, 2, 28), True, 88.74)
        assignment3 = Assignment("Final Exam", "", "Final Exam", datetime(2026, 4, 17), True, 76.11)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        course1.add_assignment(assignment3)
        assert math.isclose(course1.grade_percentage, 84.05, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_multiple_assignments_same_category(self, course1):
        """Test grade percentage automatic calculation with multiple assignments same category."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 2, 28), True, 88.74)
        assignment3 = Assignment("Homework 3", "", "Homework", datetime(2026, 4, 17), True, 76.11)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        course1.add_assignment(assignment3)
        assert math.isclose(course1.grade_percentage, 85.02, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_uneven_category_split(self, course1):
        """Test grade percentage automatic calculation with uneven category split."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 2, 28), True, 88.74)
        assignment3 = Assignment("Final Exam", "", "Final Exam", datetime(2026, 4, 17), True, 76.11)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        course1.add_assignment(assignment3)
        assert math.isclose(course1.grade_percentage, 81.25, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_automatic_categories_nonexistent(self, course1):
        """Test grade percentage automatic calculation with nonexistent categories."""
        assignment1 = Assignment("Quiz 1", "", "Quizzes", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Quiz 2", "", "Quizzes", datetime(2026, 2, 28), True, 88.74)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_manual_invalid_low(self, course1):
        """Test grade percentage setter with invalid low value raises ValueError."""
        with pytest.raises(ValueError):
            course1.grade_percentage = -20.24
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_manual_invalid_high(self, course1):
        """Test grade percentage setter with invalid high value raises ValueError."""
        with pytest.raises(ValueError):
            course1.grade_percentage = 200.24
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_manual_boundary_low(self, course1):
        """Test grade percentage setter with boundary low value."""
        course1.grade_percentage = 0.0
        assert math.isclose(course1.grade_percentage, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_pct_setter_manual_boundary_high(self, course1):
        """Test grade percentage setter with boundary high value."""
        course1.grade_percentage = 150.0
        assert math.isclose(course1.grade_percentage, 150.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_letter_grade_setter_range_high(self, course1):
        """Test letter grade property with high range value."""
        course1.grade_percentage = 92.99
        assert course1.letter_grade == "A-"

    @pytest.mark.course_edge
    def test_letter_grade_setter_low_f(self, course1):
        """Test letter grade property with low F grade."""
        course1.grade_percentage = 35.0
        assert course1.letter_grade == "F"

    @pytest.mark.course_edge
    def test_letter_grade_setter_boundary_high(self, course1):
        """Test letter grade property with boundary high value."""
        course1.grade_percentage = 150.0
        assert course1.letter_grade == "A+"

    @pytest.mark.course_edge
    def test_letter_grade_setter_boundary_low(self, course1):
        """Test letter grade property with boundary low value."""
        course1.grade_percentage = 0.0
        assert course1.letter_grade == "N/A"

    @pytest.mark.course_edge
    def test_letter_grade_setter_no_complete_assignments(self, course1):
        """Test letter grade property with no complete assignments."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), False, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 1, 31), False, 0.0)
        course1.add_assignment(assignment1)
        course1.add_assignment(assignment2)
        assert course1.letter_grade == "N/A"

    @pytest.mark.course_edge
    def test_letter_grade_setter_completed_zero_grade(self, course1):
        """Test letter grade property with completed zero grade."""
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 0.0)
        course1.add_assignment(assignment1)
        assert course1.letter_grade == "F"

    @pytest.mark.course_edge
    def test_gpa_val_setter_no_grade(self, course1):
        """Test GPA value property calculates from grade percentage."""
        course1.grade_percentage = 88.4
        assert math.isclose(course1.gpa_value, 3.3, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_gpa_val_setter_low_f(self, course1):
        """Test GPA value property with low F grade."""
        course1.grade_percentage = 15.5
        assert math.isclose(course1.gpa_value, 0.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_gpa_val_setter_over_hundred(self, course1):
        """Test GPA value property with grade over 100."""
        course1.grade_percentage = 147.1
        assert math.isclose(course1.gpa_value, 4.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_grade_scale_setter_empty(self, course1):
        """Test grade scale setter with empty scale raises ValueError."""
        grade_scale2 = {}

        with pytest.raises(ValueError):
            course1.grade_scale = grade_scale2

    @pytest.mark.course_edge
    def test_grade_scale_setter_missing_zero(self, course1):
        """Test grade scale setter missing zero raises ValueError."""
        grade_scale2 = {
            80.0: "A",
            60.0: "C"
        }

        with pytest.raises(ValueError):
            course1.grade_scale = grade_scale2

    @pytest.mark.course_edge
    def test_grade_scale_setter_invalid_high(self, course1):
        """Test grade scale setter with invalid high value raises ValueError."""
        grade_scale2 = {
            110.0: "A++",
            60.0: "C",
            0.0: "F"
        }

        with pytest.raises(ValueError):
            course1.grade_scale = grade_scale2

    @pytest.mark.course_edge
    def test_grade_scale_setter_upper_bound(self, course1):
        """Test grade scale setter with upper bound value raises ValueError."""
        grade_scale2 = {
            100.0: "A++",
            90.0: "A-",
            0.0: "F"
        }

        with pytest.raises(ValueError):
            course1.grade_scale = grade_scale2

    @pytest.mark.course_edge
    def test_print_course_info_partial(self):
        """Test print_course_info with partial information."""
        ss = StringIO()
        course2 = Course("CMPE 142", "", datetime(2025, 8, 12), datetime(2025, 12, 5), 3, True)
        course2.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 0.00%\nLetter Grade: N/A\n" \
                   "GPA Value: 0.0\nTotal Assignments: 0\nIncomplete Assignments: 0\nCurrent? Yes\n"
        assert output == expected

    @pytest.mark.course_edge
    def test_print_course_info_desc_partial(self):
        """Test print_course_info with description."""
        ss = StringIO()
        course2 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, True)
        course2.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\nDescription: Operating Systems\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 0.00%\nLetter Grade: N/A\n" \
                   "GPA Value: 0.0\nTotal Assignments: 0\nIncomplete Assignments: 0\nCurrent? Yes\n"
        assert output == expected

    @pytest.mark.course_edge
    def test_print_course_info_completed_assignments(self):
        """Test print_course_info with completed assignments."""
        ss = StringIO()
        course2 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, True)
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 2, 5), True, 87.18)
        assignment3 = Assignment("Homework 3", "", "Homework", datetime(2026, 2, 23), True, 100.0)
        course2.add_assignment(assignment1)
        course2.add_assignment(assignment2)
        course2.add_assignment(assignment3)
        course2.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\nDescription: Operating Systems\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 92.46%\nLetter Grade: A-\n" \
                   "GPA Value: 3.7\nTotal Assignments: 3\nIncomplete Assignments: 0\nCurrent? Yes\n"
        assert output == expected

    @pytest.mark.course_edge
    def test_print_course_info_mixed_assignments(self):
        """Test print_course_info with mixed completed/incomplete assignments."""
        ss = StringIO()
        course2 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, True)
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), True, 90.2)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 2, 5), True, 87.18)
        assignment3 = Assignment("Homework 3", "", "Homework", datetime(2026, 2, 23), False, 0.0)
        course2.add_assignment(assignment1)
        course2.add_assignment(assignment2)
        course2.add_assignment(assignment3)
        course2.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\nDescription: Operating Systems\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 88.69%\nLetter Grade: B+\n" \
                   "GPA Value: 3.3\nTotal Assignments: 3\nIncomplete Assignments: 1\nCurrent? Yes\n"
        assert output == expected

    @pytest.mark.course_edge
    def test_print_course_info_incomplete_assignments(self):
        """Test print_course_info with all incomplete assignments."""
        ss = StringIO()
        course2 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, True)
        assignment1 = Assignment("Homework 1", "", "Homework", datetime(2026, 1, 20), False, 0.0)
        assignment2 = Assignment("Homework 2", "", "Homework", datetime(2026, 2, 5), False, 0.0)
        assignment3 = Assignment("Homework 3", "", "Homework", datetime(2026, 2, 23), False, 0.0)
        course2.add_assignment(assignment1)
        course2.add_assignment(assignment2)
        course2.add_assignment(assignment3)
        course2.print_course_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = "ID: <UUID>\nCourse: CMPE 142\nDescription: Operating Systems\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\nNumber of Credits: 3\n" \
                   "Grade Percentage: 0.00%\nLetter Grade: N/A\n" \
                   "GPA Value: 0.0\nTotal Assignments: 3\nIncomplete Assignments: 3\nCurrent? Yes\n"
        assert output == expected

    @pytest.mark.course_edge
    def test_add_assignment_already_exists(self, course1, assignment1):
        """Test adding duplicate assignment raises ValueError."""
        course1.add_assignment(assignment1)

        with pytest.raises(ValueError, match="already exists"):
            course1.add_assignment(assignment1)

        assert math.isclose(course1.grade_percentage, 95.18, abs_tol=1e-9)
        assert course1.letter_grade == "A"
        assert math.isclose(course1.gpa_value, 4.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_remove_assignment_not_found(self, course1, assignment1, assignment2):
        """Test removing non-existent assignment raises KeyError."""
        course1.add_assignment(assignment1)
        id = assignment2.id

        with pytest.raises(KeyError, match="Assignment not found"):
            course1.remove_assignment(id)

        assert math.isclose(course1.grade_percentage, 95.18, abs_tol=1e-9)
        assert course1.letter_grade == "A"
        assert math.isclose(course1.gpa_value, 4.0, abs_tol=1e-9)

    @pytest.mark.course_edge
    def test_find_assignment_not_found(self, course1, assignment1, assignment2):
        """Test finding non-existent assignment raises KeyError."""
        course1.add_assignment(assignment1)
        id = assignment2.id

        with pytest.raises(KeyError, match="Assignment not found"):
            course1.find_assignment(id)

    @pytest.mark.course_edge
    def test_overloaded_equals_same_title_different_params(self, course1):
        """Test equality with same title but different parameters."""
        course2 = Course("CMPE 142", "Global and Social Issues in Engineering", 
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False)
        course3 = Course("CMPE 142", "Operating Systems", datetime(2025, 9, 2), 
            datetime(2025, 12, 5), 3, False)
        course4 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2026, 12, 5), 3, False)
        course5 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 1, False)
        course6 = Course("CMPE 142", "Operating Systems", datetime(2025, 8, 12), 
            datetime(2025, 12, 5), 3, True)

        assert course1 != course2
        assert course1 != course3
        assert course1 != course4
        assert course1 != course5
        assert course1 != course6

    @pytest.mark.course_edge
    def test_overloaded_equals_same_params_different_id(self):
        """Test equality with same parameters but different IDs."""
        course2 = Course("CMPE 142", "Global and Social Issues in Engineering", 
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False)
        course3 = Course("CMPE 142", "Global and Social Issues in Engineering", 
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False)

        assert course2 != course3

    @pytest.mark.course_edge
    def test_from_row_empty_title(self):
        """Test from_row with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Course.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "",
                "",
                datetime(2025, 8, 12),
                datetime(2025, 12, 5),
                3, False
            )

    @pytest.mark.course_edge
    def test_from_row_whitespace_title(self):
        """Test from_row with whitespace title raises ValueError."""
        with pytest.raises(ValueError):
            Course.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "   ",
                "",
                datetime(2025, 8, 12),
                datetime(2025, 12, 5),
                3, False
            )

    @pytest.mark.course_edge
    def test_from_row_invalid_num_credits(self):
        """Test from_row with invalid num credits raises ValueError."""
        with pytest.raises(ValueError):
            Course.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "CMPE 142",
                "",
                datetime(2025, 8, 12),
                datetime(2025, 12, 5),
                -1, False
            )

    @pytest.mark.course_edge
    def test_from_row_zero_credits_valid(self):
        """Test from_row with zero credits is valid."""
        course = Course.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "CMPE 142",
            "",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            0, False
        )

        assert course.num_credits == 0

    @pytest.mark.course_edge
    def test_from_row_same_day_start_and_end(self):
        """Test from_row with same start and end date."""
        course = Course.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "CMPE 142",
            "",
            datetime(2025, 8, 12),
            datetime(2025, 8, 12),
            3, False
        )

        assert course.start_date == course.end_date


class TestTerm:
    """Test suite for Term model."""

    @pytest.fixture
    def term1(self) -> Term:
        """Create a sample Term for testing."""
        return Term(
            title="Fall 2025",
            start_date=datetime(2025, 8, 12),
            end_date=datetime(2025, 12, 5),
            active=False
        )

    @pytest.mark.term_smoke
    def test_initialization_basic(self):
        """Test Term initialization with basic parameters."""
        term2 = Term(
            "Spring 2025",
            datetime(2025, 1, 18),
            datetime(2025, 5, 28),
            False
        )
        assert term2.id and not term2.id.isspace()
        assert term2.title == "Spring 2025"
        assert term2.start_date == datetime(2025, 1, 18)
        assert term2.end_date == datetime(2025, 5, 28)
        assert term2.active is False

    @pytest.mark.term_smoke
    def test_initialization_with_active_true(self):
        """Test Term initialization with active=True."""
        term2 = Term(
            "Spring 2025",
            datetime(2025, 1, 18),
            datetime(2025, 5, 28),
            True
        )
        assert term2.active is True

    @pytest.mark.term_edge
    def test_initialization_empty_title(self):
        """Test initialization with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Term(
                "",
                datetime(2025, 1, 18),
                datetime(2025, 5, 28),
                False
            )

    @pytest.mark.term_edge
    def test_initialization_invalid_date_order(self):
        """Test initialization with end date before start date raises ValueError."""
        with pytest.raises(ValueError):
            Term(
                "Spring 2026",
                datetime(2026, 5, 28),  # End date before start date
                datetime(2026, 1, 18),
                False
            )

    @pytest.mark.term_smoke
    def test_id_getter(self, term1):
        """Ensure ID is not empty."""
        assert term1.id and not term1.id.isspace()

    @pytest.mark.term_smoke
    def test_title_getter(self, term1):
        """Test title getter returns correct value."""
        assert term1.title == "Fall 2025"

    @pytest.mark.term_smoke
    def test_start_date_getter(self, term1):
        """Test start date getter returns correct value."""
        assert term1.start_date == datetime(2025, 8, 12)

    @pytest.mark.term_smoke
    def test_end_date_getter(self, term1):
        """Test end date getter returns correct value."""
        assert term1.end_date == datetime(2025, 12, 5)

    @pytest.mark.term_smoke
    def test_active_getter(self, term1):
        """Test active getter returns correct value."""
        assert term1.active is False

    @pytest.mark.term_smoke
    def test_total_credits_getter(self, term1):
        """Test total credits calculation."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        term1.add_course(course1)
        term1.add_course(course2)
        
        assert term1.total_credits == 4

    @pytest.mark.term_smoke
    def test_ovr_gpa_getter(self, term1):
        """Test overall GPA calculation."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        
        course1.grade_percentage = 89.5
        course2.grade_percentage = 72.8
        term1.add_course(course1)
        term1.add_course(course2)
        
        # Calculate expected GPA: (3.3 * 3 + 1.7 * 1) / 4 = 2.9
        # Using the grade scale: 89.5 -> B+ (3.3), 72.8 -> C- (1.7)
        assert term1.ovr_gpa == 2.9

    @pytest.mark.term_edge
    def test_ovr_gpa_getter_no_courses(self, term1):
        """Test overall GPA when no courses are added."""
        assert term1.ovr_gpa == 0.0

    @pytest.mark.term_edge
    def test_ovr_gpa_getter_zero_credits(self, term1):
        """Test overall GPA when courses have zero credits."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 0, False
        )
        term1.add_course(course1)
        
        assert term1.ovr_gpa == 0.0

    @pytest.mark.term_smoke
    def test_title_setter(self, term1):
        """Test title setter updates the title."""
        term1.title = "Spring 2026"
        assert term1.title == "Spring 2026"

    @pytest.mark.term_smoke
    def test_start_date_setter(self, term1):
        """Test start date setter updates the start date."""
        term1.start_date = datetime(2026, 1, 20)
        assert term1.start_date == datetime(2026, 1, 20)

    @pytest.mark.term_smoke
    def test_end_date_setter(self, term1):
        """Test end date setter updates the end date."""
        term1.end_date = datetime(2026, 5, 23)
        assert term1.end_date == datetime(2026, 5, 23)

    @pytest.mark.term_smoke
    def test_active_setter(self, term1):
        """Test active setter updates the active status."""
        term1.active = True
        assert term1.active is True

    @pytest.mark.term_edge
    def test_title_setter_empty(self, term1):
        """Test title setter with empty string raises ValueError."""
        with pytest.raises(ValueError):
            term1.title = ""
        assert term1.title == "Fall 2025"

    @pytest.mark.term_edge
    def test_title_setter_whitespace(self, term1):
        """Test title setter with whitespace raises ValueError."""
        with pytest.raises(ValueError):
            term1.title = " "
        assert term1.title == "Fall 2025"

    @pytest.mark.term_smoke
    def test_add_course(self, term1):
        """Test adding a course to term."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        
        term1.add_course(course1)
        assert len(term1._course_list) == 1

    @pytest.mark.term_smoke
    def test_remove_course(self, term1):
        """Test removing a course from term."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        
        term1.add_course(course1)
        term1.add_course(course2)
        course_id = course1.id
        term1.remove_course(course_id)
        
        # Check size and success of removal
        assert len(term1._course_list) == 1
        assert course_id not in term1._course_list

    @pytest.mark.term_smoke
    def test_find_course(self, term1):
        """Test finding a course by ID."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        
        term1.add_course(course1)
        term1.add_course(course2)
        
        assert term1.find_course(course1.id) == course1

    @pytest.mark.term_smoke
    def test_find_course_modifiable(self, term1):
        """Test that found course can be modified."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        
        term1.add_course(course1)
        term1.add_course(course2)
        
        # Modify the found course
        found_course = term1.find_course(course1.id)
        found_course.active = True
        
        # Verify the modification
        assert term1.find_course(course1.id).active is True

    @pytest.mark.term_smoke
    def test_print_term_info(self, term1):
        """Test print_term_info outputs correct format."""
        ss = StringIO()
        
        # Initialize courses for total_credits and ovr_gpa
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        term1.add_course(course1)
        term1.add_course(course2)
        
        term1.print_term_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)
        
        expected = "ID: <UUID>\nTerm: Fall 2025\n" \
                   "Duration: 2025-08-12 00:00:00 - 2025-12-05 00:00:00\n" \
                   "Total Credits: 4\nOverall GPA: 0.00\n" \
                   "Current? No\n"
        assert output == expected

    @pytest.mark.term_edge
    def test_add_course_already_exists(self, term1):
        """Test adding duplicate course raises ValueError."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        
        term1.add_course(course1)
        
        with pytest.raises(ValueError, match="already exists"):
            term1.add_course(course1)

    @pytest.mark.term_edge
    def test_remove_course_not_found(self, term1):
        """Test removing non-existent course raises KeyError."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        course_id = course2.id
        
        term1.add_course(course1)
        
        with pytest.raises(KeyError, match="Course not found"):
            term1.remove_course(course_id)

    @pytest.mark.term_edge
    def test_find_course_not_found(self, term1):
        """Test finding non-existent course raises KeyError."""
        course1 = Course(
            "CMPE 142", "Operating Systems",
            datetime(2025, 8, 12), datetime(2025, 12, 5), 3, False
        )
        course2 = Course(
            "ENGR 195A", "",
            datetime(2025, 8, 14), datetime(2025, 12, 18), 1, True
        )
        
        term1.add_course(course1)
        course_id = course2.id
        
        with pytest.raises(KeyError, match="Course not found"):
            term1.find_course(course_id)

    @pytest.mark.term_smoke
    def test_equality_basic(self, term1):
        """Test Term equality operator."""
        term2 = Term(
            "Spring 2025",
            datetime(2025, 1, 18),
            datetime(2025, 5, 28),
            False
        )
        term3 = Term(
            "Spring 2026",
            datetime(2026, 1, 20),
            datetime(2026, 5, 23),
            True
        )
        term4 = term1  # Copy reference
        
        assert term1 != term2
        assert term1 != term3
        assert term1 == term4

    @pytest.mark.term_edge
    def test_equality_same_title_different_params(self, term1):
        """Test equality with same title but different parameters."""
        term2 = Term(
            "Fall 2025",
            datetime(2025, 9, 1),
            datetime(2025, 12, 5),
            False
        )
        term3 = Term(
            "Fall 2025",
            datetime(2025, 8, 12),
            datetime(2025, 11, 29),
            False
        )
        term4 = Term(
            "Fall 2025",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            True
        )
        
        assert term1 != term2
        assert term1 != term3
        assert term1 != term4

    @pytest.mark.term_edge
    def test_equality_same_params_different_id(self):
        """Test equality with same parameters but different IDs."""
        term2 = Term(
            "Fall 2025",
            datetime(2025, 9, 1),
            datetime(2025, 12, 5),
            False
        )
        term3 = Term(
            "Fall 2025",
            datetime(2025, 9, 1),
            datetime(2025, 12, 5),
            False
        )
        
        assert term2 != term3

    @pytest.mark.term_smoke
    def test_from_row_basic(self):
        """Test Term.from_row class method with basic parameters."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        term = Term.from_row(
            test_id, "Fall 2025",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            False
        )
        
        assert term.id == test_id
        assert term.title == "Fall 2025"
        assert term.start_date == datetime(2025, 8, 12)
        assert term.end_date == datetime(2025, 12, 5)
        assert term.active is False

    @pytest.mark.term_smoke
    def test_from_row_active_true(self):
        """Test Term.from_row with active=True."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        term = Term.from_row(
            test_id, "Spring 2026",
            datetime(2026, 1, 20),
            datetime(2026, 5, 23),
            True
        )
        
        assert term.active is True

    @pytest.mark.term_smoke
    def test_from_row_preserves_id(self):
        """Test that from_row preserves the provided ID (key invariant)."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        term = Term.from_row(
            test_id, "Winter 2025",
            datetime(2025, 1, 6),
            datetime(2025, 3, 21),
            False
        )
        
        assert term.id == test_id

    @pytest.mark.term_smoke
    def test_from_row_does_not_equal_new_term(self):
        """Test that from_row Term and new Term with same params are not equal."""
        from_row_term = Term.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "Fall 2025",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            False
        )
        
        new_term = Term(
            "Fall 2025",
            datetime(2025, 8, 12),
            datetime(2025, 12, 5),
            False
        )
        
        assert from_row_term != new_term

    @pytest.mark.term_edge
    def test_from_row_empty_title(self):
        """Test from_row with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Term.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "",
                datetime(2025, 8, 12),
                datetime(2025, 12, 5),
                False
            )

    @pytest.mark.term_edge
    def test_from_row_whitespace_title(self):
        """Test from_row with whitespace title raises ValueError."""
        with pytest.raises(ValueError):
            Term.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "   ",
                datetime(2025, 8, 12),
                datetime(2025, 12, 5),
                False
            )

    @pytest.mark.term_edge
    def test_from_row_invalid_date_order(self):
        """Test from_row with end date before start date raises ValueError."""
        with pytest.raises(ValueError):
            Term.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "Fall 2025",
                datetime(2025, 12, 5),
                datetime(2025, 8, 12),
                False
            )

    @pytest.mark.term_edge
    def test_from_row_same_day_start_and_end(self):
        """Test from_row with same start and end date."""
        term = Term.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "One Day Term",
            datetime(2025, 8, 12),
            datetime(2025, 8, 12),
            True
        )
        
        assert term.start_date == term.end_date


class TestAssignment:
    """Test suite for Assignment model."""

    @pytest.fixture
    def assignment1(self) -> Assignment:
        """Create a sample Assignment for testing.
        
        Returns:
            Assignment: A test assignment with all fields populated.
        """
        return Assignment(
            "Homework 3",
            "Focus on variables and strings.",
            "Homework",
            datetime(2025, 11, 20),
            True,
            95.18
        )

    @pytest.mark.assignment_smoke
    def test_id_getter(self, assignment1: Assignment) -> None:
        """Ensure ID is not empty."""
        assert assignment1.id and not assignment1.id.isspace()

    @pytest.mark.assignment_smoke
    def test_title_getter(self, assignment1: Assignment) -> None:
        """Test title getter returns correct value."""
        assert assignment1.title == "Homework 3"

    @pytest.mark.assignment_smoke
    def test_description_getter(self, assignment1: Assignment) -> None:
        """Test description getter returns correct value."""
        assert assignment1.description == "Focus on variables and strings."

    @pytest.mark.assignment_smoke
    def test_category_getter(self, assignment1: Assignment) -> None:
        """Test category getter returns correct value."""
        assert assignment1.category == "Homework"

    @pytest.mark.assignment_smoke
    def test_due_date_getter(self, assignment1: Assignment) -> None:
        """Test due date getter returns correct value."""
        assert assignment1.due_date == datetime(2025, 11, 20)

    @pytest.mark.assignment_smoke
    def test_completed_getter(self, assignment1: Assignment) -> None:
        """Test completed getter returns correct value."""
        assert assignment1.completed is True

    @pytest.mark.assignment_smoke
    def test_grade_getter(self, assignment1: Assignment) -> None:
        """Test grade getter returns correct value."""
        assert math.isclose(assignment1.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_smoke
    def test_title_setter(self, assignment1: Assignment) -> None:
        """Test title setter updates the title."""
        assignment1.title = "Homework 2"
        assert assignment1.title == "Homework 2"

    @pytest.mark.assignment_smoke
    def test_description_setter(self, assignment1: Assignment) -> None:
        """Test description setter updates the description."""
        assignment1.description = "Focus on order of operations."
        assert assignment1.description == "Focus on order of operations."

    @pytest.mark.assignment_smoke
    def test_category_setter(self, assignment1: Assignment) -> None:
        """Test category setter updates the category."""
        assignment1.category = "Midterm"
        assert assignment1.category == "Midterm"

    @pytest.mark.assignment_smoke
    def test_due_date_setter(self, assignment1: Assignment) -> None:
        """Test due date setter updates the due date."""
        assignment1.due_date = datetime(2025, 11, 22)
        assert assignment1.due_date == datetime(2025, 11, 22)

    @pytest.mark.assignment_smoke
    def test_completed_setter(self, assignment1: Assignment) -> None:
        """Test completed setter updates the completed status."""
        assignment1.completed = False
        assert assignment1.completed is False

    @pytest.mark.assignment_smoke
    def test_grade_setter_percentage(self, assignment1: Assignment) -> None:
        """Test grade setter with percentage value."""
        assignment1.grade = (96.20,)
        assert math.isclose(assignment1.grade, 96.20, abs_tol=1e-9)

    @pytest.mark.assignment_smoke
    def test_grade_setter_points(self, assignment1: Assignment) -> None:
        """Test grade setter with points earned and total points."""
        assignment1.grade = (18, 20)
        assert math.isclose(assignment1.grade, 90.0, abs_tol=1e-9)

    @pytest.mark.assignment_smoke
    def test_initialization_without_description(self) -> None:
        """Test initialization with empty description."""
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 0.0
        )
        assert assignment2.id and not assignment2.id.isspace()
        assert assignment2.title == "Homework 1"
        assert assignment2.category == "Homework"
        assert assignment2.description == ""

    @pytest.mark.assignment_smoke
    def test_initialization_with_description(self) -> None:
        """Test initialization with description."""
        assignment2 = Assignment(
            "Homework 1", "Focus on lexical analysis.", "Homework",
            datetime(2025, 10, 31), True, 90.50
        )
        assert assignment2.id and not assignment2.id.isspace()
        assert assignment2.title == "Homework 1"
        assert assignment2.category == "Homework"
        assert assignment2.description == "Focus on lexical analysis."
        assert assignment2.due_date == datetime(2025, 10, 31)
        assert assignment2.completed is True
        assert math.isclose(assignment2.grade, 90.50, abs_tol=1e-9)

    @pytest.mark.assignment_smoke
    def test_print_assignment_info(self, assignment1: Assignment) -> None:
        """Test print_assignment_info outputs correct format."""
        ss = StringIO()
        assignment1.print_assignment_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = ("ID: <UUID>\nAssignment: Homework 3\n"
                   "Description: Focus on variables and strings.\n"
                   "Category: Homework\nDue Date: 2025-11-20 00:00:00\n"
                   "Completed? Yes\nGrade: 95.18%\n")
        assert output == expected

    @pytest.mark.assignment_smoke
    def test_equality_basic(self, assignment1: Assignment) -> None:
        """Test Assignment equality operator."""
        assignment2 = Assignment(
            "Homework 1", "Focus on lexical analysis.", "Homework",
            datetime(2025, 10, 31), True, 75
        )
        assignment3 = Assignment(
            "Homework 3", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 20), True, 95.18
        )
        assignment4 = assignment1  # Copy reference

        assert assignment1 != assignment2
        assert assignment1 != assignment3
        assert assignment1 == assignment4

    @pytest.mark.assignment_smoke
    def test_from_row_all_fields(self) -> None:
        """Test Assignment.from_row class method with all fields."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        assignment = Assignment.from_row(
            test_id, "Homework 3", "Focus on variables and strings.",
            "Homework", datetime(2025, 11, 20), True, 95.18
        )

        assert assignment.id == test_id
        assert assignment.title == "Homework 3"
        assert assignment.description == "Focus on variables and strings."
        assert assignment.category == "Homework"
        assert assignment.due_date == datetime(2025, 11, 20)
        assert assignment.completed is True
        assert math.isclose(assignment.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_smoke
    def test_from_row_preserves_id(self) -> None:
        """Test that from_row preserves the provided ID."""
        test_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        assignment = Assignment.from_row(
            test_id, "Homework 3", "",
            "Homework", datetime(2025, 11, 20), False, 0.0
        )

        assert assignment.id == test_id

    @pytest.mark.assignment_smoke
    def test_from_row_completed_false(self) -> None:
        """Test from_row with completed=False."""
        assignment = Assignment.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "Homework 3", "", "Homework",
            datetime(2025, 11, 20), False, 0.0
        )

        assert assignment.completed is False

    @pytest.mark.assignment_smoke
    def test_from_row_empty_description(self) -> None:
        """Test from_row with empty description."""
        assignment = Assignment.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "Homework 3", "", "Homework",
            datetime(2025, 11, 20), False, 0.0
        )

        assert assignment.description == ""

    @pytest.mark.assignment_smoke
    def test_from_row_does_not_equal_new_assignment(self) -> None:
        """Test that from_row Assignment and new Assignment with same params are not equal."""
        from_row_assignment = Assignment.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "Homework 3", "Focus on variables and strings.",
            "Homework", datetime(2025, 11, 20), True, 95.18
        )
        new_assignment = Assignment(
            "Homework 3", "Focus on variables and strings.",
            "Homework", datetime(2025, 11, 20), True, 95.18
        )

        assert from_row_assignment != new_assignment

    @pytest.mark.assignment_edge
    def test_description_getter_empty(self) -> None:
        """Test description getter with empty description."""
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 90.50
        )
        assert assignment2.description == ""

    @pytest.mark.assignment_edge
    def test_completed_getter_default(self) -> None:
        """Test completed getter when not explicitly set."""
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 0.0
        )
        assert assignment2.completed is False

    @pytest.mark.assignment_edge
    def test_grade_getter_default(self) -> None:
        """Test grade getter when assignment is not completed."""
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 0.0
        )
        assert math.isclose(assignment2.grade, 0.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_title_setter_empty(self, assignment1: Assignment) -> None:
        """Test title setter with empty string raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.title = ""
        assert assignment1.title == "Homework 3"

    @pytest.mark.assignment_edge
    def test_title_setter_whitespace(self, assignment1: Assignment) -> None:
        """Test title setter with whitespace raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.title = " "
        assert assignment1.title == "Homework 3"

    @pytest.mark.assignment_edge
    def test_grade_setter_percentage_invalid_low(self, assignment1: Assignment) -> None:
        """Test grade setter with percentage below 0 raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (-20.24,)
        assert math.isclose(assignment1.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_percentage_invalid_high(self, assignment1: Assignment) -> None:
        """Test grade setter with percentage above 150 raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (200.24,)
        assert math.isclose(assignment1.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_percentage_boundary_low(self, assignment1: Assignment) -> None:
        """Test grade setter with percentage at lower boundary (0)."""
        assignment1.grade = (0.0,)
        assert math.isclose(assignment1.grade, 0.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_percentage_boundary_high(self, assignment1: Assignment) -> None:
        """Test grade setter with percentage at upper boundary (100)."""
        assignment1.grade = (100.0,)
        assert math.isclose(assignment1.grade, 100.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_invalid_low(self, assignment1: Assignment) -> None:
        """Test grade setter with points below 0 raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (-3, 20)
        assert math.isclose(assignment1.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_invalid_high(self, assignment1: Assignment) -> None:
        """Test grade setter with points above total raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (40, 20)
        assert math.isclose(assignment1.grade, 95.18, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_boundary_low(self, assignment1: Assignment) -> None:
        """Test grade setter with points at lower boundary (0)."""
        assignment1.grade = (0, 20)
        assert math.isclose(assignment1.grade, 0.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_boundary_high(self, assignment1: Assignment) -> None:
        """Test grade setter with points at upper boundary (total)."""
        assignment1.grade = (20, 20)
        assert math.isclose(assignment1.grade, 100.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_negative_total(self, assignment1: Assignment) -> None:
        """Test grade setter with negative total points raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (20, -20)

    @pytest.mark.assignment_edge
    def test_grade_setter_points_zero_total(self, assignment1: Assignment) -> None:
        """Test grade setter with zero total points raises ValueError."""
        with pytest.raises(ValueError):
            assignment1.grade = (20, 0)

    @pytest.mark.assignment_edge
    def test_initialization_empty_title(self) -> None:
        """Test initialization with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Assignment("", "", "Homework", datetime(2025, 10, 31), False, 0.0)

    @pytest.mark.assignment_edge
    def test_initialization_empty_category(self) -> None:
        """Test initialization with empty category raises ValueError."""
        with pytest.raises(ValueError):
            Assignment("Homework 1", "", "", datetime(2025, 10, 31), False, 0.0)

    @pytest.mark.assignment_edge
    def test_initialization_invalid_grade_low(self) -> None:
        """Test initialization with grade below 0 raises ValueError."""
        with pytest.raises(ValueError):
            Assignment(
                "Homework 1", "", "Homework",
                datetime(2025, 10, 31), True, -20.24
            )

    @pytest.mark.assignment_edge
    def test_initialization_invalid_grade_high(self) -> None:
        """Test initialization with grade above 150 raises ValueError."""
        with pytest.raises(ValueError):
            Assignment(
                "Homework 1", "", "Homework",
                datetime(2025, 10, 31), True, 200.24
            )

    @pytest.mark.assignment_edge
    def test_initialization_completed_false_with_grade(self) -> None:
        """Test that grade is set to 0 when completed is False."""
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 90.50
        )
        assert assignment2.completed is False
        assert math.isclose(assignment2.grade, 0.0, abs_tol=1e-9)

    @pytest.mark.assignment_edge
    def test_print_assignment_info_partial(self) -> None:
        """Test print_assignment_info with minimal fields."""
        ss = StringIO()
        assignment2 = Assignment(
            "Homework 1", "", "Homework",
            datetime(2025, 10, 31), False, 0.0
        )
        assignment2.print_assignment_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = ("ID: <UUID>\nAssignment: Homework 1\n"
                   "Category: Homework\nDue Date: 2025-10-31 00:00:00\n"
                   "Completed? No\nGrade: 0.00%\n")
        assert output == expected

    @pytest.mark.assignment_edge
    def test_print_assignment_info_with_description(self) -> None:
        """Test print_assignment_info with description."""
        ss = StringIO()
        assignment2 = Assignment(
            "Homework 1", "Focus on lexical analysis.", "Homework",
            datetime(2025, 10, 31), False, 0.0
        )
        assignment2.print_assignment_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = ("ID: <UUID>\nAssignment: Homework 1\n"
                   "Description: Focus on lexical analysis.\n"
                   "Category: Homework\nDue Date: 2025-10-31 00:00:00\n"
                   "Completed? No\nGrade: 0.00%\n")
        assert output == expected

    @pytest.mark.assignment_edge
    def test_print_assignment_info_integer_grade(self) -> None:
        """Test print_assignment_info with integer grade."""
        ss = StringIO()
        assignment2 = Assignment(
            "Homework 1", "Focus on lexical analysis.", "Homework",
            datetime(2025, 10, 31), True, 75
        )
        assignment2.print_assignment_info(ss)
        output = ss.getvalue()
        output = mask_uuids(output)

        expected = ("ID: <UUID>\nAssignment: Homework 1\n"
                   "Description: Focus on lexical analysis.\n"
                   "Category: Homework\nDue Date: 2025-10-31 00:00:00\n"
                   "Completed? Yes\nGrade: 75.00%\n")
        assert output == expected

    @pytest.mark.assignment_edge
    def test_equality_same_title_different_params(self, assignment1: Assignment) -> None:
        """Test equality with same title but different parameters."""
        assignment2 = Assignment(
            "Homework 1", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 20), True, 95.18
        )
        assignment3 = Assignment(
            "Homework 3", "Focus on functions.", "Homework",
            datetime(2025, 11, 20), True, 95.18
        )
        assignment4 = Assignment(
            "Homework 3", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 19), True, 95.18
        )
        assignment5 = Assignment(
            "Homework 3", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 20), False, 92.71
        )

        assert assignment1 != assignment2
        assert assignment1 != assignment3
        assert assignment1 != assignment4
        assert assignment1 != assignment5

    @pytest.mark.assignment_edge
    def test_equality_same_params_different_id(self) -> None:
        """Test equality with same parameters but different IDs."""
        assignment2 = Assignment(
            "Homework 1", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 20), True, 95.18
        )
        assignment3 = Assignment(
            "Homework 1", "Focus on variables and strings.", "Homework",
            datetime(2025, 11, 20), True, 95.18
        )

        assert assignment2 != assignment3

    @pytest.mark.assignment_edge
    def test_from_row_empty_title(self) -> None:
        """Test from_row with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Assignment.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "", "",
                "Homework", datetime(2025, 11, 20), False, 0.0
            )

    @pytest.mark.assignment_edge
    def test_from_row_whitespace_title(self) -> None:
        """Test from_row with whitespace title raises ValueError."""
        with pytest.raises(ValueError):
            Assignment.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "   ", "",
                "Homework", datetime(2025, 11, 20), False, 0.0
            )

    @pytest.mark.assignment_edge
    def test_from_row_empty_category(self) -> None:
        """Test from_row with empty category raises ValueError."""
        with pytest.raises(ValueError):
            Assignment.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "Homework 3", "",
                "", datetime(2025, 11, 20), False, 0.0
            )

    @pytest.mark.assignment_edge
    def test_from_row_grade_too_low(self) -> None:
        """Test from_row with grade below 0 raises ValueError."""
        with pytest.raises(ValueError):
            Assignment.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "Homework 3", "",
                "Homework", datetime(2025, 11, 20), True, -1.0
            )

    @pytest.mark.assignment_edge
    def test_from_row_grade_too_high(self) -> None:
        """Test from_row with grade above 150 raises ValueError."""
        with pytest.raises(ValueError):
            Assignment.from_row(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "Homework 3", "",
                "Homework", datetime(2025, 11, 20), True, 200.0
            )

    @pytest.mark.assignment_edge
    def test_from_row_zero_grade_when_not_completed(self) -> None:
        """Test that from_row zeroes grade when completed is False."""
        assignment = Assignment.from_row(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "Homework 3", "", "Homework",
            datetime(2025, 11, 20), False, 90.0
        )

        assert math.isclose(assignment.grade, 0.0, abs_tol=1e-9)
