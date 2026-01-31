# FastAPI Authentication Project

This project is a FastAPI-based backend service with JWT authentication, refresh-token rotation, and database migrations managed using Alembic.

---

## 🚀 Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM
- **PostgreSQL** – Database
- **Alembic** – Database migrations
- **JWT** – Authentication (Access & Refresh tokens)
- **Uvicorn** – ASGI server

Python 3.12.4
---

## 📂 Project Structure

```
app/
├── api/
│   └── v1/
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
├── schemas/
├── services/
├── utils/
└── main.py
```

---

## ⚙️ Setup & Installation

### 1️⃣ Create Virtual Environment

```bash
python -m venv env
```

### 2️⃣ Activate Virtual Environment

**Ubuntu/MacOS:**
```bash
source env/bin/activate
```

**Windows:**
```bash
env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Ensure PostgreSQL is running and configure your database credentials in:

Need to add .env in the the outside the app inside the main folder
ex

SECRET_KEY = 
DATABASE_URL=
DEBUG =
BACKEND_CORS_ORIGINS =
ALGORITHM  =
ACCESS_TOKEN_EXPIRE_MINUTES  =
REFRESH_TOKEN_EXPIRE_DAYS  =

```
app/core/config.py
```

---

## 🔄 Database Migrations (Alembic)

### Create a New Migration

```bash
alembic revision --autogenerate -m "your_migration_message"
```

This command:
- Detects model changes
- Generates a new migration file automatically

### Apply Migrations

```bash
alembic upgrade head
```

This applies all pending migrations to the database.

### Downgrade Migrations

```bash
alembic downgrade -1
```

---

## ▶️ Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

**Access the application:**
- App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Authentication Flow

### Login
- Generates access & refresh tokens
- Stores them as HTTP-only cookies

### Refresh
- Rotates refresh token
- Issues new access token

### Logout
- Revokes refresh token
- Deletes cookies

---

## 🧪 Common Commands

| Purpose | Command |
|---------|---------|
| Run server | `uvicorn app.main:app --reload` |
| Create migration | `alembic revision --autogenerate -m "message"` |
| Apply migration | `alembic upgrade head` |
| Downgrade | `alembic downgrade -1` |

---

## 📝 Notes

- Refresh tokens are stored in the database for revocation & rotation
- Access tokens are short-lived
- Refresh tokens are rotated on every refresh
