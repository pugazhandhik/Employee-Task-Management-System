from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.config import get_database
from app.models import TaskCreate, TaskUpdate, TaskInDB

router = APIRouter()


def convert_task_doc(doc: dict) -> dict:
    """Convert MongoDB document to Pydantic-compatible format"""
    if doc:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        if "employee_id" in doc and doc["employee_id"]:
            doc["employee_id"] = str(doc["employee_id"])
    return doc


async def get_task_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["tasks"]


@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    tasks_collection=Depends(get_task_collection),
):
    task_dict = task.model_dump()
    # Convert employee_id string to ObjectId if present
    if task_dict.get("employee_id"):
        if not ObjectId.is_valid(task_dict["employee_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID")
        task_dict["employee_id"] = ObjectId(task_dict["employee_id"])
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    result = await tasks_collection.insert_one(task_dict)
    created = await tasks_collection.find_one({"_id": result.inserted_id})
    return TaskInDB(**convert_task_doc(created))


@router.get("/", response_model=List[TaskInDB])
async def list_tasks(tasks_collection=Depends(get_task_collection)):
    tasks_cursor = tasks_collection.find()
    tasks = []
    async for doc in tasks_cursor:
        tasks.append(TaskInDB(**convert_task_doc(doc)))
    return tasks


@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str, tasks_collection=Depends(get_task_collection)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID")
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskInDB(**convert_task_doc(task))


@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    tasks_collection=Depends(get_task_collection),
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID")
    update_data = {k: v for k, v in task_update.model_dump(exclude_unset=True).items()}
    # Convert employee_id string to ObjectId if present in update
    if "employee_id" in update_data and update_data["employee_id"]:
        if not ObjectId.is_valid(update_data["employee_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID")
        update_data["employee_id"] = ObjectId(update_data["employee_id"])
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
    result = await tasks_collection.find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskInDB(**convert_task_doc(result))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, tasks_collection=Depends(get_task_collection)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID")
    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None
