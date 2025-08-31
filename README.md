# AI-Powered Content Moderation System

A content moderation system using Django, PostgreSQL, Celery, and OpenAI's Moderation API.

## Features

- Content submission API
- Asynchronous content moderation using OpenAI
- Admin dashboard for content review
- Docker-based deployment
- Comprehensive test coverage

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Setup

1. Clone the repository
2. Copy `.env.sample` to `.env` and fill in your environment variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   DATABASE_URL=postgres://postgres:postgres@db:5432/moderation
   REDIS_URL=redis://redis:6379/0
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Run migrations:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## Usage

- API endpoint for content submission: `POST /api/content/`
- Admin interface: `http://localhost:8000/admin`
- API documentation: `http://localhost:8000/api/docs/`

## Testing

Run tests with:
```bash
docker-compose exec backend pytest
```

Run tests with coverage report:
```bash
docker-compose exec backend pytest --cov=. --cov-report=term-missing
```

The test suite includes:
- Model tests
- API endpoint tests
- Celery task tests
- Admin interface tests

## Architecture

- Django: Web framework and admin interface
- PostgreSQL: Main database
- Redis: Message broker for Celery
- Celery: Asynchronous task processing
- OpenAI: Content moderation API
- Docker: Containerization 
