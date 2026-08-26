acdmc/
├── server/                       # Thin API server (database abstraction)
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Configuration settings
│   ├── dependencies.py           # Dependency injection
│   ├── routes/                   # Simple CRUD endpoints
│   │   ├── __init__.py
│   │   ├── terms.py              # CRUD operations for terms
│   │   ├── courses.py            # CRUD operations for courses
│   │   └── assignments.py        # CRUD operations for assignments
│   ├── models/                   # SQLAlchemy ORM models (database schema)
│   │   ├── __init__.py
│   │   ├── base.py               # Base model with common fields
│   │   ├── term.py
│   │   ├── course.py
│   │   └── assignment.py
│   ├── schemas/                  # Pydantic schemas (request/response validation)
│   │   ├── __init__.py
│   │   ├── term.py
│   │   ├── course.py
│   │   └── assignment.py
│   ├── database/                 # Database configuration
│   │   ├── __init__.py
│   │   ├── connection.py         # Database session management
│   │   ├── migrations/           # Alembic migrations
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   └── seed.py               # Seed data for development
│   └── middleware/               # Custom middleware (auth, logging, etc.)
│       └── __init__.py
│
├── client/                       # Fat client with business logic
│   ├── __init__.py
│   ├── main.py                   # Tkinter app entry point
│   ├── controllers/              # MVC Controllers (business logic)
│   │   ├── __init__.py
│   │   ├── term_controller.py    # Port of C++ TermController
│   │   ├── course_controller.py  # Port of C++ CourseController
│   │   └── assignment_controller.py  # Port of C++ AssignmentController
│   ├── models/                   # MVC Models (client-side data structures)
│   │   ├── __init__.py
│   │   ├── term.py               # Client-side Term model
│   │   ├── course.py             # Client-side Course model
│   │   └── assignment.py         # Client-side Assignment model
│   ├── views/                    # MVC Views (Tkinter GUI)
│   │   ├── __init__.py
│   │   ├── main_window.py        # Main application window
│   │   ├── term_view.py          # Term management view
│   │   ├── course_view.py        # Course management view
│   │   ├── assignment_view.py    # Assignment detail view
│   │   └── form_dialog.py        # Generic form dialog
│   ├── widgets/                  # Custom Tkinter widgets
│   │   ├── __init__.py
│   │   ├── grade_input.py        # Grade input widget
│   │   └── date_picker.py        # Date selection widget
│   ├── api_client.py             # HTTP client for server communication
│   └── utils/                    # Shared utilities (port of C++ utils)
│       ├── __init__.py
│       ├── grade_calculations.py # Grade calculation logic
│       ├── date_utils.py         # Date parsing/formatting
│       ├── validation.py         # Input validation
│       └── uuid_utils.py         # UUID generation
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── client/
│   │   │   ├── test_controllers.py
│   │   │   ├── test_models.py
│   │   │   └── test_utils.py
│   │   └── server/
│   │       ├── test_routes.py
│   │       ├── test_models.py
│   │       └── test_schemas.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_client_server.py
│   │   └── test_database.py
│   └── conftest.py               # Pytest configuration
│
├── scripts/                      # Utility scripts
│   ├── init_db.py                # Initialize database
│   ├── migrate_data.py           # Migrate data from C++ version
│   ├── seed_data.py              # Seed development data
│   └── run_server.py             # Convenience script to run server
│
├── docker/                       # Docker configurations
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   └── docker-compose.yml
│
├── docs/                         # Documentation
│   ├── api.md                    # API documentation
│   ├── architecture.md           # Architecture decisions
│   ├── migration_guide.md        # Migration from C++ guide
│   └── future_proofing.md        # Guide for moving logic to server
│
├── .env.example                  # Environment variables template
├── .gitignore
├── pyproject.toml                # Python project configuration (uv)
├── uv.lock                       # Lock file for deterministic builds
├── README.md
└── LICENSE