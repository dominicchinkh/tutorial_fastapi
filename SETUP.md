# Project Setup Guide

This guide walks you through setting up a local Python virtual environment and installing the required dependencies for this project.

## ⚙️ Prerequisites

Before you begin, ensure you have Python 3 installed on your system. You can verify your Python version by running:

```bash
python3 --version
```

## 🚀 Setup Instructions

Follow these three steps to get your environment ready:

### 1. Create the Environment

Utilize Python's built-in `venv` module to create an isolated virtual environment. This prevents dependency conflicts with other projects on your system.

```bash
python3 -m venv .venv
```

### 2. Activate the Environment

You must activate the virtual environment before installing packages. Run the following command in your terminal:

```bash
source .venv/bin/activate
```

💡 Tip: Once activated, your terminal prompt will be prefixed with `(.venv)`, indicating that any subsequent Python or pip commands will run strictly within this isolated environment.

### 3. Install Dependencies

With the environment activated, install the libraries using pip:

```bash
pip install "fastapi[standard]"
```

## 🏃‍♂️ Run the Application

Once the dependencies are installed, you can run the server by running:

```bash
fastapi dev
```

## Interactive API docs

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

And now, go to http://127.0.0.1:8000/redoc.

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc)):

If you are curious about what the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.

You can see it directly at: http://127.0.0.1:8000/openapi.json.

## 🛑 Deactivating the Environment

When you are finished working on the project and want to return to your global system Python environment, simply run:

```bash
deactivate
```