"""Tests for the CliView class."""
import io
import math
from datetime import datetime

import pytest

from controllers.term_controller import TermController
from views.cli_view import CliView


class TestCliView:
    """Test suite for CliView."""

    @pytest.fixture
    def controller(self) -> TermController:
        """Create a TermController instance for testing.

        Returns:
            TermController: A fresh TermController instance.
        """
        return TermController()

    @pytest.mark.cli_view_smoke
    def test_full_constructor_initialization(self, controller):
        """Test that CliView can be initialized with all parameters."""
        input_stream = io.StringIO()
        output_stream = io.StringIO()
        view = CliView(controller, input_stream, output_stream)
        assert view is not None

    @pytest.mark.cli_view_smoke
    def test_user_exits_immediately(self, controller):
        """Test that user can exit immediately."""
        input_stream = io.StringIO("X\n")
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        assert "Welcome" in output_stream.getvalue()

    @pytest.mark.cli_view_smoke
    def test_add_term(self, controller):
        """Test adding a term."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        selected_term = controller.find_term("Spring 2025")
        assert selected_term.title == "Spring 2025"
        assert selected_term.start_date == datetime(2025, 1, 10)
        assert selected_term.end_date == datetime(2025, 5, 23)
        assert selected_term.active is True

        user_out = output_stream.getvalue()
        assert "Enter the following information" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_smoke
    def test_edit_term(self, controller):
        """Test editing a term."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "title, start date, end date, active\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        selected_term = controller.find_term("Fall 2025")
        assert selected_term.title == "Fall 2025"
        assert selected_term.start_date == datetime(2025, 8, 2)
        assert selected_term.end_date == datetime(2025, 12, 11)
        assert selected_term.active is False

        user_out = output_stream.getvalue()
        assert "Enter the following information" in user_out
        assert "Update results" in user_out

    @pytest.mark.cli_view_smoke
    def test_select_term(self, controller):
        """Test selecting a term."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Enter the following information" in user_out
        assert "was selected" in user_out

    @pytest.mark.cli_view_smoke
    def test_remove_term(self, controller):
        """Test removing a term."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "A\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "R\n"
            "Spring 2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        with pytest.raises(KeyError):
            controller.find_term("Spring 2025")

        user_out = output_stream.getvalue()
        assert "Enter the following information" in user_out
        assert "was removed" in user_out

    @pytest.mark.cli_view_smoke
    def test_add_course(self, controller):
        """Test adding a course."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        selected_course = course_controller.find_course("ENGR 195A")
        assert selected_course.title == "ENGR 195A"
        assert selected_course.description == ""
        assert selected_course.start_date == datetime(2025, 1, 2)
        assert selected_course.end_date == datetime(2025, 5, 12)
        assert selected_course.num_credits == 3
        assert selected_course.active is True

        user_out = output_stream.getvalue()
        assert "for the course you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_smoke
    def test_edit_course(self, controller):
        """Test editing a course."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "title, description, start date, end date, number of credits, active\n"
            "CMPE 152\n"
            "Compiler Design\n"
            "01-03-2026\n"
            "05-22-2026\n"
            "2\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        selected_course = course_controller.find_course("CMPE 152")
        assert selected_course.title == "CMPE 152"
        assert selected_course.description == "Compiler Design"
        assert selected_course.start_date == datetime(2026, 1, 3)
        assert selected_course.end_date == datetime(2026, 5, 22)
        assert selected_course.num_credits == 2
        assert selected_course.active is False

        user_out = output_stream.getvalue()
        assert "for the course you want to edit" in user_out
        assert "New number of credits" in user_out
        assert "Update results" in user_out

    @pytest.mark.cli_view_smoke
    def test_select_course(self, controller):
        """Test selecting a course."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "for the course you want to select" in user_out
        assert "Course 'ENGR 195A' was selected" in user_out

    @pytest.mark.cli_view_smoke
    def test_remove_course(self, controller):
        """Test removing a course."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "A\n"
            "CMPE 142\n"
            "Operating Systems\n"
            "01-01-2025\n"
            "05-23-2025\n"
            "3\n"
            "no\n"
            "R\n"
            "ENGR 195A\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        with pytest.raises(KeyError):
            course_controller.find_course("ENGR 195A")

        user_out = output_stream.getvalue()
        assert "for the course you want to remove" in user_out
        assert "Course 'ENGR 195A' was removed" in user_out

    @pytest.mark.cli_view_smoke
    def test_add_assignment_pct(self, controller):
        """Test adding an assignment with percentage grade."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert selected_assignment.title == "Homework 1"
        assert selected_assignment.description == ""
        assert selected_assignment.due_date == datetime(2025, 1, 30)
        assert selected_assignment.completed is True
        assert math.isclose(selected_assignment.grade, 90.5, abs_tol=1e-9)

        user_out = output_stream.getvalue()
        assert "for the assignment you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_smoke
    def test_add_assignment_points(self, controller):
        """Test adding an assignment with points grade."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "17/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert selected_assignment.title == "Homework 1"
        assert selected_assignment.description == ""
        assert selected_assignment.due_date == datetime(2025, 1, 30)
        assert selected_assignment.completed is True
        assert math.isclose(selected_assignment.grade, 85.0, abs_tol=1e-9)

        user_out = output_stream.getvalue()
        assert "for the assignment you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_smoke
    def test_remove_assignment(self, controller):
        """Test removing an assignment."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "Linked lists\n"
            "Homework\n"
            "02-03-2025\n"
            "no\n"
            "0.0\n"
            "R\n"
            "Homework 1\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to remove" in user_out
        assert "you want to remove" in user_out
        assert "Assignment 'Homework 1' was removed" in user_out

    @pytest.mark.cli_view_smoke
    def test_add_assignment_grade_pct(self, controller):
        """Test adding a grade to an assignment using percentage."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 90.5, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 90.5 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_smoke
    def test_add_assignment_grade_points(self, controller):
        """Test adding a grade to an assignment using points."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "17/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 85.0, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 85.0 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_smoke
    def test_remove_assignment_grade(self, controller):
        """Test removing a grade from an assignment."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "M\n"
            "Homework 1\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 0.0, abs_tol=1e-9)
        assert selected_assignment.completed is False

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to remove" in user_out
        assert "Grade removed from assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_smoke
    def test_view_assignments_all(self, controller):
        """Test viewing all assignments."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "yes\n"
            "88.24\n"
            "V\n"
            "A\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "Assignment: Homework 1" in user_out
        assert "2025-01-30" in user_out
        assert "Assignment: Homework 2" in user_out
        assert "2025-02-05" in user_out
        assert "Assignment: Homework 3" in user_out
        assert "2025-02-13" in user_out

    @pytest.mark.cli_view_smoke
    def test_view_assignments_completed(self, controller):
        """Test viewing completed assignments."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "yes\n"
            "88.24\n"
            "V\n"
            "C\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "Assignment: Homework 1" in user_out
        assert "2025-01-30" in user_out
        assert "Assignment: Homework 2" not in user_out
        assert "2025-02-05" not in user_out
        assert "Assignment: Homework 3" in user_out
        assert "2025-02-13" in user_out

    @pytest.mark.cli_view_smoke
    def test_view_assignments_incomplete(self, controller):
        """Test viewing incomplete assignments."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "yes\n"
            "88.24\n"
            "V\n"
            "I\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "Assignment: Homework 1" in user_out
        assert "2025-01-30" in user_out
        assert "Assignment: Homework 2" in user_out
        assert "2025-02-05" in user_out
        assert "Assignment: Homework 3" not in user_out
        assert "2025-02-13" not in user_out

    @pytest.mark.cli_view_edge
    def test_empty_input(self, controller):
        """Test handling of empty input."""
        input_stream = io.StringIO(
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid selection" not in user_out

    @pytest.mark.cli_view_edge
    def test_invalid_input(self, controller):
        """Test handling of invalid input."""
        input_stream = io.StringIO(
            "I\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid selection" in user_out

    @pytest.mark.cli_view_edge
    def test_lowercase_input(self, controller):
        """Test handling of lowercase input."""
        input_stream = io.StringIO(
            "a\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Enter the following information" in user_out

    @pytest.mark.cli_view_edge
    def test_long_input(self, controller):
        """Test handling of long input."""
        input_stream = io.StringIO(
            "Avatar\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_term_menu_invalid_selection(self, controller):
        """Test invalid selection in term menu."""
        input_stream = io.StringIO(
            "R\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid selection" in user_out

    @pytest.mark.cli_view_edge
    def test_course_menu_invalid_selection(self, controller):
        """Test invalid selection in course menu."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "R\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Term 'Spring 2025' was selected" in user_out
        assert "Invalid selection" in user_out

    @pytest.mark.cli_view_edge
    def test_assignment_menu_invalid_selection(self, controller):
        """Test invalid selection in assignment menu."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "R\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Course 'ENGR 195A' was selected" in user_out
        assert "Invalid selection" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_title_empty(self, controller):
        """Test adding term with empty title."""
        input_stream = io.StringIO(
            "A\n"
            "\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Title cannot be empty" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_start_date_empty(self, controller):
        """Test adding term with empty start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "\n"
            "\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_start_date_wrong_format(self, controller):
        """Test adding term with wrong start date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "invalid\n"
            "05-23-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_end_date_empty(self, controller):
        """Test adding term with empty end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_end_date_wrong_format(self, controller):
        """Test adding term with wrong end date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "invalid\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_end_date_before_start_date(self, controller):
        """Test adding term with end date before start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "12-20-2024\n"
            "05-23-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "End date must be after start date" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_active_empty(self, controller):
        """Test adding term with empty active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "05-18-2025\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_active_invalid(self, controller):
        """Test adding term with invalid active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "05-18-2025\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_already_exists(self, controller):
        """Test adding term that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "05-18-2025\n"
            "yes\n"
            "A\n"
            "Spring 2025\n"
            "01-22-2025\n"
            "05-18-2025\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "already exists" in user_out

    @pytest.mark.cli_view_edge
    def test_add_term_all_defaults(self, controller):
        """Test adding term with all defaults."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "\n"
            "\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "successfully added" in user_out
        assert "already exists" not in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_not_found(self, controller):
        """Test editing term that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Fall 2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Term not found. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_no_edit_fields(self, controller):
        """Test editing term with no fields specified."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Fields available" in user_out
        assert "Fields to update" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_title_empty(self, controller):
        """Test editing term with empty new title."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "title\n"
            "\n"
            "Fall 2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Empty title not allowed. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_title_already_exists(self, controller):
        """Test editing term with title that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "A\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "E\n"
            "Spring 2025\n"
            "title\n"
            "Spring 2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "A term with this title already exists. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_empty(self, controller):
        """Test editing term with empty new start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date\n"
            "\n"
            "08-16-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_wrong_format(self, controller):
        """Test editing term with wrong start date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date\n"
            "invalid\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_after_end_date(self, controller):
        """Test editing term with start date after end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date\n"
            "08-01-2025\n"
            "02-02-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid date value. Cannot update start date." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_unchanged(self, controller):
        """Test editing term with unchanged start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date\n"
            "01-10-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Duration" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_end_date_empty(self, controller):
        """Test editing term with empty new end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "end date\n"
            "\n"
            "12-01-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_end_date_wrong_format(self, controller):
        """Test editing term with wrong end date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "end date\n"
            "invalid\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_end_date_before_start_date(self, controller):
        """Test editing term with end date before start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "end date\n"
            "01-01-2025\n"
            "02-03-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid date value. Cannot update end date." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_end_date_unchanged(self, controller):
        """Test editing term with unchanged end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "end date\n"
            "05-23-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Duration" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_end_date_combo(self, controller):
        """Test editing term with both start and end dates."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date, end date\n"
            "06-10-2025\n"
            "08-12-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Update results" in user_out
        assert "Duration" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_start_date_end_date_combo_unchanged(self, controller):
        """Test editing term with unchanged start and end dates."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "start date, end date\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Duration" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_active_empty(self, controller):
        """Test editing term with empty active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "active\n"
            "\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "No input" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_active_invalid(self, controller):
        """Test editing term with invalid active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "active\n"
            "maybe\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid boolean" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_term_new_active_unchanged(self, controller):
        """Test editing term with unchanged active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "E\n"
            "Spring 2025\n"
            "active\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Current" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_select_term_not_found(self, controller):
        """Test selecting term that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Fall 2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Term not found" in user_out
        assert "No selection made" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_term_not_found(self, controller):
        """Test removing term that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "A\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "R\n"
            "Spring 2026\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Term not found. No term was removed." in user_out

    @pytest.mark.cli_view_edge
    def test_remove_term_invalid_bool(self, controller):
        """Test removing term with invalid confirmation."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "A\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "R\n"
            "Spring 2025\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid response" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_term_not_confirmed(self, controller):
        """Test removing term when not confirmed."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "A\n"
            "Fall 2025\n"
            "08-02-2025\n"
            "12-11-2025\n"
            "no\n"
            "R\n"
            "Spring 2025\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        term_list = controller.term_list
        assert len(term_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Operation cancelled" in user_out
        assert "not removed" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_title_empty(self, controller):
        """Test adding course with empty title."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "Title cannot be empty" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_start_date_empty(self, controller):
        """Test adding course with empty start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "\n"
            "\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_start_date_wrong_format(self, controller):
        """Test adding course with wrong start date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "invalid\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_end_date_empty(self, controller):
        """Test adding course with empty end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_end_date_wrong_format(self, controller):
        """Test adding course with wrong end date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "invalid\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_end_date_before_start_date(self, controller):
        """Test adding course with end date before start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "12-01-2024\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "End date must be after start date. Please try again." in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_num_credits_empty(self, controller):
        """Test adding course with empty number of credits."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_num_credits_less_than_zero(self, controller):
        """Test adding course with negative number of credits."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "-5\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Invalid number of credits. Number of credits must be greater than or equal to 0. Please try again." in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_active_empty(self, controller):
        """Test adding course with empty active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_active_invalid(self, controller):
        """Test adding course with invalid active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the course you want to add" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_already_exists(self, controller):
        """Test adding course that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course with this title already exists" in user_out

    @pytest.mark.cli_view_edge
    def test_add_course_all_defaults(self, controller):
        """Test adding course with all defaults."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "successfully added" in user_out
        assert "course with this title already exists" not in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_not_found(self, controller):
        """Test editing course that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "CMPE 142\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Course not found. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_no_edit_fields(self, controller):
        """Test editing course with no fields specified."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Fields available" in user_out
        assert "Fields to update" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_title_empty(self, controller):
        """Test editing course with empty new title."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "title\n"
            "\n"
            "CMPE 142\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Empty title not allowed. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_title_already_exists(self, controller):
        """Test editing course with title that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "title\n"
            "ENGR 195A\n"
            "CMPE 142\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "A course with this title already exists. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_empty(self, controller):
        """Test editing course with empty new start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_wrong_format(self, controller):
        """Test editing course with wrong start date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date\n"
            "2025-01-10\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_after_end_date(self, controller):
        """Test editing course with start date after end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date\n"
            "05-23-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Invalid date value. Cannot update start date." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_unchanged(self, controller):
        """Test editing course with unchanged start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date\n"
            "01-02-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Duration" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_end_date_empty(self, controller):
        """Test editing course with empty new end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "end date\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_end_date_wrong_format(self, controller):
        """Test editing course with wrong end date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "end date\n"
            "2025-04-22\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_end_date_before_start_date(self, controller):
        """Test editing course with end date before start date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "end date\n"
            "11-08-2024\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Invalid date value. Cannot update end date." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_end_date_unchanged(self, controller):
        """Test editing course with unchanged end date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "end date\n"
            "05-12-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_end_date_combo(self, controller):
        """Test editing course with both start and end dates."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date, end date\n"
            "06-11-2025\n"
            "09-08-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_start_date_end_date_combo_unchanged(self, controller):
        """Test editing course with unchanged start and end dates."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "start date, end date\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_num_credits_empty(self, controller):
        """Test editing course with empty number of credits."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "number of credits\n"
            "\n"
            "1\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "No input" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_num_credits_less_than_zero(self, controller):
        """Test editing course with negative number of credits."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "number of credits\n"
            "-3\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Number of credits must be a valid integer. Cannot update number of credits." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_num_credits_unchanged(self, controller):
        """Test editing course with unchanged number of credits."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "number of credits\n"
            "3\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_active_empty(self, controller):
        """Test editing course with empty active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "active\n"
            "\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_active_invalid(self, controller):
        """Test editing course with invalid active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "active\n"
            "maybe\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out
        assert "Invalid boolean value. Cannot update active flag." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_course_new_active_unchanged(self, controller):
        """Test editing course with unchanged active flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "E\n"
            "ENGR 195A\n"
            "active\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_select_course_not_found(self, controller):
        """Test selecting course that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "CMPE 142\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to select" in user_out
        assert "Course not found" in user_out
        assert "No selection made" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_course_not_found(self, controller):
        """Test removing course that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "A\n"
            "CMPE 152\n"
            "Compiler Design\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "2\n"
            "yes\n"
            "R\n"
            "CMPE 142\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to remove" in user_out
        assert "Course not found. No Course was removed." in user_out

    @pytest.mark.cli_view_edge
    def test_remove_course_invalid_bool(self, controller):
        """Test removing course with invalid confirmation."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "A\n"
            "CMPE 152\n"
            "Compiler Design\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "2\n"
            "yes\n"
            "R\n"
            "ENGR 195A\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to remove" in user_out
        assert "Invalid response" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_course_not_confirmed(self, controller):
        """Test removing course when not confirmed."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "A\n"
            "CMPE 152\n"
            "Compiler Design\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "2\n"
            "yes\n"
            "R\n"
            "ENGR 195A\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        course_controller = controller.course_controller

        course_list = course_controller.get_course_list()
        assert len(course_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "course you want to remove" in user_out
        assert "Operation cancelled" in user_out
        assert "not removed" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_title_empty(self, controller):
        """Test adding assignment with empty title."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Title cannot be empty" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_category_empty(self, controller):
        """Test adding assignment with empty category."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid category" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_category_invalid(self, controller):
        """Test adding assignment with invalid category."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Quizzes\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Category must be in grade weights" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_due_date_empty(self, controller):
        """Test adding assignment with empty due date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "No input provided, using default value." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_due_date_wrong_format(self, controller):
        """Test adding assignment with wrong due date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "2-12-2025\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid date format. Please use MM-DD-YYYY." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_completed_empty(self, controller):
        """Test adding assignment with empty completed flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_completed_invalid(self, controller):
        """Test adding assignment with invalid completed flag."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "maybe\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_completed_false(self, controller):
        """Test adding assignment with completed set to false."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert selected_assignment.title == "Homework 1"
        assert selected_assignment.description == ""
        assert selected_assignment.due_date == datetime(2025, 1, 30)
        assert selected_assignment.completed is False
        assert math.isclose(selected_assignment.grade, 0.0, abs_tol=1e-9)

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "successfully added" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_pct_invalid_low(self, controller):
        """Test adding assignment with percentage grade too low."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "-11.3\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" in user_out
        assert "must be from 0 to 150" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_pct_invalid_high(self, controller):
        """Test adding assignment with percentage grade too high."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "200.18\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" in user_out
        assert "must be from 0 to 150" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_pct_boundary_low(self, controller):
        """Test adding assignment with percentage grade at lower boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "0.0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" not in user_out
        assert "must be from 0 to 150" not in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_pct_boundary_high(self, controller):
        """Test adding assignment with percentage grade at upper boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "100.0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" not in user_out
        assert "must be from 0 to 150" not in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_invalid_low(self, controller):
        """Test adding assignment with points grade too low."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "-11/20\n"
            "17/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" in user_out
        assert "must be from 0 to 150" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_invalid_high(self, controller):
        """Test adding assignment with points grade too high."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "40/20\n"
            "17/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" in user_out
        assert "must be from 0 to 150" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_boundary_low(self, controller):
        """Test adding assignment with points grade at lower boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "0/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" not in user_out
        assert "must be from 0 to 150" not in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_boundary_high(self, controller):
        """Test adding assignment with points grade at upper boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "20/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade" not in user_out
        assert "must be from 0 to 150" not in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_missing_dividend(self, controller):
        """Test adding assignment with points grade missing dividend."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_negative_divisor(self, controller):
        """Test adding assignment with points grade with negative divisor."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "20/-10\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_points_divide_by_zero(self, controller):
        """Test adding assignment with points grade dividing by zero."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "20/0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment you want to add" in user_out
        assert "Invalid grade input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_already_exists(self, controller):
        """Test adding assignment that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "already exists" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_all_defaults(self, controller):
        """Test adding assignment with all defaults."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "\n"
            "\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "successfully added" in user_out
        assert "already exists" not in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_not_found(self, controller):
        """Test editing assignment that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 3\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "Assignment not found" in user_out
        assert "Operation cancelled" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_no_edit_fields(self, controller):
        """Test editing assignment with no fields specified."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Fields available" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_title_empty(self, controller):
        """Test editing assignment with empty new title."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "title\n"
            "\n"
            "Homework 4\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Empty title not allowed. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_title_already_exists(self, controller):
        """Test editing assignment with title that already exists."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "title\n"
            "Homework 1\n"
            "Homework 4\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "An assignment with this title already exists. Cannot update title." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_category_empty(self, controller):
        """Test editing assignment with empty new category."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "category\n"
            "\n"
            "Midterm\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Invalid category. Category cannot be empty. Please try again." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_category_invalid(self, controller):
        """Test editing assignment with invalid new category."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "category\n"
            "Quizzes\n"
            "Midterm\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Invalid category. Category must be in grade weights. Cannot update category." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_category_unchanged(self, controller):
        """Test editing assignment with unchanged category."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "category\n"
            "Homework\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_due_date_empty(self, controller):
        """Test editing assignment with empty new due date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "due date\n"
            "\n"
            "02-15-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Due date is empty. Using default date." in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_due_date_wrong_format(self, controller):
        """Test editing assignment with wrong due date format."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "due date\n"
            "1-10-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out

    @pytest.mark.cli_view_edge
    def test_edit_assignment_new_due_date_unchanged(self, controller):
        """Test editing assignment with unchanged due date."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "E\n"
            "Homework 1\n"
            "due date\n"
            "01-30-2025\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to edit" in user_out
        assert "Due Date" in user_out
        assert "(unchanged)" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_assignment_not_found(self, controller):
        """Test removing assignment that doesn't exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "Linked lists\n"
            "Homework\n"
            "02-03-2025\n"
            "no\n"
            "0.0\n"
            "R\n"
            "Homework 8\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 2

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to remove" in user_out
        assert "Assignment not found" in user_out
        assert "Operation cancelled" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_assignment_invalid_bool(self, controller):
        """Test removing assignment with invalid confirmation."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "Linked lists\n"
            "Homework\n"
            "02-03-2025\n"
            "no\n"
            "0.0\n"
            "R\n"
            "Homework 1\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment you want to remove" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_pct_invalid_low(self, controller):
        """Test adding assignment grade with percentage too low."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "-10.2\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade. Grade must be in range 0 to 150. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_pct_invalid_high(self, controller):
        """Test adding assignment grade with percentage too high."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "200.0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade. Grade must be in range 0 to 150. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_pct_boundary_low(self, controller):
        """Test adding assignment grade at lower boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "0.0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 0.0, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 90.5 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_pct_boundary_high(self, controller):
        """Test adding assignment grade at upper boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "150.0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 150.0, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 90.5 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_invalid_low(self, controller):
        """Test adding assignment grade with points too low."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "-5/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade. Grade must be in range 0 to 150. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_invalid_high(self, controller):
        """Test adding assignment grade with points too high."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "40/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade. Grade must be in range 0 to 150. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_boundary_low(self, controller):
        """Test adding assignment grade with points at lower boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "0/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 0.0, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 90.5 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_boundary_high(self, controller):
        """Test adding assignment grade with points at upper boundary."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "30/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 150.0, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "for the assignment grade you want to add" in user_out
        assert "Grade 90.5 added to assignment 'Homework 1'." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_missing_dividend(self, controller):
        """Test adding assignment grade with points missing dividend."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "/20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade input" in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_negative_divisor(self, controller):
        """Test adding assignment grade with points negative divisor."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "16/-20\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade. Grade must be in range 0 to 150. Operation cancelled." in user_out

    @pytest.mark.cli_view_edge
    def test_add_assignment_grade_points_divide_by_zero(self, controller):
        """Test adding assignment grade with points dividing by zero."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "G\n"
            "Homework 1\n"
            "20/0\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "for the assignment grade you want to add" in user_out
        assert "Invalid grade input" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_assignment_grade_not_found(self, controller):
        """Test removing assignment grade from non-existent assignment."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "M\n"
            "Homework 8\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 90.5, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment grade you want to remove" in user_out
        assert "Assignment not found" in user_out
        assert "Operation cancelled" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_assignment_grade_invalid_bool(self, controller):
        """Test removing assignment grade with invalid confirmation."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "M\n"
            "Homework 1\n"
            "maybe\n"
            "yes\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 0.0, abs_tol=1e-9)
        assert selected_assignment.completed is False

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment grade you want to remove" in user_out
        assert "Invalid input" in user_out

    @pytest.mark.cli_view_edge
    def test_remove_assignment_grade_not_confirmed(self, controller):
        """Test removing assignment grade when not confirmed."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "M\n"
            "Homework 1\n"
            "no\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 1

        selected_assignment = assignment_controller.find_assignment("Homework 1")
        assert math.isclose(selected_assignment.grade, 90.5, abs_tol=1e-9)
        assert selected_assignment.completed is True

        user_out = output_stream.getvalue()
        assert "Welcome to ACDMC!" in user_out
        assert "assignment grade you want to remove" in user_out
        assert "Operation cancelled" in user_out
        assert "not removed" in user_out

    @pytest.mark.cli_view_edge
    def test_view_assignments_all_empty(self, controller):
        """Test viewing all assignments when none exist."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "V\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 0

        user_out = output_stream.getvalue()
        assert "Invalid selection" in user_out

    @pytest.mark.cli_view_edge
    def test_view_assignments_completed_empty(self, controller):
        """Test viewing completed assignments when none are completed."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "no\n"
            "0.0\n"
            "V\n"
            "C\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "would you like to view" in user_out
        assert "No completed assignments to display" in user_out

    @pytest.mark.cli_view_edge
    def test_view_assignments_incomplete_empty(self, controller):
        """Test viewing incomplete assignments when none are incomplete."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "yes\n"
            "90.5\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "yes\n"
            "76.4\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "yes\n"
            "88.24\n"
            "V\n"
            "I\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "would you like to view" in user_out
        assert "No incomplete assignments to display" in user_out

    @pytest.mark.cli_view_edge
    def test_view_assignments_invalid_selection(self, controller):
        """Test viewing assignments with invalid selection."""
        input_stream = io.StringIO(
            "A\n"
            "Spring 2025\n"
            "01-10-2025\n"
            "05-23-2025\n"
            "yes\n"
            "S\n"
            "Spring 2025\n"
            "A\n"
            "ENGR 195A\n"
            "\n"
            "01-02-2025\n"
            "05-12-2025\n"
            "3\n"
            "yes\n"
            "S\n"
            "ENGR 195A\n"
            "A\n"
            "Homework 1\n"
            "\n"
            "Homework\n"
            "01-30-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 2\n"
            "\n"
            "Homework\n"
            "02-05-2025\n"
            "no\n"
            "0.0\n"
            "A\n"
            "Homework 3\n"
            "\n"
            "Homework\n"
            "02-13-2025\n"
            "yes\n"
            "88.24\n"
            "V\n"
            "W\n"
            "X\n"
            "X\n"
            "X\n"
            "X\n"
        )
        output_stream = io.StringIO()

        view = CliView(controller, input_stream, output_stream)
        view.run()
        assignment_controller = controller.course_controller.assignment_controller

        assignment_list = assignment_controller.get_assignment_list()
        assert len(assignment_list) == 3

        user_out = output_stream.getvalue()
        assert "would you like to view" in user_out
        assert "Invalid selection" in user_out
