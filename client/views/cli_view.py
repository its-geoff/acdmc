# Standard library imports
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

# Local imports
from controllers.term_controller import TermController
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
        """Return whether any term field was requested for edit.
        
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
    

class CliView:
    """Class that handles I/O and user interaction for the command line interface."""

    