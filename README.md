# Property Manager

This is a FastAPI project for managing properties.

## Installation

1. Install Poetry:
    ```bash
    pip install poetry
    ```

2. Install dependencies:
    ```bash
    poetry install
    ```


3. Create an env file and customize variables
    ```bash
    cp .env.sample .env
    ```

## Running the app

```bash
docker-compose up -d

poetry run runserver

## Use Alembic to create migrations and update database model

alembic init alembic

# Create migration
alembic revision --autogenerate -m "New Migration"

# Apply migration 
alembic upgrade head

# downgrade migration 
alembic downgrade head

# Verify state of migrations 
alembic current
