# TO-DO List Backend API

A comprehensive RESTful API for task management with user authentication, built with Flask and SQLAlchemy.

## Features

### Core Features
- ✅ **CRUD Operations**: Create, read, update, and delete tasks
- ✅ **Task Status Management**: Mark tasks as completed or pending
- ✅ **Secure Storage**: SQLite database with SQLAlchemy ORM
- ✅ **Data Validation**: Comprehensive request validation
- ✅ **HTTP Status Codes**: Proper status codes for all responses
- ✅ **Filtering & Search**: Filter by status, priority, category, and search by text
- ✅ **Structured Architecture**: Organized with controllers, routes, models, and validators

### Bonus Features
- 🔐 **User Authentication**: JWT-based authentication system
- 📅 **Due Dates**: Set and track task deadlines
- ⭐ **Priority Levels**: Low, medium, and high priority tasks
- 🏷️ **Categories**: Organize tasks with custom categories
- 📊 **Task Statistics**: Get overview of task completion and priorities
- 🔍 **Advanced Search**: Search tasks by title and description
- 📄 **Pagination**: Efficient data retrieval with pagination

## Tech Stack

- **Language**: Python 3.8+
- **Framework**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Password Hashing**: Flask-Bcrypt 1.0.1
- **Database**: SQLite
- **CORS**: Flask-CORS 4.0.0
- **Email Validation**: email-validator 2.1.0

## Project Structure

```
TO-DO list backend/
│
├── app.py                    # Main application entry point
├── extensions.py             # Flask extensions initialization
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Application configuration
│
├── models/
│   ├── __init__.py
│   ├── users.py             # User model
│   └── tasks.py             # Task model
│
├── routes/
│   ├── __init__.py
│   ├── auth.py              # Authentication endpoints
│   └── tasks.py             # Task management endpoints
│
├── validators/
│   ├── __init__.py
│   ├── users.py             # User data validation
│   └── tasks.py             # Task data validation
│
└── middleware/
    └── auth.py              # Authentication middleware
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd "TO-DO list backend"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///todo.db
```

### 6. Run the application

```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication

All task endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## Endpoints

### Health Check

#### Check API Status
```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "TO-DO List API is running"
}
```

---

### Authentication Endpoints

#### 1. Register a New User

```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123"
}
```

**Validation Rules:**
- Username: Required, 3-80 characters
- Email: Required, valid email format
- Password: Required, minimum 6 characters

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-10-08T08:53:38.775Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors
- `409 Conflict`: Username or email already exists

---

#### 2. Login

```http
POST /api/auth/login
```

**Request Body (with username):**
```json
{
  "username": "john_doe",
  "password": "secure123"
}
```

**Or with email:**
```json
{
  "email": "john@example.com",
  "password": "secure123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-10-08T08:53:38.775Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Invalid credentials

---

### Task Endpoints

All task endpoints require authentication (JWT token).

#### 1. Create a Task

```http
POST /api/tasks
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "pending",
  "priority": "high",
  "category": "Work",
  "due_date": "2026-10-15T18:00:00"
}
```

**Field Details:**
- `title` (required): String, max 200 characters
- `description` (optional): String, max 1000 characters
- `status` (optional): `pending` or `completed` (default: `pending`)
- `priority` (optional): `low`, `medium`, or `high` (default: `medium`)
- `category` (optional): String, max 50 characters
- `due_date` (optional): ISO 8601 format

**Response (201 Created):**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "status": "pending",
    "priority": "high",
    "category": "Work",
    "due_date": "2026-10-15T18:00:00",
    "created_at": "2026-10-08T08:53:38.775Z",
    "updated_at": "2026-10-08T08:53:38.775Z",
    "user_id": 1
  }
}
```

---

#### 2. Get All Tasks

```http
GET /api/tasks
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` (optional): Filter by status (`pending` or `completed`)
- `priority` (optional): Filter by priority (`low`, `medium`, or `high`)
- `category` (optional): Filter by category
- `search` (optional): Search in title and description
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Examples:**

Get all tasks:
```http
GET /api/tasks
```

Filter by status:
```http
GET /api/tasks?status=pending
```

Filter by priority:
```http
GET /api/tasks?priority=high
```

Filter by category:
```http
GET /api/tasks?category=Work
```

Search tasks:
```http
GET /api/tasks?search=documentation
```

Combine filters with pagination:
```http
GET /api/tasks?status=pending&priority=high&page=1&per_page=5
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API docs",
      "status": "pending",
      "priority": "high",
      "category": "Work",
      "due_date": "2026-10-15T18:00:00",
      "created_at": "2026-10-08T08:53:38.775Z",
      "updated_at": "2026-10-08T08:53:38.775Z",
      "user_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

---

#### 3. Get Single Task

```http
GET /api/tasks/<task_id>
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "status": "pending",
    "priority": "high",
    "category": "Work",
    "due_date": "2026-10-15T18:00:00",
    "created_at": "2026-10-08T08:53:38.775Z",
    "updated_at": "2026-10-08T08:53:38.775Z",
    "user_id": 1
  }
}
```

**Error Response:**
- `404 Not Found`: Task not found

---

#### 4. Update a Task

```http
PUT /api/tasks/<task_id>
Authorization: Bearer <token>
```

**Request Body (all fields optional):**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "priority": "medium",
  "category": "Personal",
  "due_date": "2026-10-20T18:00:00"
}
```

**Response (200 OK):**
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed",
    "priority": "medium",
    "category": "Personal",
    "due_date": "2026-10-20T18:00:00",
    "created_at": "2026-10-08T08:53:38.775Z",
    "updated_at": "2026-10-08T09:00:00.000Z",
    "user_id": 1
  }
}
```

---

#### 5. Delete a Task

```http
DELETE /api/tasks/<task_id>
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Error Response:**
- `404 Not Found`: Task not found

---

#### 6. Mark Task as Completed

```http
PATCH /api/tasks/<task_id>/complete
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Task marked as completed",
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "status": "completed",
    ...
  }
}
```

---

#### 7. Mark Task as Pending

```http
PATCH /api/tasks/<task_id>/pending
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Task marked as pending",
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "status": "pending",
    ...
  }
}
```

---

#### 8. Get Task Statistics

```http
GET /api/tasks/stats
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 10,
  "overdue_tasks": 3,
  "by_priority": {
    "high": 4,
    "medium": 5,
    "low": 1
  }
}
```

---

## HTTP Status Codes

| Status Code | Meaning |
|-------------|---------|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid request data or validation error |
| `401 Unauthorized` | Missing or invalid authentication token |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Resource conflicts with existing data |
| `500 Internal Server Error` | Server error |

## Error Response Format

All error responses follow this format:

**Single Error:**
```json
{
  "error": "Error message here"
}
```

**Multiple Validation Errors:**
```json
{
  "errors": [
    "Title is required",
    "Invalid email format"
  ]
}
```

## Database Models

### User Model
```python
- id: Integer (Primary Key)
- username: String(80), Unique, Required
- email: String(120), Unique, Required
- password_hash: String(128), Required
- created_at: DateTime
- tasks: Relationship to Task
```

### Task Model
```python
- id: Integer (Primary Key)
- title: String(200), Required
- description: Text, Optional
- status: String(20), Default: 'pending'
- priority: String(20), Default: 'medium'
- category: String(50), Optional
- due_date: DateTime, Optional
- created_at: DateTime
- updated_at: DateTime
- user_id: Integer (Foreign Key)
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with 24-hour token expiry
- **User Isolation**: Users can only access their own tasks
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protects against SQL injection
- **CORS Configuration**: Controlled cross-origin resource sharing

## Testing with Postman

### Import Collection

1. Open Postman
2. Create a new collection named "TO-DO List API"
3. Add the endpoints documented above

### Testing Flow

1. **Register a user** → Save the user details
2. **Login** → Save the `access_token` from response
3. **Set up Authorization**:
   - Go to Collection → Authorization
   - Type: Bearer Token
   - Token: Paste the `access_token`
4. **Test task endpoints** with authentication

### Sample Postman Requests

**Environment Variables:**
```
base_url = http://localhost:5000/api
token = <your-jwt-token>
```

## Development

### Run in Development Mode

```bash
python app.py
```

The server runs on `http://localhost:5000` with debug mode enabled.

### Database Migrations

The database is automatically created when you first run the application. To reset the database:

1. Stop the application
2. Delete `todo.db` file
3. Restart the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational purposes as part of CodSoft internship tasks.

## Author

Developed as part of CodSoft Task 3 - Backend Development

---

## Quick Start Example

```bash
# 1. Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'

# 2. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'

# 3. Create a task (use token from login)
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"title":"My first task","priority":"high"}'

# 4. Get all tasks
curl -X GET http://localhost:5000/api/tasks \
  -H "Authorization: Bearer <your-token>"
```

## Support

For issues or questions, please create an issue in the repository.
