"""Tests for the TermController class."""
# Standard library imports
import re
from datetime import datetime

import pytest

# Local imports
from controllers.term_controller import TermController
from models.term import Term


class TestTermController:
    """Test suite for TermController."""

    @pytest.fixture
    def controller(self) -> TermController:
        """Create a TermController instance for testing.
        
        Returns:
            TermController: A fresh TermController instance.
        """
        return TermController()

    @pytest.fixture
    def sample_term(self) -> Term:
        """Create a sample Term for testing.
        
        Returns:
            Term: A sample Term with default values.
        """
        return Term(
            "Fall 2025",
            datetime(2025, 8, 15),
            datetime(2025, 12, 17),
            False
        )

    @pytest.mark.term_controller_smoke
    def test_term_list_getter(self, controller):
        """Test that term_list getter returns correct terms."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        term_list = controller.term_list
        assert len(term_list) == 2

        # Check if both added terms are in the list
        id1 = controller.get_term_id("Fall 2025")
        assert id1 in term_list

        id2 = controller.get_term_id("Spring 2026")
        assert id2 in term_list

    @pytest.mark.term_controller_smoke
    def test_term_id_getter(self, controller):
        """Test that get_term_id returns a valid UUID."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        id = controller.get_term_id("Fall 2025")

        # Check if the ID is in the correct UUID format
        uuid_pattern = r"""
            ^[0-9a-fA-F]{8}
            -[0-9a-fA-F]{4}
            -[0-9a-fA-F]{4}
            -[0-9a-fA-F]{4}
            -[0-9a-fA-F]{12}$
        """
        assert re.match(uuid_pattern, id, re.VERBOSE)

    @pytest.mark.term_controller_smoke
    def test_term_order_getter(self, controller):
        """Test that term_order getter returns correct order."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        term_order = controller.term_order
        assert len(term_order) == 2

        # Verify the order matches the order terms were added
        id1 = controller.get_term_id("Fall 2025")
        id2 = controller.get_term_id("Spring 2026")
        assert term_order[0] == id1
        assert term_order[1] == id2

    @pytest.mark.term_controller_smoke
    def test_add_term(self, controller):
        """Test adding a term to the controller."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        selected_term = controller.find_term("Fall 2025")
        assert selected_term.title == "Fall 2025"
        assert selected_term.start_date == datetime(2025, 8, 15)
        assert selected_term.end_date == datetime(2025, 12, 17)
        assert selected_term.active is False

    @pytest.mark.term_controller_smoke
    def test_edit_title(self, controller):
        """Test editing a term's title."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        id = controller.get_term_id("Fall 2025")
        controller.edit_title(id, "Winter 2026")

        # Check that title has been edited and title -> id mapping is correct
        selected_term = controller.find_term("Winter 2026")
        assert selected_term.title == "Winter 2026"
        assert controller.get_term_id("Winter 2026") == id

    @pytest.mark.term_controller_smoke
    def test_edit_start_date(self, controller):
        """Test editing a term's start date."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        controller.edit_start_date(id, datetime(2025, 8, 20))

        selected_term = controller.find_term("Fall 2025")
        assert selected_term.start_date == datetime(2025, 8, 20)

    @pytest.mark.term_controller_smoke
    def test_edit_end_date(self, controller):
        """Test editing a term's end date."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        controller.edit_end_date(id, datetime(2025, 12, 20))

        selected_term = controller.find_term("Fall 2025")
        assert selected_term.end_date == datetime(2025, 12, 20)

    @pytest.mark.term_controller_smoke
    def test_edit_active(self, controller):
        """Test editing a term's active status."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        controller.edit_active(id, True)

        selected_term = controller.find_term("Fall 2025")
        assert selected_term.active is True

    @pytest.mark.term_controller_smoke
    def test_remove_term(self, controller):
        """Test removing a term from the controller."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        controller.remove_term("Fall 2025")

        term_list = controller.term_list
        assert len(term_list) == 1

        # Raise KeyError since the term is not in the list
        with pytest.raises(KeyError):
            controller.get_term_id("Fall 2025")

        id2 = controller.get_term_id("Spring 2026")
        assert id2 in term_list

    @pytest.mark.term_controller_smoke
    def test_find_term(self, controller):
        """Test finding a term by title."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        selected_term = controller.find_term("Spring 2026")
        assert selected_term.title == "Spring 2026"
        assert selected_term.start_date == datetime(2026, 1, 2)
        assert selected_term.end_date == datetime(2026, 5, 24)
        assert selected_term.active is True

    @pytest.mark.term_controller_smoke
    def test_select_term(self, controller):
        """Test selecting a term by title."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        controller.select_term("Fall 2025")

        assert controller.active_term.title == "Fall 2025"
        assert controller.active_term.start_date == datetime(2025, 8, 15)
        assert controller.active_term.end_date == datetime(2025, 12, 17)
        assert controller.active_term.active is False

    @pytest.mark.term_controller_smoke
    def test_active_term_property(self, controller):
        """Test that active_term property returns the selected term."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.select_term("Fall 2025")

        active_term = controller.active_term
        assert active_term.title == "Fall 2025"

    @pytest.mark.term_controller_smoke
    def test_course_controller_property(self, controller):
        """Test that course_controller property returns CourseController when term is selected."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.select_term("Fall 2025")

        course_controller = controller.course_controller
        assert course_controller is not None

    @pytest.mark.term_controller_edge
    def test_term_list_getter_empty(self, controller):
        """Test that term_list getter returns empty dict when no terms exist."""
        term_list = controller.term_list
        assert len(term_list) == 0

    @pytest.mark.term_controller_edge
    def test_term_order_getter_empty(self, controller):
        """Test that term_order getter returns empty tuple when no terms exist."""
        term_order = controller.term_order
        assert len(term_order) == 0

    @pytest.mark.term_controller_edge
    def test_term_id_getter_not_found(self, controller):
        """Test that get_term_id raises KeyError when term not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        with pytest.raises(KeyError):
            controller.get_term_id("Fall 2026")

    @pytest.mark.term_controller_edge
    def test_add_term_already_exists(self, controller):
        """Test that add_term raises ValueError when term already exists."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(ValueError):
            controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

    @pytest.mark.term_controller_edge
    def test_add_term_already_exists_different_case(self, controller):
        """Test that add_term raises ValueError when term already exists (case insensitive)."""
        controller.add_term("FALL 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(ValueError):
            controller.add_term("fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

    @pytest.mark.term_controller_edge
    def test_edit_title_already_exists(self, controller):
        """Test that edit_title raises ValueError when new title already exists."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)
        
        id = controller.get_term_id("Fall 2025")
        
        with pytest.raises(ValueError):
            controller.edit_title(id, "Spring 2026")

    @pytest.mark.term_controller_edge
    def test_edit_title_already_exists_different_case(self, controller):
        """Test that edit_title raises ValueError when new title already 
        exists (case insensitive).
        """
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)
        
        id = controller.get_term_id("Fall 2025")
        
        with pytest.raises(ValueError):
            controller.edit_title(id, "SPRING 2026")

    @pytest.mark.term_controller_edge
    def test_edit_title_not_found(self, controller):
        """Test that edit_title raises KeyError when term ID not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(KeyError):
            controller.edit_title("non-existent-id", "Winter 2026")

    @pytest.mark.term_controller_edge
    def test_edit_start_date_not_found(self, controller):
        """Test that edit_start_date raises KeyError when term ID not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(KeyError):
            controller.edit_start_date("non-existent-id", datetime(2025, 8, 20))

    @pytest.mark.term_controller_edge
    def test_edit_end_date_not_found(self, controller):
        """Test that edit_end_date raises KeyError when term ID not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(KeyError):
            controller.edit_end_date("non-existent-id", datetime(2025, 12, 20))

    @pytest.mark.term_controller_edge
    def test_edit_active_not_found(self, controller):
        """Test that edit_active raises KeyError when term ID not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        with pytest.raises(KeyError):
            controller.edit_active("non-existent-id", True)

    @pytest.mark.term_controller_edge
    def test_edit_start_date_invalid_order(self, controller):
        """Test that edit_start_date raises ValueError when new start date is after end date."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        
        with pytest.raises(ValueError):
            controller.edit_start_date(id, datetime(2025, 12, 20))

    @pytest.mark.term_controller_edge
    def test_edit_end_date_invalid_order(self, controller):
        """Test that edit_end_date raises ValueError when new end date is before start date."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        
        with pytest.raises(ValueError):
            controller.edit_end_date(id, datetime(2025, 8, 10))

    @pytest.mark.term_controller_edge
    def test_edit_title_same_title(self, controller):
        """Test that edit_title allows editing a term to its own title (self-assignment)."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        id = controller.get_term_id("Fall 2025")
        
        # Should not raise ValueError when editing to the same title
        controller.edit_title(id, "Fall 2025")
        
        # Verify the term still exists and has the same title
        selected_term = controller.find_term("Fall 2025")
        assert selected_term.title == "Fall 2025"
        assert controller.get_term_id("Fall 2025") == id

    @pytest.mark.term_controller_edge
    def test_remove_term_not_found(self, controller):
        """Test that remove_term raises KeyError when term not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        with pytest.raises(KeyError):
            controller.remove_term("Fall 2026")

    @pytest.mark.term_controller_edge
    def test_remove_term_case_insensitive(self, controller):
        """Test that remove_term works with case-insensitive title lookup."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        # Should remove the term regardless of case
        controller.remove_term("FALL 2025")

        term_list = controller.term_list
        assert len(term_list) == 1

        # Verify the term was actually removed
        with pytest.raises(KeyError):
            controller.get_term_id("Fall 2025")

        # Verify the other term still exists
        id2 = controller.get_term_id("Spring 2026")
        assert id2 in term_list

    @pytest.mark.term_controller_edge
    def test_find_term_not_found(self, controller):
        """Test that find_term raises KeyError when term not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        with pytest.raises(KeyError):
            controller.find_term("Fall 2026")

    @pytest.mark.term_controller_edge
    def test_select_term_not_found(self, controller):
        """Test that select_term raises ValueError when term not found."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        with pytest.raises(KeyError):
            controller.select_term("Fall 2026")

    @pytest.mark.term_controller_edge
    def test_active_term_property_not_selected(self, controller):
        """Test that active_term property raises ValueError when no term selected."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        with pytest.raises(ValueError, match="No Term selected"):
            _ = controller.active_term

    @pytest.mark.term_controller_edge
    def test_course_controller_property_not_selected(self, controller):
        """Test that course_controller property raises ValueError when no term selected."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)

        with pytest.raises(ValueError, match="No Term selected"):
            _ = controller.course_controller

    @pytest.mark.term_controller_edge
    def test_remove_active_term(self, controller):
        """Test that removing the active term clears active_term and course_controller."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)
        
        controller.select_term("Fall 2025")
        assert controller.active_term is not None
        assert controller.course_controller is not None
        
        controller.remove_term("Fall 2025")
        
        with pytest.raises(ValueError, match="No Term selected"):
            _ = controller.active_term
        
        with pytest.raises(ValueError, match="No Term selected"):
            _ = controller.course_controller

    @pytest.mark.term_controller_edge
    def test_term_order_preserved_after_removal(self, controller):
        """Test that term_order is correctly updated after term removal."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)
        controller.add_term("Summer 2026", datetime(2026, 6, 1), datetime(2026, 8, 15), False)
        
        initial_order = controller.term_order
        assert len(initial_order) == 3
        
        controller.remove_term("Spring 2026")
        
        new_order = controller.term_order
        assert len(new_order) == 2
        
        # Verify the remaining terms are in the correct order
        id1 = controller.get_term_id("Fall 2025")
        id3 = controller.get_term_id("Summer 2026")
        assert new_order[0] == id1
        assert new_order[1] == id3

    @pytest.mark.term_controller_edge
    def test_multiple_terms_case_insensitive_lookup(self, controller):
        """Test that term lookup is case-insensitive."""
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        
        # Should find the term regardless of case
        id_upper = controller.get_term_id("FALL 2025")
        id_lower = controller.get_term_id("fall 2025")
        id_mixed = controller.get_term_id("FaLl 2025")
        
        assert id_upper == id_lower == id_mixed

    @pytest.mark.term_controller_edge
    def test_term_reselection_preserves_course_state(self, controller):
        """Test that reselecting a term preserves course controller state.
        
        This test addresses the bug where course indexes were lost when
        reselecting a term, causing course lookup, selection, removal,
        and ordering to fail despite courses remaining in Term._course_list.
        """
        controller.add_term("Fall 2025", datetime(2025, 8, 15), datetime(2025, 12, 17), False)
        controller.add_term("Spring 2026", datetime(2026, 1, 2), datetime(2026, 5, 24), True)

        # Select first term and add a course
        controller.select_term("Fall 2025")
        first_course_controller = controller.course_controller
        first_course_controller.add_course(
            "Calculus I",
            "Introduction to calculus",
            datetime(2025, 8, 20),
            datetime(2025, 12, 15),
            4,
            True
        )
        first_course_controller.add_course(
            "Physics I",
            "Introduction to physics",
            datetime(2025, 8, 20),
            datetime(2025, 12, 15),
            4,
            True
        )

        # Select second term
        controller.select_term("Spring 2026")
        second_course_controller = controller.course_controller
        second_course_controller.add_course(
            "Chemistry I",
            "Introduction to chemistry",
            datetime(2026, 1, 5),
            datetime(2026, 5, 20),
            4,
            True
        )

        # Reselect first term - this should restore course controller state
        controller.select_term("Fall 2025")
        restored_course_controller = controller.course_controller

        # Verify that the course controller is a new instance but has restored state
        assert restored_course_controller is not first_course_controller

        # Verify course lookup works
        calculus_id = restored_course_controller.get_course_id("Calculus I")
        physics_id = restored_course_controller.get_course_id("Physics I")

        # Verify course selection works
        restored_course_controller.select_course("Calculus I")
        assert restored_course_controller.active_course.title == "Calculus I"

        # Verify course order is preserved
        course_order = restored_course_controller.course_order
        assert len(course_order) == 2
        assert course_order[0] == calculus_id
        assert course_order[1] == physics_id

        # Verify course removal works
        restored_course_controller.remove_course("Physics I")
        with pytest.raises(KeyError):
            restored_course_controller.get_course_id("Physics I")

        # Verify the course was actually removed from the term
        assert len(restored_course_controller.course_order) == 1
