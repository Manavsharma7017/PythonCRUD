"""User CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.logger import get_logger

logger = get_logger(__name__)


class CRUDUser:
    """CRUD operations for User model"""
    
    @staticmethod
    def create(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        try:
            hashed_password = get_password_hash(user_create.password)
            db_user = User(
                email=user_create.email,
                full_name=user_create.full_name,
                hashed_password=hashed_password,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created: {db_user.email}")
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating user {user_create.email}: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating user {user_create.email}: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, db_user: User, user_update: UserUpdate) -> User:
        """Update a user"""
        try:
            update_data = user_update.model_dump(exclude_unset=True)
            
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            
            for field, value in update_data.items():
                setattr(db_user, field, value)
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User updated: {db_user.email}")
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error updating user {db_user.email}: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error updating user {db_user.email}: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete a user"""
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                logger.info(f"User deleted: {user_id}")
                return True
            logger.warning(f"Attempted to delete non-existent user: {user_id}")
            return False
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error deleting user {user_id}: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error deleting user {user_id}: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        """Authenticate user by email and password"""
        user = CRUDUser.get_by_email(db, email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user


crud_user = CRUDUser()
