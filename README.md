# GeoSnap Developer Documentation

## 1. Project Overview

**GeoSnap** is a Python-based backend service built with FastAPI. Its primary purpose is to provide a robust, scalable RESTful API for location-based services. It handles user authentication, location data storage (create, read, search), and advanced geospatial queries like finding points of interest within a specific radius.

The entire application is containerized with Docker, ensuring a consistent and easy-to-manage development and deployment environment.

## 2. Technology Stack

The project utilizes a modern and efficient technology stack:

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Web Framework** | **FastAPI** | For building the high-performance API endpoints and handling data validation. |
| **Web Server** | **Uvicorn** | The ASGI server that runs the FastAPI application. |
| **Database** | **PostgreSQL + PostGIS**| A powerful relational database with the PostGIS extension for storing and querying geospatial data. |
| **ORM** | **SQLAlchemy** | For interacting with the database using Python objects instead of raw SQL. |
| **Database Migrations**| **Alembic** | For managing and applying changes to the database schema as the models evolve. |
| **Authentication** | **JWT & Passlib** | For securing endpoints with JSON Web Tokens and hashing passwords. |
| **Containerization**| **Docker & Docker Compose**| For creating a reproducible environment and orchestrating the `web`, `db`, and `redis` services. |
| **Data Caching** | **Redis** | For high-speed, in-memory caching (can be used to speed up frequent queries). |

## 3. First-Time Setup & Installation

Follow these steps to get the project running on your local machine.

#### Prerequisites
*   Git
*   Docker
*   Docker Compose

#### Step-by-Step Guide

1.  **Clone the Repository (If you haven't already)**
    ```bash
    git clone <your-repository-url>
    cd GeoSnap
    ```

2.  **Create the Environment Configuration File**
    The project uses an `.env` file to manage sensitive information and environment-specific settings. The `docker-compose.yml` file is already configured to read from it. Create a file named `.env` in the project root.
    ```bash
    touch .env
    ```
    Now, copy the contents from `.env.example` (if it exists) or use the following template. **These values must match the ones in your `docker-compose.yml` file.**

    ```dotenv
    # .env

    # PostgreSQL Database
    DATABASE_URL=postgresql://geo_user:geo_pass@db:5432/geo_db

    # JWT Authentication
    SECRET_KEY=your_super_secret_key_that_should_be_long_and_random
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    *Note: The `DATABASE_URL` uses the service name `db` as the host because the containers communicate with each other over Docker's internal network.*

3.  **Build and Run the Services**
    This single command will build the Docker image for the `web` service (as defined in your `Dockerfile`) and start all the services (`web`, `db`, `redis`).

    ```bash
    docker-compose up --build
    ```
    You should see logs from all services. Once you see the Uvicorn message `Application startup complete`, the API is ready.

4.  **Access the API**
    *   **API URL:** `http://localhost:8000`
    *   **Interactive Docs (Swagger UI):** `http://localhost:8000/docs`

## 4. Key Developer Workflows

### How to Test Endpoints
The fastest way to test is using the **Swagger UI** at `http://localhost:8000/docs`.

1.  **Register a User:** Use the `POST /auth/register` endpoint first to create an account.
2.  **Authorize:** Click the green "Authorize" button at the top right. Enter the username and password you just registered. This will store the JWT token in your browser session for future requests on this page.
3.  **Execute Protected Endpoints:** Now you can use endpoints like `POST /autosnap/create`. The Swagger UI will automatically add the `Authorization` header to your requests.

### How to Add a New API Endpoint

1.  **Define the Route:** Open the relevant route file (e.g., `app/autosnap.py`). Add a new function with a FastAPI decorator (e.g., `@router.get("/new-route")`).
2.  **Create Pydantic Models (if needed):** In `app/models.py` or a dedicated `app/schemas.py`, define the Pydantic models for your request body and response. This gives you automatic data validation.
3.  **Implement the Logic:** Write the function that handles the request, interacts with the database (via SQLAlchemy), and returns the result.
4.  **Restart the Server:** The Uvicorn reloader should detect the file change and restart automatically. If not, you can restart Docker Compose with `Ctrl+C` and `docker-compose up`.

### How to Work with the Database (Migrations)

When you change a SQLAlchemy model (e.g., add a new column in `app/models.py`), you **must** create a database migration to apply that change to the live database schema. This project uses **Alembic** for that.

**Never modify the database directly.** Always use migrations.

1.  **Make a change** to your models in `app/models.py`. For example, add a `description` field to your `Location` model.

2.  **Open a new terminal.** You need to run the Alembic command *inside* the running `web` container.

3.  **Generate the Migration Script:**
    ```bash
    docker-compose exec web alembic revision --autogenerate -m "Add description to Location model"
    ```
    This will create a new file in the `alembic/versions/` directory containing the Python code to alter your database table.

4.  **Apply the Migration:**
    ```bash
    docker-compose exec web alembic upgrade head
    ```
    This command runs the migration script, safely updating your PostgreSQL database schema to match your models.

## 5. Project Structure Explained

```
GeoSnap/
│
├── .env                  # Your local environment variables (you created this)
├── alembic.ini           # Alembic configuration file.
├── alembic/              # Directory for database migrations.
│   └── versions/         # Auto-generated migration scripts live here.
│
├── app/                  # The main application source code.
│   ├── __init__.py
│   ├── main.py           # FastAPI app entrypoint, brings all routers together.
│   ├── autosnap.py       # Core routes for location management (/create, /search).
│   ├── auth.py           # Routes and logic for user authentication (/register, /login).
│   ├── db.py             # Database session management and setup.
│   └── models.py         # Contains SQLAlchemy models (database table structure) and Pydantic schemas (API data shapes).
│
├── docker-compose.yml    # Orchestrates all services (web, db, redis).
├── Dockerfile            # Instructions to build the Docker image for the 'web' service.
├── requirements.txt      # List of Python dependencies.
└── ...                   # Other folders like tests/, etc.
```

## 6. Shutting Down the Application

To stop all running services, simply press `Ctrl+C` in the terminal where `docker-compose` is running.

To stop and remove the containers, run:
```bash
docker-compose down
```Use `docker-compose down -v` to also remove the database volume if you want a completely clean slate.

---