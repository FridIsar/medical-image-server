# Medical Image Server

## Overview

A simple web server for managing medical images with functionality to view DICOM volumes and interact with patient information. This project is developed using Test-Driven Development (TDD) principles.

## Technologies

- **Backend:** FastAPI, Python, SQLAlchemy, pydicom
- **Frontend:** SvelteKit, JavaScript
- **Testing:** pytest, Playwright
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Setup and Running

### Prerequisites

- Docker
- Docker Compose

### Environment Configuration

The application uses different environment configurations depending on the context:

1. **Local development** uses `localhost` URLs.
2. **Dockerized testing** uses Docker service names (e.g., `backend` and `frontend`) for communication.

You can find the environment variable files in the following locations:

- **`.env.local`**: for local development (`localhost`).
- **`.env.docker`**: for Dockerized environments (`backend`, `frontend`).

### Running the Project

To run the application, you can use one of the following commands depending on your use case:

---

### **1. Build and Run Backend Tests Only**

To build the backend and run the backend tests:

```bash
docker-compose build backend backend_tests && docker-compose run backend_tests
```

### **2. Frontend E2E Testing**

For Dockerized testing (using backend and frontend service names for internal communication):

```bash
docker-compose --env-file .env.docker build frontend backend frontend_tests && docker-compose --env-file .env.docker up --abort-on-container-exit frontend_tests && docker-compose down
```
This command will:

Build the frontend, backend, and frontend_tests.
Run the frontend tests using Playwright, and automatically shut down the services after tests complete.

### **3. Build and Run Frontend and Backend for Local Development**

For local development where the frontend communicates with the backend using localhost:

```bash
docker-compose --env-file .env.local build frontend backend && docker-compose --env-file .env.local up frontend backend
```

This command will:

- Build and run both the frontend and backend services.
- The frontend will be accessible at http://localhost:5173, and the backend at http://localhost:8000.

### **Accessing the application**
- Frontend: Visit http://localhost:5173/login for the frontend UI.
- Backend: The backend API can be accessed at http://localhost:8000/docs for interactive API documentation (via Swagger UI).