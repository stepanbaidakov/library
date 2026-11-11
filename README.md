# Library API

## Description

A Django REST Framework API for managing a library, including books, authors, users, and book loans.

The application allows users to manage library resources, track book borrowing and returns, check book availability, and receive automated reminders.

## Features

- **JWT Authentication** — user registration and authentication using JSON Web Tokens.
- **Book Management** — manage books available in the library.
- **Author Management** — manage author information.
- **User Management** — manage user accounts.
- **Book Borrowing** — track books borrowed by users.
- **Return Tracking** — monitor the return status of borrowed books.
- **Book Availability** — check whether books are available for borrowing.
- **Automated Reminders** — send reminders to users regarding borrowed books.
- **API Documentation** — interactive API documentation based on the OpenAPI standard.

## Tech Stack

- Python
- Django
- Django REST Framework
- JWT Authentication
- OpenAPI
- Docker
- Docker Compose
- Celery beat/worker
- GitHub Actions

## Local Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/stepanbaidakov/library.git
```

### 2. Navigate to the project directory

```bash
cd library
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file based on the `.env.sample` template.

```bash
cp .env.sample .env
```

On Windows, copy the template manually if the `cp` command is unavailable.

Configure the required environment variables, including the Django secret key, database credentials, Redis connection settings and Email backend and other config settings.

Example:

```dotenv
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=library
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

BACKEND=
LOCATION=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
DOCKER_HUB_USERNAME=
```

Use secure values and set `DEBUG=False` in production.

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Create a superuser

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

The development server will be available at:

```text
http://127.0.0.1:8000/
```

## Running with Docker

### 1. Configure environment variables

Create a `.env` file based on `.env.sample` and configure the required settings for the application and its services.

### 2. Pull  and start the application

```bash
docker compose pull web worker beat nginx
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py collectstatic --noinput
docker compose up -d web worker beat nginx
```

### 5. Check the running containers

```bash
docker compose ps
```

View application logs if necessary:

```bash
docker compose logs -f
```

To view logs for a specific service:

```bash
docker compose logs -f web
```

### 6. Stop the application

```bash
docker compose down
```

This stops and removes the Compose containers and network without automatically deleting named volumes.

## Usage

### User Registration and Authentication

Users can register and authenticate using the API endpoints provided by the application. Authentication is based on JWT tokens.

Authenticated requests must include the appropriate access token according to the API's authentication configuration.

### Managing Books and Authors

The API provides endpoints for managing books and authors. Available operations depend on the configured views, serializers, and permissions.

### Managing Users

User management functionality is available through the API, subject to the application's authentication and permission rules.

### Borrowing and Returning Books

The application tracks book loans and their return status, allowing clients to monitor borrowed books and check availability.

### Automated Reminders

The application supports automated reminders for users. Reminder delivery requires the relevant Redis connection and background task configuration used by the project.

## API Documentation

The API documentation follows the OpenAPI standard.

Depending on the application's URL configuration, interactive documentation may be available through Swagger UI and ReDoc.

- **Swagger UI:** `/swagger/`
- **ReDoc:** `/redoc/`

These are example paths. Use the actual documentation URLs configured in the project's Django URL configuration.

## CI/CD

The GitHub Actions workflows are located in:

```text
.github/workflows/
```

### GitHub Actions Secrets

Navigate to:

**Settings → Secrets and variables → Actions**

Add the secrets required by the configured workflow:

```text
DOCKER_HUB_ACCESS_TOKEN
DOCKER_HUB_USERNAME
SERVER_IP
SERVER_USER
SERVER_SSH_KEY
SECRET_KEY
```

### Deployment Workflow

When changes are pushed to the configured branch, the workflow may perform the following steps, depending on its implementation:

1. Check out the source code.
2. Install dependencies.
3. Run automated tests.
4. Build Docker images.
5. Push images to a container registry.
6. Connect to the deployment server via SSH.
7. Pull updated images and restart the application.

## Deployment

The deployment server must have the following software installed:

- Docker Engine
- Docker Compose plugin

Verify the installation:

```bash
docker --version
docker compose version
```

### 1. Copy the Docker Compose file

Copy `docker-compose.yml` to the deployment server.

### 2. Configure environment variables

Create a `.env` file containing the production environment variables required by the application and Docker Compose.

```bash
nano .env
```

Configure database credentials, Django settings, service connection details, and image tags as required by the deployment.

Do not commit production secrets to the repository.

### 3. Pull and start the application

Deploy the images with:

```bash
docker compose pull
docker compose up -d
```


### 4. Verify the deployment

Check container status:

```bash
docker compose ps
```

Inspect logs:

```bash
docker compose logs -f
```

After changes are pushed to the configured branch, the CI/CD workflow can deploy updates automatically.
