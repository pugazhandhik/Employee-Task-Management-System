# Employee Task Management System

A full-stack web application for managing employees and their tasks, built with FastAPI (backend) and HTML/CSS/JavaScript (frontend), using MongoDB as the database.

## 🚀 Features

- **Employee Management**
  - Create, read, update, delete employees
  - Track employee status (active/inactive)
  - Store employee position and contact info

- **Task Management**
  - Create, read, update, delete tasks
  - Assign tasks to employees
  - Track task status (pending, in progress, done)
  - Add descriptions to tasks

- **Modern UI**
  - Clean, responsive design
  - Card-based layout
  - Real-time notifications
  - Smooth animations

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- MongoDB (via Motor async driver)
- Pydantic for data validation
- Uvicorn ASGI server

**Frontend:**
- HTML5
- CSS3 (with custom variables and animations)
- Vanilla JavaScript (ES6+)
- Fetch API for HTTP requests

**Database:**
- MongoDB Atlas (cloud database)

## 📁 Project Structure

```
ProU/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── employees.py    # Employee CRUD endpoints
│   │   │   └── tasks.py        # Task CRUD endpoints
│   │   ├── config.py           # Database configuration
│   │   └── models.py           # Pydantic models
│   ├── main.py                 # FastAPI app entry point
│   ├── seed_data.py            # Sample data seeder
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile               # Render deployment config
│   ├── build.sh               # Build script for deployment
│   └── README.md              # Backend documentation
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── styles.css             # Styling
│   └── app.js                 # Frontend logic
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file
```

## 🏃 Local Development

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- Modern web browser

### Backend Setup

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the server:**
```bash
uvicorn main:app --reload
```

Backend will be available at: `http://127.0.0.1:8000`
API docs: `http://127.0.0.1:8000/docs`

### Frontend Setup

1. **Open the frontend:**
```bash
cd frontend
start index.html  # Windows
open index.html   # Mac
```

Or use a simple HTTP server:
```bash
python -m http.server 8080
```
Then visit: `http://localhost:8080`

## 📡 API Endpoints

### Employees
- `GET /employees/` - List all employees
- `POST /employees/` - Create new employee
- `GET /employees/{id}` - Get employee by ID
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Delete employee

### Tasks
- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for Render, Netlify, and Vercel.

**Quick Steps:**
1. Push code to GitHub
2. Deploy backend on Render
3. Deploy frontend on Netlify/Vercel
4. Update frontend API URL
5. Configure CORS

## 🔧 Configuration

**Environment Variables (backend):**
- `MONGODB_URI` - MongoDB connection string
- `DATABASE_NAME` - Database name (default: `employee_task_db`)
- `PORT` - Server port (set by Render)

**Frontend Configuration:**
Update `API_URL` in `frontend/app.js` to your deployed backend URL.

## 📝 Sample Data

The `seed_data.py` script creates:
- 2 sample employees (Alice Johnson, Bob Smith)
- 2 sample tasks assigned to them

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🐛 Troubleshooting

**Backend won't start:**
- Check MongoDB connection string
- Ensure all dependencies are installed
- Check Python version (3.11+)

**CORS errors:**
- Update `allow_origins` in `backend/main.py`
- Add your frontend URL to allowed origins

**Data not showing:**
- Verify backend is running
- Check browser console for errors
- Ensure MongoDB Atlas allows connections from your IP

