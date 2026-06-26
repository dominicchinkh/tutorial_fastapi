project/
├── .env                  # Environment variables (secret)
├── .gitignore
├── README.md
├── requirements.txt      # Or pyproject.toml / Pipfile
└── app/
    ├── __init__.py
    ├── main.py           # App initialization and FastAPI instance
    ├── config.py         # Pydantic settings management
    ├── database.py       # SQLAlchemy/Tortoise connection & session setup
    ├── dependencies.py   # Global dependencies (e.g., current_user, get_db)
    ├── crud/             # Database queries / Business logic
    │   ├── __init__.py
    │   ├── user.py
    │   └── item.py
    ├── exception/        # Exception
    │   ├── __init__.py
    ├── internal/         # Admin or private routes
    │   ├── __init__.py
    │   └── admin.py
    ├── models/           # Database ORM models (e.g., SQLAlchemy)
    │   ├── __init__.py
    │   ├── user.py
    │   └── item.py
    ├── routers/          # API endpoints split by resource
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── users.py
    │   └── items.py
    └── schemas/          # Pydantic data validation schemas
        ├── __init__.py
        ├── user.py
        └── item.py
