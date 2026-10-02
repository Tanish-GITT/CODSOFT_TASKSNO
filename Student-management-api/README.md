\# Student Record Management API



A RESTful API for managing students, courses, and student enrollments.



This project is built with Flask and SQLAlchemy and provides CRUD operations, data validation, searching, filtering, sorting, pagination, and relationship management between students and courses.



\## Tech Stack



\- \*\*Language:\*\* Python

\- \*\*Backend:\*\* Flask

\- \*\*ORM:\*\* Flask-SQLAlchemy

\- \*\*Database:\*\* SQLite

\- \*\*API Testing:\*\* Postman



\## Features



\### Student Management



\- Create a student

\- Retrieve all students

\- Retrieve a student by ID

\- Update student information

\- Delete a student

\- Search students by name or email

\- Pagination

\- Email format validation

\- Duplicate email protection



\### Course Management



\- Create a course

\- Retrieve all courses

\- Retrieve a course by ID

\- Update course information

\- Delete a course

\- Filter courses by credits

\- Sort courses by name or credits

\- Pagination

\- Duplicate course code protection



\### Enrollment Management



\- Enroll a student in a course

\- Retrieve all enrollments

\- Retrieve an enrollment by ID

\- Delete an enrollment

\- Filter enrollments by student or course

\- Pagination

\- Prevent duplicate enrollments

\- Validate student and course existence

\- Return related student and course information



\### Validation \& Error Handling



The API validates incoming request data before storing it in the database.



It also handles common API errors using appropriate HTTP status codes:



| Status Code | Meaning |

|---|---|

| `200 OK` | Request completed successfully |

| `201 Created` | Resource created successfully |

| `400 Bad Request` | Invalid request data |

| `404 Not Found` | Requested resource does not exist |

| `409 Conflict` | Resource conflicts with existing data |



Examples of handled errors include:



\- Missing required fields

\- Invalid email format

\- Invalid course credits

\- Invalid student/course IDs

\- Non-existent students or courses

\- Duplicate student emails

\- Duplicate course codes

\- Duplicate enrollments



\## Project Structure



```text

Student-management-api/

│

├── app.py

├── extensions.py

├── README.md

│

├── models/

│   ├── \_\_init\_\_.py

│   ├── students.py

│   ├── courses.py

│   └── enrollments.py

│

├── validators/

│   ├── \_\_init\_\_.py

│   ├── students.py

│   ├── courses.py

│   └── enrollments.py

│

├── routes/

│   ├── \_\_init\_\_.py

│   ├── students.py

│   ├── courses.py

│   └── enrollments.py

│

└── instance/

&#x20;   └── mydatabase.db

```



\### Directory Responsibilities



| File/Directory | Responsibility |

|---|---|

| `app.py` | Creates and configures the Flask application |

| `extensions.py` | Initializes the SQLAlchemy database extension |

| `models/` | Defines database models and relationships |

| `validators/` | Handles request-data validation |

| `routes/` | Contains API endpoints grouped by resource |

| `instance/` | Stores the local SQLite database |



The application follows a modular structure that separates database models, validation logic, and API routes.



\## Database Design



The application uses three main models:



```text

Student

&#x20;  │

&#x20;  │

&#x20;  ▼

Enrollment

&#x20;  │

&#x20;  │

&#x20;  ▼

Course

```



\### Student



Stores student information:



\- `id`

\- `name`

\- `email`



The email field is unique to prevent duplicate student records.



\### Course



Stores course information:



\- `id`

\- `name`

\- `code`

\- `description`

\- `credits`



The course code is unique.



\### Enrollment



Acts as a bridge between students and courses.



It contains:



\- `id`

\- `student\_id`

\- `course\_id`



A unique constraint prevents the same student from being enrolled in the same course more than once.



\## Installation



\### 1. Clone the repository



```bash

git clone <your-github-repository-url>

cd Student-management-api

```



\### 2. Create a virtual environment



On Windows:



```bash

python -m venv venv

```



Activate it:



```bash

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install flask flask-sqlalchemy

```



\### 4. Run the application



```bash

python app.py

```



The API will be available at:



```text

http://127.0.0.1:5000

```



\## Health Check



To verify that the API is running:



```http

GET /api/health

```



Example:



```text

GET http://127.0.0.1:5000/api/health

```



Response:



```json

{

&#x20;   "status": "ok"

}

```



\## API Endpoints



\### Students



| Method | Endpoint | Description |

|---|---|---|

| `GET` | `/api/students` | Get students |

| `GET` | `/api/students/<student\_id>` | Get a student by ID |

| `POST` | `/api/students` | Create a student |

| `PUT` | `/api/students/<student\_id>` | Update a student |

| `DELETE` | `/api/students/<student\_id>` | Delete a student |



\### Student Search



Search by name or email:



```http

GET /api/students?search=tanish

```



\### Student Pagination



```http

GET /api/students?page=1\&per\_page=10

```



Search and pagination can also be combined:



```http

GET /api/students?search=tanish\&page=1\&per\_page=5

```



\---



\### Courses



| Method | Endpoint | Description |

|---|---|---|

| `GET` | `/api/courses` | Get courses |

| `GET` | `/api/courses/<course\_id>` | Get a course by ID |

| `POST` | `/api/courses` | Create a course |

| `PUT` | `/api/courses/<course\_id>` | Update a course |

| `DELETE` | `/api/courses/<course\_id>` | Delete a course |



\### Course Filtering



Filter courses by credits:



```http

GET /api/courses?credits=4

```



\### Course Sorting



Sort by name:



```http

GET /api/courses?sort=name

```



Sort by name in descending order:



```http

GET /api/courses?sort=-name

```



Sort by credits:



```http

GET /api/courses?sort=credits

```



Sort by credits in descending order:



```http

GET /api/courses?sort=-credits

```



\### Course Pagination



```http

GET /api/courses?page=1\&per\_page=10

```



Filtering, sorting, and pagination can be combined:



```http

GET /api/courses?credits=4\&sort=-name\&page=1\&per\_page=5

```



\---



\### Enrollments



| Method | Endpoint | Description |

|---|---|---|

| `GET` | `/api/enrollments` | Get enrollments |

| `GET` | `/api/enrollments/<enrollment\_id>` | Get an enrollment by ID |

| `POST` | `/api/enrollments` | Enroll a student in a course |

| `DELETE` | `/api/enrollments/<enrollment\_id>` | Delete an enrollment |



\### Enrollment Filtering



Filter by student:



```http

GET /api/enrollments?student\_id=1

```



Filter by course:



```http

GET /api/enrollments?course\_id=1

```



Filters can also be combined with pagination:



```http

GET /api/enrollments?student\_id=1\&page=1\&per\_page=5

```



\## Example Requests



\### Create Student



```http

POST /api/students

```



```json

{

&#x20;   "name": "John Doe",

&#x20;   "email": "john@example.com"

}

```



\### Create Course



```http

POST /api/courses

```



```json

{

&#x20;   "name": "Python Programming",

&#x20;   "code": "PY101",

&#x20;   "description": "Introduction to Python programming",

&#x20;   "credits": 4

}

```



\### Create Enrollment



```http

POST /api/enrollments

```



```json

{

&#x20;   "student\_id": 1,

&#x20;   "course\_id": 1

}

```



Example successful response:



```json

{

&#x20;   "id": 1,

&#x20;   "student\_id": 1,

&#x20;   "course\_id": 1

}

```



\## Example Enrollment Response



The enrollment GET endpoint includes related student and course information:



```json

{

&#x20;   "enrollments": \[

&#x20;       {

&#x20;           "id": 1,

&#x20;           "student": {

&#x20;               "id": 1,

&#x20;               "

