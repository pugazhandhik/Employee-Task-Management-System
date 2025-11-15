# Employee Task Management Backend

FastAPI + MongoDB backend for managing Employees and Tasks.

## Setup

From the `backend` folder:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`.

## Seed Sample Data

```bash
python seed_data.py
```

This will create sample employees and tasks in your MongoDB database.

## Main Endpoints

### Employees
- `GET /employees/` – list employees
- `POST /employees/` – create employee
- `GET /employees/{employee_id}` – get single employee
- `PUT /employees/{employee_id}` – update employee
- `DELETE /employees/{employee_id}` – delete employee

### Tasks
- `GET /tasks/` – list tasks
- `POST /tasks/` – create task
- `GET /tasks/{task_id}` – get single task
- `PUT /tasks/{task_id}` – update task
- `DELETE /tasks/{task_id}` – delete task
