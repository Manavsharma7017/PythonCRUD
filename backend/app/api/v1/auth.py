"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.crud.user import crud_user
from app.core.security import create_access_token, create_refresh_token
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}, 400: {"description": "Bad Request"}},
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user with email and password",
)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user"""
    # Check if user already exists
    existing_user = crud_user.get_by_email(db, user_create.email)
    if existing_user:
        logger.warning(f"Registration attempt with already registered email: {user_create.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    user = crud_user.create(db, user_create)
    logger.info(f"New user registered successfully: {user.email} (ID: {user.id})")
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Login with email and password to get JWT tokens",
)
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db),
):
    """Login user and return JWT tokens"""
    # Authenticate user
    user = crud_user.authenticate(db, user_login.email, user_login.password)
    if not user:
        logger.warning(f"Failed login attempt for email: {user_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        logger.warning(f"Login attempt for inactive user: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive",
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email},
    )
    
    logger.info(f"User logged in successfully: {user.email} (ID: {user.id})")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user",
)
def get_me(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user information"""
    return current_user
