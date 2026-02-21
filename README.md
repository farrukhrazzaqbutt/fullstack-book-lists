# Fullstack Book Lists

A full-stack web application for managing book lists. The **webapp** (Angular frontend) runs in the browser and talks to a Django REST API. You can view all books, create named lists, and add or remove books from each list.

## Tech Stack

- **Webapp (frontend):** Angular 21, standalone components, Angular SSR
- **Backend:** Django 6, Django REST Framework, SQLite
- **Tooling:** ESLint (Angular), Ruff (Python)

---

## How to install, run, lint and test the webapp

### Install

**1. Backend (API the webapp depends on)**

- **Prerequisites:** Python 3.10+

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_books   # optional: load sample books
```

**2. Webapp (frontend)**

- **Prerequisites:** Node.js v20+ and npm

```bash
cd frontend/book-lists
npm install
```

### Run

**1. Start the backend API** (from repo root):

```bash
cd backend
venv\Scripts\activate          # Windows (or source venv/bin/activate on macOS/Linux)
python manage.py runserver
```

API: **http://127.0.0.1:8000/api/**

**2. Start the webapp** (in a second terminal):

```bash
cd frontend/book-lists
npm start
```

Webapp: **http://localhost:4200/**

Open the webapp URL in a browser. Keep the backend running so the webapp can load books and lists.

### Lint

Lint the webapp (Angular/TypeScript and templates):

```bash
cd frontend/book-lists
npm run lint
```

Optional: auto-fix what can be fixed:

```bash
npm run lint -- --fix
```

### Test

**Webapp:** The project uses `npm run lint` for the frontend (no separate unit test script in package.json). To run the backend unit tests (which cover the API used by the webapp):

```bash
cd backend
python manage.py test api
```

---

## Project structure

```
fullstack-book-lists/
├── frontend/book-lists/    # Angular webapp
│   └── src/app/            # Components, services, routes
├── backend/                # Django API
│   ├── api/                # Models, views, serializers, tests
│   ├── config/             # Settings, root URLs
│   └── requirements.txt
└── README.md
```

## Features

- **Books:** Browse all books (title, year, author).
- **Lists:** Create and delete named book lists.
- **List detail:** View books in a list, add books from a dropdown, remove books from the list.

## API overview

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

## Notes

- Backend CORS allows `http://localhost:4200`.
- Webapp API base URL: `http://127.0.0.1:8000/api` (see `frontend/book-lists/src/app/api.service.ts`).
- Database: SQLite at `backend/db.sqlite3`.
