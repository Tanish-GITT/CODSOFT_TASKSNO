# Testing TO-DO List API with Postman

## Step-by-Step Postman Testing Guide

### Step 1: Start the Server

1. Open a terminal in the project directory
2. Activate your virtual environment:
   ```bash
   cd "TO-DO list backend"
   venv\Scripts\activate
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. Verify the server is running at `http://localhost:5000`

---

### Step 2: Set Up Postman

1. **Open Postman** (download from https://www.postman.com if needed)
2. **Create a new Collection**:
   - Click "New" → "Collection"
   - Name it: "TO-DO List API"
   - Save it

3. **Set up Environment Variables** (Optional but recommended):
   - Click on "Environments" in the left sidebar
   - Click "+" to create new environment
   - Name it: "TO-DO Local"
   - Add variables:
     ```
     base_url = http://localhost:5000/api
     token = (leave empty for now)
     ```
   - Click "Save"
   - Select this environment from the dropdown in top-right

---

### Step 3: Test Endpoints in Order

## 1. Health Check (No Auth Required)

**Purpose:** Verify the API is running

- **Method:** `GET`
- **URL:** `http://localhost:5000/api/health`
- **Headers:** None needed
- **Body:** None

**Expected Response (200 OK):**
```json
{
  "status": "ok",
  "message": "TO-DO List API is running"
}
```

---

## 2. Register a New User (No Auth Required)

**Purpose:** Create your first user account

- **Method:** `POST`
- **URL:** `http://localhost:5000/api/auth/register`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "test123"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2026-10-08T08:59:38.171Z"
  }
}
```

📝 **Note:** You can register multiple users to test user isolation.

---

## 3. Login

**Purpose:** Get authentication token

- **Method:** `POST`
- **URL:** `http://localhost:5000/api/auth/login`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "testuser",
  "password": "test123"
}
```

**OR login with email:**
```json
{
  "email": "test@example.com",
  "password": "test123"
}
```

**Expected Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2026-10-08T08:59:38.171Z"
  }
}
```

🔑 **IMPORTANT:** Copy the `access_token` value - you'll need it for all task endpoints!

---

### Step 4: Set Up Authentication for Task Endpoints

**For ALL requests below, you must add the Authorization header:**

**Option A: Manual Method**
1. Go to the "Headers" tab
2. Add a new header:
   - Key: `Authorization`
   - Value: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` (paste your token after "Bearer ")

**Option B: Collection-Level Auth (Recommended)**
1. Click on your "TO-DO List API" collection
2. Go to "Authorization" tab
3. Type: Select "Bearer Token"
4. Token: Paste your access token
5. Save
6. Now all requests in this collection inherit this auth automatically!

---

## 4. Create a Task (Requires Auth)

- **Method:** `POST`
- **URL:** `http://localhost:5000/api/tasks`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer <your-token>`
- **Body (raw JSON):**

**Minimal Example:**
```json
{
  "title": "Buy groceries"
}
```

**Full Example with all fields:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs for the TO-DO backend",
  "status": "pending",
  "priority": "high",
  "category": "Work",
  "due_date": "2026-10-15T18:00:00"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs for the TO-DO backend",
    "status": "pending",
    "priority": "high",
    "category": "Work",
    "due_date": "2026-10-15T18:00:00",
    "created_at": "2026-10-08T08:59:38.171Z",
    "updated_at": "2026-10-08T08:59:38.171Z",
    "user_id": 1
  }
}
```

📝 **Create multiple tasks** with different priorities, categories, and statuses to test filtering.

---

## 5. Get All Tasks (Requires Auth)

- **Method:** `GET`
- **URL:** `http://localhost:5000/api/tasks`
- **Headers:** 
  - `Authorization: Bearer <your-token>`
- **Body:** None

**Expected Response (200 OK):**
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
      "created_at": "2026-10-08T08:59:38.171Z",
      "updated_at": "2026-10-08T08:59:38.171Z",
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

## 6. Get Tasks with Filters (Requires Auth)

### Filter by Status
- **URL:** `http://localhost:5000/api/tasks?status=pending`

### Filter by Priority
- **URL:** `http://localhost:5000/api/tasks?priority=high`

### Filter by Category
- **URL:** `http://localhost:5000/api/tasks?category=Work`

### Search Tasks
- **URL:** `http://localhost:5000/api/tasks?search=documentation`

### Combined Filters with Pagination
- **URL:** `http://localhost:5000/api/tasks?status=pending&priority=high&page=1&per_page=5`

💡 **Tip:** In Postman, use the "Params" tab to add query parameters easily!

---

## 7. Get Single Task (Requires Auth)

- **Method:** `GET`
- **URL:** `http://localhost:5000/api/tasks/1` (replace 1 with your task ID)
- **Headers:** 
  - `Authorization: Bearer <your-token>`

**Expected Response (200 OK):**
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
    "created_at": "2026-10-08T08:59:38.171Z",
    "updated_at": "2026-10-08T08:59:38.171Z",
    "user_id": 1
  }
}
```

---

## 8. Update a Task (Requires Auth)

- **Method:** `PUT`
- **URL:** `http://localhost:5000/api/tasks/1` (replace 1 with your task ID)
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer <your-token>`
- **Body (raw JSON):**

**You can update any field(s):**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "priority": "medium",
  "category": "Personal",
  "due_date": "2026-10-20T18:00:00"
}
```

**Or update just one field:**
```json
{
  "priority": "low"
}
```

**Expected Response (200 OK):**
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Updated task title",
    ...
  }
}
```

---

## 9. Mark Task as Completed (Requires Auth)

- **Method:** `PATCH`
- **URL:** `http://localhost:5000/api/tasks/1/complete`
- **Headers:** 
  - `Authorization: Bearer <your-token>`
- **Body:** None

**Expected Response (200 OK):**
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

## 10. Mark Task as Pending (Requires Auth)

- **Method:** `PATCH`
- **URL:** `http://localhost:5000/api/tasks/1/pending`
- **Headers:** 
  - `Authorization: Bearer <your-token>`
- **Body:** None

---

## 11. Get Task Statistics (Requires Auth)

- **Method:** `GET`
- **URL:** `http://localhost:5000/api/tasks/stats`
- **Headers:** 
  - `Authorization: Bearer <your-token>`
- **Body:** None

**Expected Response (200 OK):**
```json
{
  "total_tasks": 10,
  "completed_tasks": 5,
  "pending_tasks": 5,
  "overdue_tasks": 2,
  "by_priority": {
    "high": 3,
    "medium": 1,
    "low": 1
  }
}
```

---

## 12. Delete a Task (Requires Auth)

- **Method:** `DELETE`
- **URL:** `http://localhost:5000/api/tasks/1` (replace 1 with your task ID)
- **Headers:** 
  - `Authorization: Bearer <your-token>`
- **Body:** None

**Expected Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

---

## Common Testing Scenarios

### Test 1: User Isolation
1. Register User A and login
2. Create tasks for User A
3. Register User B and login (get new token)
4. Try to get tasks - should only see User B's tasks (empty initially)
5. Try to access User A's task by ID - should get 404

### Test 2: Validation Errors
1. Try creating a task without title:
   ```json
   {
     "description": "No title"
   }
   ```
   Expected: 400 Bad Request with validation errors

2. Try invalid priority:
   ```json
   {
     "title": "Test",
     "priority": "urgent"
   }
   ```
   Expected: 400 Bad Request

### Test 3: Authentication
1. Try to get tasks without Authorization header
   Expected: 401 Unauthorized
2. Try with invalid token
   Expected: 401 Unauthorized

### Test 4: Filtering and Search
1. Create tasks with different statuses, priorities, and categories
2. Test each filter individually
3. Combine multiple filters
4. Test search functionality

---

## Error Testing

### Test Invalid Credentials
```json
{
  "username": "wronguser",
  "password": "wrongpass"
}
```
Expected: 401 Unauthorized

### Test Duplicate Registration
Register the same username/email twice.
Expected: 409 Conflict

### Test Non-existent Task
Get/Update/Delete task ID 999 (doesn't exist).
Expected: 404 Not Found

---

## Tips for Postman

1. **Save Requests:** Save each request in your collection for reuse
2. **Use Variables:** Set `{{base_url}}` and `{{token}}` as environment variables
3. **Tests Tab:** Add automated tests in the "Tests" tab:
   ```javascript
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```
4. **Pre-request Scripts:** Auto-set token from login response
5. **Collection Runner:** Run all requests in sequence
6. **Export Collection:** Share with teammates

---

## Quick Test Checklist

- [ ] Health check works
- [ ] User registration works
- [ ] Login returns token
- [ ] Create task with token
- [ ] Get all tasks
- [ ] Filter by status
- [ ] Filter by priority
- [ ] Search tasks
- [ ] Update task
- [ ] Mark as completed
- [ ] Get statistics
- [ ] Delete task
- [ ] Test without auth (should fail)
- [ ] Test user isolation

---

## Troubleshooting

### Issue: "401 Unauthorized"
- Solution: Check if token is included and starts with "Bearer "

### Issue: "404 Not Found"
- Solution: Verify the URL and task ID exist

### Issue: "Connection refused"
- Solution: Make sure Flask server is running

### Issue: "Validation errors"
- Solution: Check request body matches required format

---

## Next Steps

After testing manually, consider:
1. Export your Postman collection to share
2. Create automated test suites
3. Set up monitoring with Postman Monitor
4. Generate API documentation from Postman
