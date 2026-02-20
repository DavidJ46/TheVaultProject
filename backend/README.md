
```markdown
# The Vault – Backend (Flask)

This folder contains the Flask backend for The Vault project.

---

## 🏗 Project Structure

```

backend/

├── app.py                # Flask app factory & blueprint registration

├── requirements.txt      # Python dependencies

├── init_db.py            # Database initialization script

│
├── config/               # App configuration

├── controllers/          # Route handlers (Flask Blueprints)

├── services/             # Business logic layer

├── models/               # Database models / schema

├── utils/                # Helpers (DB connection, security, etc.)

└── tests/                # Backend tests

```

---

## Environment Variables

The backend requires the following environment variables:

```

SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@host:5432/dbname
FLASK_ENV=development

```

Use `.env.example` in the root as a reference.

Never commit a real `.env` file.

---

## Running the Backend Locally

1. Create a virtual environment:

```

python -m venv venv

```

2. Activate it:

Mac/Linux:
```

source venv/bin/activate

```

Windows:
```

venv\Scripts\activate

```

3. Install dependencies:

```

pip install -r backend/requirements.txt

```

4. Run the app:

```

python backend/app.py

```

The server will start at:

```

[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

Test health endpoint:

```

GET /health

```

---

##  Architecture Overview

We follow a layered architecture:

- Controllers → Handle HTTP requests
- Services → Business logic
- Models → Database layer
- Utils → Shared helpers

Controllers should NOT contain business logic.  
Services should NOT handle HTTP directly.

---

## 🛠 Tech Stack

- Flask
- PostgreSQL
- psycopg2 or SQLAlchemy (depending on implementation)
```

