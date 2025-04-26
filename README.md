# BLX MARKETPLACE 🛒

## 📝 Overview 
This is a personal project designed to apply and deepen the knowledge I have gained in FastAPI, SQLAlchemy, Alembic, and JWT for authentication.

## 💻 Technologies Used 
- **FastAPI** - High-performance web framework for building APIs.
- **SQLAlchemy** - SQL toolkit and ORM for database interactions.
- **Alembic** - Database migration tool for SQLAlchemy.
- **JWT (JSON Web Token)** - Authentication mechanism for secure API access.
- **Docker** - Used to containerize the API for deployment on Render.

### ⚙️ Prerequisites 
- Python 3.10+
- Optional: PostgreSQL (or another compatible relational database)

## 🛠️ Installation 
```bash
git clone https://github.com/steven-dev8/blx.git
cd blx
python -m venv venv
```
🪟 Windows
``` bash
# CMD
venv\Scripts\activate.bat
# PowerShell
venv\Scripts\Activate.ps1
```
🐧 Linux
```bash
source venv/bin/activate
```

### Installing dependencies
```
pip install -r requirements.txt
```

### Initializing the server
```bash
uvicorn src.main:app --port 8000 --reload-dir=src
```
## 🌿 Environment Variables

### Required Environment Variables for Proper Operation

These are the required environment variables that must be set for the application to work properly.

| **Variable**          | **Description**                                                            | **Example**                               |
|-----------------------|----------------------------------------------------------------------------|-------------------------------------------|
| `DATABASE_URL`        | The connection string for the database.                                     | `postgresql://user:password@localhost/dbname`, default SQLite |
| `SECRET_KEY`      | The secret key used for signing JWT tokens.                                 | `supersecretkey`                          |
| `ALGORITHM`       | The algorithm used to encode the JWT token.                                 | `HS256`                                   |
| `EXPIRES_IN_MINUTE` | The expiration time of the access token in minutes.                   | `30`, default 500                                      |


# 📜 Access, Documentation, and API Structure 

### Accessing the API
**Base URL**: `http://localhost:8000`

### 📚 Documentation

- **Swagger Documentation**: (RECOMMENDED) `http://localhost:8000/docs`
- **Redoc Documentation**: `http://localhost:8000/redoc`
- **Swagger Render (ONLINE)**: `https://blx-marketplace.onrender.com/` (Note: This version may be unstable, intended for endpoint visualization only.)

### 📂 Structure
```bash
src/
│
├── infra/
├── routers/
├── schema/
└── main.py
```

## 📄 License 

This project is licensed under the MIT License. See the LICENSE file for details.

## 👤 Author 

- Steven Araújo – @steven-dev8
