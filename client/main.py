"""Main entry point for the acdmc client."""

from controllers.term_controller import TermController
from views.cli_view import CliView


def main() -> None:
    """Function that instantiates the entry point for the acdmc client."""
    controller = TermController()
    view = CliView(controller)
    view.run()


if __name__ == "__main__":
    main()
