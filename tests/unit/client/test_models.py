# Standard library imports
import re
from datetime import datetime
from io import StringIO

import pytest
from models.course import Course

# Local imports
from models.term import Term

# Pytest markers configuration
pytestmark = [
    pytest.mark.term_smoke,
    pytest.mark.term_edge
]


# Helper function to mask UUIDs in output
def mask_uuids(output: str) -> str:
    """Replace UUIDs in output string with <UUID> placeholder."""
    uuid_pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    return re.sub(uuid_pattern, "<UUID>", output)


class TestTerm:
    """Test suite for Term model."""

    @pytest.fixture
    def term1(self):
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
        found_course.active = False
        
        # Verify the modification
        assert term1.find_course(course1.id).active is False

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
