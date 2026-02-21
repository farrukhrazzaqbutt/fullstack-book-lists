# Fullstack Book Lists

A full-stack application for managing book lists. The frontend is an Angular SPA that talks to a Django REST API. You can view all books, create named lists, and add or remove books from each list.

## Tech Stack

- **Frontend:** Angular 21, standalone components, Angular SSR, Express (server)
- **Backend:** Django 6, Django REST Framework, SQLite
- **Tooling:** ESLint (Angular), Ruff (Python)

## Project Structure

```
fullstack-book-lists/
├── frontend/book-lists/    # Angular app
│   └── src/app/            # Components, services, routes
├── backend/                # Django project
│   ├── api/                # Books & lists app (models, views, serializers, tests)
│   ├── config/             # Django settings and root URLs
│   └── requirements.txt
└── README.md
```

## Features

- **Books:** Browse all books (title, year, author).
- **Lists:** Create and delete named book lists.
- **List detail:** View books in a list, add books from a dropdown, remove books from the list.

## Prerequisites

- **Node.js** (v20+) and **npm** for the frontend
- **Python** (3.10+) for the backend

## Backend Setup

1. Create and activate a virtual environment:

   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies and run migrations:

   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. (Optional) Seed sample books:

   ```bash
   python manage.py seed_books
   ```

4. Start the API server:

   ```bash
   python manage.py runserver
   ```

   API base URL: **http://127.0.0.1:8000/api/**

## Frontend Setup

1. Install dependencies and start the dev server:

   ```bash
   cd frontend/book-lists
   npm install
   npm start
   ```

   App URL: **http://localhost:4200/**

2. Ensure the backend is running so the app can load books and lists.

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books |
| GET | `/api/books/{id}/` | Get one book |
| GET | `/api/lists/` | List all book lists |
| POST | `/api/lists/` | Create a list (`{"name": "..."}`) |
| GET | `/api/lists/{id}/` | Get one list |
| DELETE | `/api/lists/{id}/` | Delete a list |
| GET | `/api/lists/{id}/books/` | List books in a list |
| POST | `/api/lists/{id}/books/` | Add book to list (`{"book_id": number}`) |
| DELETE | `/api/lists/{id}/books/{book_id}/` | Remove book from list |

## Running Tests

**Backend (Django):**

```bash
cd backend
python manage.py test api
```

**Frontend (lint):**

```bash
cd frontend/book-lists
npm run lint
```

## Development Notes

- Backend uses **CORS** with `http://localhost:4200` allowed.
- Frontend API base URL is set to `http://127.0.0.1:8000/api` in `ApiService`.
- Database is SQLite (`backend/db.sqlite3`).
