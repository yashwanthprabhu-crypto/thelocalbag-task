# FastAPI CRUD Project

A simple CRUD (Create, Read, Update, Delete) API built with FastAPI.

## Project Structure

```
fastapi_crud_project/
│── main.py             # Main FastAPI application
│── models.py           # Pydantic models
│── database.py         # In-memory storage
│── routes/
│   ├── users.py        # CRUD operations for users
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
```

## Setup and Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API documentation at:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

- POST /users/ - Create a new user
- GET /users/{user_id} - Get user by ID
- GET /users/search - Search users by name
- PUT /users/{user_id} - Update user
- DELETE /users/{user_id} - Delete user# Thelocalbag-Task
