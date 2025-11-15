from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import employees, tasks

app = FastAPI(title="Employee Task Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
async def root():
    return {"message": "Employee Task Management API is running"}
