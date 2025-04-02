# Task Manager API

🚀 Overview

This is a Flask-based Task Manager API that allows users to register, authenticate, and manage tasks with JWT-based authentication.

✨ Features

🧑‍💻 User Registration & Authentication

🔐 JWT-based Authentication

📝 CRUD Operations for Tasks

🗄️ Database Integration using SQLAlchemy

✅ Marshmallow for Data Validation

⚙️ Error Handling & Logging

🛠️ Tech Stack

Back-end: Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Marshmallow

Database: PostgreSQL

Dependencies: SQLAlchemy, Marshmallow, Flask, Flask-JWT-Extended, psycopg2-binary

📥 Installation

✅ Prerequisites

Python 3.8+

PostgreSQL Database

📌 Steps

1️⃣ Clone the repository

git clone https://github.com/your-repo/task-manager-api.git
cd task-manager-api

2️⃣ Create a virtual environment and activate it

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Set up the database (update config.py with your database credentials)

export DATABASE_URL="postgresql://user:password@localhost/task_db"

### postman collection https://technical-test-phase.postman.co/workspace/Technical-Test-Phase-Workspace-~d30430da-a175-4e92-9e9f-3d6a1dc0aa97/collection/16166567-d81dac87-67a7-44ad-915b-a395e6a31125?action=share&creator=16166567

5️⃣ Run database migrations

flask db upgrade

6️⃣ Run the application

python main.py

📌 API Endpoints

🔐 Authentication

📝 Register a new user

POST /auth/register

📤 Request Body:

{
    "username": "testuser",
    "password": "testpassword"
}

📥 Response:

{
    "message": "User registered successfully"
}

🔑 Login

POST /auth/login

📤 Request Body:

{
    "username": "testuser",
    "password": "testpassword"
}

📥 Response:

{
    "access_token": "your-jwt-token"
}

📋 Task Management

➕ Create a new task

POST /tasksAuthorization: Bearer {JWT_TOKEN}

📤 Request Body:

{
    "title": "Learn Flask",
    "description": "Build an API with Flask"
}

📂 Get all tasks

GET /tasksAuthorization: Bearer {JWT_TOKEN}

🔍 Get task by ID

GET /tasks/{task_id}Authorization: Bearer {JWT_TOKEN}

✏️ Update a task

PUT /tasks/{task_id}Authorization: Bearer {JWT_TOKEN}

📤 Request Body:

{
    "title": "Updated Task",
    "status": "completed"
}

❌ Delete a task

DELETE /tasks/{task_id}Authorization: Bearer {JWT_TOKEN}

⚠️ Error Handling

Error Type

Status Code

Description

Validation Error

400

Invalid input data

Unauthorized

401

Invalid credentials or missing token

Not Found

404

Resource not found

Server Error

500

Internal server error

📜 License

This project is licensed under the MIT License.