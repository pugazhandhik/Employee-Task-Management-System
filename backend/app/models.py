from typing import Optional, Annotated, Any
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer, ConfigDict


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


# Using str as base with custom validator
PyObjectId = Annotated[str, Field(...)]


class EmployeeBase(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    position: Optional[str] = None
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeInDB(EmployeeBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer('id')
    def serialize_id(self, value: Any) -> str:
        return str(value)


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in_progress, done
    employee_id: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    employee_id: Optional[str] = None


class TaskInDB(TaskBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer('id', 'employee_id')
    def serialize_ids(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        return str(value)
