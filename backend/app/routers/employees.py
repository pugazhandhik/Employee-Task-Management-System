from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.config import get_database
from app.models import EmployeeCreate, EmployeeUpdate, EmployeeInDB

router = APIRouter()


def convert_employee_doc(doc: dict) -> dict:
    """Convert MongoDB document to Pydantic-compatible format"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


async def get_employee_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["employees"]


@router.post("/", response_model=EmployeeInDB, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: EmployeeCreate,
    employees_collection=Depends(get_employee_collection),
):
    employee_dict = employee.model_dump()
    employee_dict["created_at"] = datetime.utcnow()
    employee_dict["updated_at"] = datetime.utcnow()
    result = await employees_collection.insert_one(employee_dict)
    created = await employees_collection.find_one({"_id": result.inserted_id})
    return EmployeeInDB(**convert_employee_doc(created))


@router.get("/", response_model=List[EmployeeInDB])
async def list_employees(employees_collection=Depends(get_employee_collection)):
    employees_cursor = employees_collection.find()
    employees = []
    async for doc in employees_cursor:
        employees.append(EmployeeInDB(**convert_employee_doc(doc)))
    return employees


@router.get("/{employee_id}", response_model=EmployeeInDB)
async def get_employee(employee_id: str, employees_collection=Depends(get_employee_collection)):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID")
    employee = await employees_collection.find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return EmployeeInDB(**convert_employee_doc(employee))


@router.put("/{employee_id}", response_model=EmployeeInDB)
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    employees_collection=Depends(get_employee_collection),
):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID")
    update_data = {k: v for k, v in employee_update.model_dump(exclude_unset=True).items()}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
    result = await employees_collection.find_one_and_update(
        {"_id": ObjectId(employee_id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return EmployeeInDB(**convert_employee_doc(result))


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: str, employees_collection=Depends(get_employee_collection)):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID")
    result = await employees_collection.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return None
