"""Task API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.crud.task import crud_task
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.models.task import Task
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}},
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the current user",
)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new task"""
    task = crud_task.create(db, task_create, current_user.id)
    return task


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get tasks",
    description="Get user's tasks or all tasks if admin",
)
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get tasks"""
    if current_user.role == "admin":
        tasks = crud_task.get_all(db, skip=skip, limit=limit)
        total = db.query(Task).count()
    else:
        tasks = crud_task.get_user_tasks(db, current_user.id, skip=skip, limit=limit)
        total = crud_task.get_user_task_count(db, current_user.id)
    
    return TaskListResponse(tasks=tasks, total=total)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Get a specific task by ID",
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get task by ID"""
    task = crud_task.get_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check ownership or admin
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update a task (owner or admin only)",
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a task"""
    task = crud_task.get_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check ownership or admin
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    task = crud_task.update(db, task, task_update)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task (owner or admin only)",
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a task"""
    task = crud_task.get_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check ownership or admin
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    crud_task.delete(db, task_id)
    return None
