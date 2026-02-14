"""Task CRUD operations"""
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
import logging

logger = logging.getLogger(__name__)


class CRUDTask:
    """CRUD operations for Task model"""
    
    @staticmethod
    def create(db: Session, task_create: TaskCreate, owner_id: int) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            owner_id=owner_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        logger.info(f"Task created: {db_task.id} by user {owner_id}")
        return db_task
    
    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Task | None:
        """Get task by ID"""
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def get_user_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks for a user"""
        return db.query(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks (admin only)"""
        return db.query(Task).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_task_count(db: Session, owner_id: int) -> int:
        """Get task count for a user"""
        return db.query(Task).filter(Task.owner_id == owner_id).count()
    
    @staticmethod
    def update(db: Session, db_task: Task, task_update: TaskUpdate) -> Task:
        """Update a task"""
        update_data = task_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        logger.info(f"Task updated: {db_task.id}")
        return db_task
    
    @staticmethod
    def delete(db: Session, task_id: int) -> bool:
        """Delete a task"""
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
            logger.info(f"Task deleted: {task_id}")
            return True
        return False


crud_task = CRUDTask()
