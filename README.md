# User Service

## Description

The User Service is a microservice that handles user-related information, including registration, login, profile management, and preferences. It is built using FastAPI and follows a REST MVC (Model-View-Controller) architecture.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Advanced Topics](#advanced-topics)
  - [Using a Makefile](#using-a-makefile)
  - [Using Docker](#using-docker)
  - [Environment Variables](#environment-variables)
  - [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Getting Started

This section will guide you through setting up and running the project.

### Prerequisites

- Python 3.8 or higher (Download from [python.org](https://www.python.org/downloads/))
- pip (usually comes bundled with Python)
- Git (for cloning the repository)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/user-service.git
   cd user-service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
user-service/
├── env                 # Environment variables (create this file)
├── .gitignore          # Git ignore file
├── requirements.txt    # Project dependencies
├── README.md           # This file
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py     # FastAPI application entry point
│       ├── config/     # Configuration files
│       ├── controllers/# Request handlers
│       ├── models/     # Database models
│       ├── repositories/# Data access layer
│       ├── services/   # Business logic
│       └── utils/      # Utility functions
└── tests/
    └── test_*.py       # Test files
```

## Running the Project

1. Ensure you're in the project root directory and your virtual environment is activated.

2. Set up virtual environment.

3. Run the FastAPI application:
   ```bash
   uvicorn src.api.main:app --reload
   ```

4. Open your browser and navigate to `http://localhost:8000` to see the API documentation.

## API Documentation

Once the application is running, you can access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

These pages provide detailed information about each endpoint, including request/response schemas and the ability to try out the API directly.

## Testing

To run the tests:

```bash
pytest tests
```

For more verbose output:

```bash
pytest tests -v
```

## Advanced Topics

### Using a Makefile

A `Makefile` is provided to simplify common tasks. Here are some available commands:

- `make install`: Install project dependencies
- `make run`: Start the FastAPI server
- `make test`: Run tests
- `make lint`: Run linters (flake8, black, isort)

Run `make help` to see all available commands.

### Using Docker

A `Dockerfile` and `docker-compose.yml` are provided for containerization.

To build and run the service using Docker:

```bash
docker-compose up --build
```

This will start the User Service and any required services (e.g., database) defined in the `docker-compose.yml` file.

### Environment Variables

The following environment variables can be set in the `.env` file:

- `DATABASE_URL`: Connection string for the database
- `SECRET_KEY`: Secret key for JWT token generation
- `DEBUG`: Set to `True` for development, `False` for production

### Deployment

For production deployment:

1. Set `DEBUG=False` in your `.env` file
2. Use a production-grade ASGI server like Gunicorn:
   ```bash
   gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
3. Set up a reverse proxy (e.g., Nginx) to handle incoming requests

## Troubleshooting

- **ImportError**: Make sure you're running the application from the project root directory and that your virtual environment is activated.
- **Database connection issues**: Check that your database is running and that the `DATABASE_URL` in your `.env` file is correct.
- **Permission denied**: Ensure you have the necessary permissions to read/write in the project directory and to the database.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/CZN-{##}`)
3. Commit your changes (`git commit -m 'CZN-## : Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/CZN-{##}`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the project's code style.
