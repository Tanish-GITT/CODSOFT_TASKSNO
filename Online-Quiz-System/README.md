# Online Quiz System - Backend API

A comprehensive backend application for quiz management with role-based access control, automatic scoring, and performance analytics.

## Features

### Core Requirements
- ✅ **Database Models**: Users, Quizzes, Questions, Options, QuizAttempts, Answers
- ✅ **REST APIs**: Quiz creation, question management, answer submission
- ✅ **Automatic Scoring**: Calculate scores immediately after submission
- ✅ **Result History**: Store all quiz attempts for each user
- ✅ **Answer Validation**: Validate all submitted answers before processing
- ✅ **Leaderboard**: Retrieve top performers for each quiz
- ✅ **Performance Statistics**: User-specific analytics and insights
- ✅ **Authentication & Authorization**: JWT-based with admin/user roles
- ✅ **Complete Documentation**: API docs and testing guide

### Bonus Features
- 🎯 **Quiz Timers**: Set duration limits for each quiz
- ➖ **Negative Marking**: Deduct marks for wrong answers (configurable)
- 🎲 **Random Question Generation**: Randomize question order per attempt
- 🏆 **Certificate Eligibility**: Award certificates based on pass percentage

## Tech Stack

- **Language**: Python 3.8+
- **Framework**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Password Hashing**: Flask-Bcrypt 1.0.1
- **Database**: SQLite
- **CORS**: Flask-CORS 4.0.0

## Project Structure

```
Online-Quiz-System/
│
├── app.py                      # Main application entry point
├── extensions.py               # Flask extensions
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Application configuration
│
├── models/
│   ├── __init__.py
│   ├── users.py               # User model
│   ├── quizzes.py             # Quiz model
│   ├── questions.py           # Question model
│   ├── options.py             # Option model
│   ├── quiz_attempts.py       # QuizAttempt model
│   └── answers.py             # Answer model
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication endpoints
│   ├── quizzes.py             # Quiz management endpoints
│   └── attempts.py            # Quiz attempt and results endpoints
│
├── validators/
│   ├── __init__.py
│   ├── users.py               # User validation
│   ├── quizzes.py             # Quiz validation
│   ├── questions.py           # Question validation
│   └── answers.py             # Answer validation
│
└── middleware/
    └── auth.py                # Authentication middleware
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Online-Quiz-System
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

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

```bash
cp .env.example .env
```

Edit `.env`:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///quiz.db
```

### 6. Run the application

```bash
python app.py
```

API will be available at: `http://localhost:5000`

## API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Authentication

All quiz and attempt endpoints require JWT authentication. Include token in header:
```
Authorization: Bearer <your-jwt-token>
```

Admin endpoints require `role: admin`.

---

## Authentication Endpoints

### 1. Register User

```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure123",
  "role": "user"
}
```

**Roles:** `user` (default) or `admin`

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2026-10-08T12:38:31.390Z"
  }
}
```

---

### 2. Login

```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "secure123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2026-10-08T12:38:31.390Z"
  }
}
```

---

## Quiz Management (Admin Only)

### 1. Create Quiz

```http
POST /api/quizzes
Authorization: Bearer <admin-token>
```

**Request Body:**
```json
{
  "title": "Python Programming Basics",
  "description": "Test your Python fundamentals",
  "category": "Programming",
  "difficulty": "medium",
  "duration_minutes": 30,
  "pass_percentage": 70,
  "has_negative_marking": true,
  "negative_marks": 0.25,
  "randomize_questions": true
}
```

**Response (201):**
```json
{
  "message": "Quiz created successfully",
  "quiz": {
    "id": 1,
    "title": "Python Programming Basics",
    "description": "Test your Python fundamentals",
    "category": "Programming",
    "difficulty": "medium",
    "duration_minutes": 30,
    "pass_percentage": 70,
    "has_negative_marking": true,
    "negative_marks": 0.25,
    "randomize_questions": true,
    "is_active": true,
    "total_questions": 0,
    "created_at": "2026-10-08T12:38:31.390Z",
    "updated_at": "2026-10-08T12:38:31.390Z",
    "created_by": 1
  }
}
```

---

### 2. Add Question to Quiz

```http
POST /api/quizzes/{quiz_id}/questions
Authorization: Bearer <admin-token>
```

**Request Body:**
```json
{
  "question_text": "What is the output of print(type([]))?",
  "question_type": "multiple_choice",
  "marks": 2.0,
  "options": [
    {
      "option_text": "<class 'list'>",
      "is_correct": true
    },
    {
      "option_text": "<class 'dict'>",
      "is_correct": false
    },
    {
      "option_text": "<class 'tuple'>",
      "is_correct": false
    },
    {
      "option_text": "<class 'set'>",
      "is_correct": false
    }
  ]
}
```

**Response (201):**
```json
{
  "message": "Question added successfully",
  "question": {
    "id": 1,
    "quiz_id": 1,
    "question_text": "What is the output of print(type([]))?",
    "question_type": "multiple_choice",
    "marks": 2.0,
    "order": 1,
    "created_at": "2026-10-08T12:38:31.390Z",
    "options": [...]
  }
}
```

---

### 3. Update Quiz

```http
PUT /api/quizzes/{quiz_id}
Authorization: Bearer <admin-token>
```

**Request Body (all fields optional):**
```json
{
  "title": "Updated Quiz Title",
  "is_active": true,
  "pass_percentage": 75
}
```

---

### 4. Delete Quiz

```http
DELETE /api/quizzes/{quiz_id}
Authorization: Bearer <admin-token>
```

---

### 5. Update Question

```http
PUT /api/quizzes/{quiz_id}/questions/{question_id}
Authorization: Bearer <admin-token>
```

---

### 6. Delete Question

```http
DELETE /api/quizzes/{quiz_id}/questions/{question_id}
Authorization: Bearer <admin-token>
```

---

### 7. Get All Quizzes (Admin View)

```http
GET /api/quizzes/admin/all
Authorization: Bearer <admin-token>
```

---

## Quiz Taking (All Users)

### 1. Get All Active Quizzes

```http
GET /api/quizzes
Authorization: Bearer <token>
```

**Query Parameters:**
- `category` (optional): Filter by category
- `difficulty` (optional): Filter by difficulty
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Response (200):**
```json
{
  "quizzes": [
    {
      "id": 1,
      "title": "Python Programming Basics",
      "description": "Test your Python fundamentals",
      "category": "Programming",
      "difficulty": "medium",
      "duration_minutes": 30,
      "pass_percentage": 70,
      "has_negative_marking": true,
      "negative_marks": 0.25,
      "randomize_questions": true,
      "is_active": true,
      "total_questions": 10,
      "created_at": "2026-10-08T12:38:31.390Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

---

### 2. Get Quiz Details

```http
GET /api/quizzes/{quiz_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "quiz": {
    "id": 1,
    "title": "Python Programming Basics",
    "duration_minutes": 30,
    "total_questions": 10,
    "questions": [
      {
        "id": 1,
        "question_text": "What is the output of print(type([]))?",
        "question_type": "multiple_choice",
        "marks": 2.0,
        "options": [
          {
            "id": 1,
            "option_text": "<class 'list'>",
            "order": 1
          },
          {
            "id": 2,
            "option_text": "<class 'dict'>",
            "order": 2
          }
        ]
      }
    ]
  }
}
```

Note: Correct answers are NOT included for users.

---

### 3. Start Quiz

```http
POST /api/attempts/start
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "quiz_id": 1
}
```

**Response (201):**
```json
{
  "message": "Quiz started successfully",
  "attempt": {
    "id": 1,
    "user_id": 1,
    "quiz_id": 1,
    "start_time": "2026-10-08T12:38:31.390Z",
    "status": "in_progress"
  },
  "quiz": {...},
  "end_time": "2026-10-08T13:08:31.390Z"
}
```

---

### 4. Submit Answers

```http
POST /api/attempts/submit
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "attempt_id": 1,
  "answers": [
    {
      "question_id": 1,
      "selected_option_id": 1
    },
    {
      "question_id": 2,
      "selected_option_id": 5
    }
  ]
}
```

**Response (200):**
```json
{
  "message": "Quiz submitted successfully",
  "result": {
    "attempt_id": 1,
    "score": 15.5,
    "total_marks": 20,
    "percentage": 77.5,
    "passed": true,
    "certificate_eligible": true,
    "correct_answers": 8,
    "wrong_answers": 2,
    "total_questions": 10,
    "time_taken_minutes": 25
  }
}
```

---

### 5. Get My Attempts

```http
GET /api/attempts/my-attempts
Authorization: Bearer <token>
```

**Query Parameters:**
- `quiz_id` (optional): Filter by quiz
- `page` (optional)
- `per_page` (optional)

**Response (200):**
```json
{
  "attempts": [
    {
      "id": 1,
      "quiz_id": 1,
      "quiz_title": "Python Programming Basics",
      "start_time": "2026-10-08T12:38:31.390Z",
      "end_time": "2026-10-08T13:03:31.390Z",
      "status": "completed",
      "score": 15.5,
      "total_marks": 20,
      "percentage": 77.5,
      "passed": true,
      "certificate_eligible": true,
      "time_taken_minutes": 25
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

---

### 6. Get Attempt Details

```http
GET /api/attempts/{attempt_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "result": {
    "id": 1,
    "quiz_title": "Python Programming Basics",
    "score": 15.5,
    "percentage": 77.5,
    "detailed_answers": [
      {
        "question": {
          "question_text": "What is the output of print(type([]))?",
          "options": [...]
        },
        "selected_option": {
          "option_text": "<class 'list'>",
          "is_correct": true
        },
        "correct_option_id": 1,
        "is_correct": true,
        "marks_obtained": 2.0
      }
    ]
  }
}
```

---

### 7. Get Leaderboard

```http
GET /api/attempts/leaderboard/{quiz_id}
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of top users (default: 10)

**Response (200):**
```json
{
  "quiz_title": "Python Programming Basics",
  "leaderboard": [
    {
      "rank": 1,
      "username": "alice",
      "score": 19.5,
      "percentage": 97.5,
      "time_taken_minutes": 20,
      "attempt_date": "2026-10-08T13:00:00.000Z"
    },
    {
      "rank": 2,
      "username": "bob",
      "score": 18.0,
      "percentage": 90.0,
      "time_taken_minutes": 25,
      "attempt_date": "2026-10-08T12:55:00.000Z"
    }
  ]
}
```

---

### 8. Get User Statistics

```http
GET /api/attempts/statistics
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "total_attempts": 15,
  "passed_attempts": 12,
  "failed_attempts": 3,
  "average_score": 78.5,
  "certificates_earned": 10,
  "recent_attempts": [
    {
      "quiz_title": "Python Programming Basics",
      "score": 15.5,
      "percentage": 77.5,
      "passed": true,
      "date": "2026-10-08T13:03:31.390Z"
    }
  ]
}
```

---

### 9. Get All Attempts (Admin)

```http
GET /api/attempts/admin/all-attempts
Authorization: Bearer <admin-token>
```

---

## Database Models

### User
```python
- id: Integer (Primary Key)
- username: String(80), Unique
- email: String(120), Unique
- password_hash: String(128)
- role: String(20) - 'admin' or 'user'
- created_at: DateTime
```

### Quiz
```python
- id: Integer (Primary Key)
- title: String(200)
- description: Text
- category: String(50)
- difficulty: String(20) - 'easy', 'medium', 'hard'
- duration_minutes: Integer (timer)
- pass_percentage: Integer (for certificates)
- has_negative_marking: Boolean
- negative_marks: Float
- randomize_questions: Boolean
- is_active: Boolean
- created_at, updated_at: DateTime
- created_by: Foreign Key (User)
```

### Question
```python
- id: Integer (Primary Key)
- quiz_id: Foreign Key (Quiz)
- question_text: Text
- question_type: String(20) - 'multiple_choice', 'true_false'
- marks: Float
- order: Integer
- created_at: DateTime
```

### Option
```python
- id: Integer (Primary Key)
- question_id: Foreign Key (Question)
- option_text: Text
- is_correct: Boolean
- order: Integer
```

### QuizAttempt
```python
- id: Integer (Primary Key)
- user_id: Foreign Key (User)
- quiz_id: Foreign Key (Quiz)
- start_time, end_time: DateTime
- status: String(20) - 'in_progress', 'completed', 'abandoned'
- score: Float
- total_marks: Float
- percentage: Float
- passed: Boolean
- certificate_eligible: Boolean
- time_taken_minutes: Integer
```

### Answer
```python
- id: Integer (Primary Key)
- attempt_id: Foreign Key (QuizAttempt)
- question_id: Foreign Key (Question)
- selected_option_id: Foreign Key (Option)
- is_correct: Boolean
- marks_obtained: Float
```

---

## Features Explained

### Quiz Timer
- Set `duration_minutes` when creating quiz
- Frontend should track time from `start_time` to `end_time`
- System calculates `time_taken_minutes` on submission

### Negative Marking
- Enable with `has_negative_marking: true`
- Set penalty with `negative_marks` (e.g., 0.25)
- Deducted automatically on wrong answers
- Final score cannot be negative

### Random Questions
- Enable with `randomize_questions: true`
- Questions shuffled per attempt
- Prevents answer pattern memorization

### Certificate Eligibility
- Automatic based on `pass_percentage`
- User must score >= pass percentage
- Tracked in `certificate_eligible` field

### Leaderboard
- Shows best attempt per user
- Ranked by score, then by time taken
- Configurable limit

### Performance Statistics
- Total attempts, pass rate
- Average score across all quizzes
- Certificates earned
- Recent attempt history

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (duplicate data) |
| 500 | Internal Server Error |

---

## Security Features

- **Password Hashing**: Bcrypt encryption
- **JWT Authentication**: 24-hour token expiry
- **Role-Based Access**: Admin vs User permissions
- **Input Validation**: All requests validated
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Answer Security**: Correct answers hidden from users during quiz

---

## Testing Flow

1. **Register Admin** → role: "admin"
2. **Register User** → role: "user"
3. **Login as Admin** → Get admin token
4. **Create Quiz** → With admin token
5. **Add Questions** → With options and correct answers
6. **Login as User** → Get user token
7. **Get Quizzes** → See available quizzes
8. **Start Quiz** → Get attempt ID
9. **Submit Answers** → Get instant results
10. **View Leaderboard** → See rankings
11. **Get Statistics** → View performance

---

## Development

```bash
# Run in development
python app.py

# Reset database (delete quiz.db and restart)
rm quiz.db
python app.py
```

---

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## License

Educational project for CodSoft Task 5

---

## Author

Developed as part of CodSoft Backend Development Internship

## Support

For issues or questions, create an issue in the repository.
