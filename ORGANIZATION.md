project/
├── .env                  # Environment variables (secret)
├── .gitignore
├── README.md
├── requirements.txt      # Or pyproject.toml / Pipfile
├── app/
│   ├── __init__.py
│   ├── main.py           # App initialization and FastAPI instance
│   ├── config.py         # Pydantic settings management
│   ├── database.py       # SQLAlchemy/Tortoise connection & session setup
│   ├── dependencies.py   # Global dependencies (e.g., current_user, get_db)
│   ├── crud/             # Database queries / Business logic
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── exception/        # Exception
│   │   ├── __init__.py
│   ├── internal/         # Admin or private routes
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── middleware/       # Middleware
│   │   ├── __init__.py
│   ├── models/           # Database ORM models (e.g., SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── routers/          # API endpoints split by resource
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── items.py
│   │   └── users.py
│   ├── schemas/          # Pydantic data validation schemas
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   └── test/
│       ├── test_main.py
│       └── routers/
│           ├── test_auth.py
│           ├── test_items.py
│           └── test_users.py
├── dist/
│   └── index.html
├── dist/
│   └── 1011.jpg
