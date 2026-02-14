"""Task Pydantic schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default="", max_length=5000)


class TaskCreate(TaskBase):
    """Task creation schema"""
    pass


class TaskUpdate(BaseModel):
    """Task update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)


class TaskResponse(TaskBase):
    """Task response schema"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Task list response schema"""
    tasks: list[TaskResponse]
    total: int
