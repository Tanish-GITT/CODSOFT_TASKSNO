# Quick Start Guide - Testing TO-DO List API

## Option 1: Import Postman Collection (Fastest! ⚡)

### Step 1: Start the Server
```bash
cd "TO-DO list backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Step 2: Import Collection into Postman

1. **Open Postman**
2. Click **"Import"** button (top left)
3. Click **"Upload Files"**
4. Select `TODO_API_Postman_Collection.json` from this folder
5. Click **"Import"**

✅ Done! All 13 endpoints are ready to test.

### Step 3: Test the API

**Run requests in this order:**

1. **Health Check** - Verify API is running
2. **Register User** - Creates account
3. **Login** - Gets your JWT token (automatically saved!)
4. **Create Task** - Add your first task
5. **Get All Tasks** - See your tasks
6. Try other endpoints (filter, search, update, delete, stats)

The collection automatically saves your token after login, so authentication works on all task endpoints! 🎉

---

## Option 2: Manual Testing in Postman

Follow the detailed guide in `POSTMAN_TESTING_GUIDE.md`

---

## Testing Checklist

### Basic Flow
- [ ] 1. Start server (`python app.py`)
- [ ] 2. Health check works
- [ ] 3. Register a user
- [ ] 4. Login and get token
- [ ] 5. Create a task
- [ ] 6. Get all tasks
- [ ] 7. Update a task
- [ ] 8. Mark as completed
- [ ] 9. Delete a task

### Advanced Features
- [ ] Filter by status (pending/completed)
- [ ] Filter by priority (low/medium/high)
- [ ] Filter by category
- [ ] Search tasks by text
- [ ] Get task statistics
- [ ] Test pagination

### Security Testing
- [ ] Try task endpoint without token (should fail)
- [ ] Register duplicate username (should fail)
- [ ] Invalid login credentials (should fail)
- [ ] Access another user's task (should fail)

---

## Sample Test Data

Use this data to create diverse tasks for testing:

```json
// Task 1: High priority work task
{
  "title": "Prepare presentation for client meeting",
  "description": "Create slides and demo",
  "priority": "high",
  "category": "Work",
  "due_date": "2026-10-10T14:00:00"
}

// Task 2: Medium priority personal task
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, vegetables",
  "priority": "medium",
  "category": "Personal"
}

// Task 3: Low priority learning
{
  "title": "Learn Docker basics",
  "description": "Complete Docker tutorial",
  "priority": "low",
  "category": "Learning",
  "due_date": "2026-10-20T18:00:00"
}

// Task 4: Already completed
{
  "title": "Setup development environment",
  "description": "Install Python, Flask, and dependencies",
  "status": "completed",
  "priority": "high",
  "category": "Work"
}
```

---

## Quick API Reference

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/health` | GET | No | Check API status |
| `/api/auth/register` | POST | No | Create account |
| `/api/auth/login` | POST | No | Get JWT token |
| `/api/tasks` | POST | Yes | Create task |
| `/api/tasks` | GET | Yes | Get all tasks |
| `/api/tasks/:id` | GET | Yes | Get one task |
| `/api/tasks/:id` | PUT | Yes | Update task |
| `/api/tasks/:id` | DELETE | Yes | Delete task |
| `/api/tasks/:id/complete` | PATCH | Yes | Mark completed |
| `/api/tasks/:id/pending` | PATCH | Yes | Mark pending |
| `/api/tasks/stats` | GET | Yes | Get statistics |

---

## Common Issues & Solutions

### ❌ "Connection refused"
**Solution:** Server not running. Run `python app.py`

### ❌ "401 Unauthorized"
**Solution:** 
- Missing token: Add `Authorization: Bearer <token>` header
- Invalid token: Login again to get fresh token

### ❌ "404 Not Found"
**Solution:** Check URL and task ID are correct

### ❌ "400 Bad Request"
**Solution:** Check request body format and required fields

### ❌ "ModuleNotFoundError"
**Solution:** Install dependencies: `pip install -r requirements.txt`

---

## Pro Tips 💡

1. **Auto-save token**: The imported collection automatically saves your JWT token after login
2. **Use variables**: Collection uses `{{base_url}}` and `{{token}}` variables
3. **Run tests**: Click "Send" to test individual requests
4. **Collection Runner**: Test → Run collection → Run entire flow automatically
5. **View response**: Check the "Body" tab for JSON responses

---

## Next Steps

After basic testing:
1. ✅ Test all filters and search combinations
2. ✅ Create multiple users and verify isolation
3. ✅ Test validation errors (missing fields, invalid data)
4. ✅ Export results and share with team
5. ✅ Set up automated test scripts

---

## Files in This Project

- `README.md` - Complete project documentation
- `POSTMAN_TESTING_GUIDE.md` - Detailed step-by-step testing guide
- `TODO_API_Postman_Collection.json` - Import this into Postman
- `QUICK_START.md` - This file
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies

---

## Support

- Check `README.md` for full API documentation
- Check `POSTMAN_TESTING_GUIDE.md` for detailed testing instructions
- Verify server is running on `http://localhost:5000`

Happy Testing! 🚀
