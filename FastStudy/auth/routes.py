from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime

from models import User
from .dependencies import get_current_user
from .models import Token, UserCreate
from .utils import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
async def get_user(email: str):
    return await User.find_one(User.email == email)

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await User.find_one(User.email == form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            # Bad creds → 401
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Good creds → issue token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        # Update last_login
        user.last_login = datetime.utcnow()
        await user.save()

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        # Re-raise 401 or any other HTTPExceptions
        raise
    except Exception:
        # Unexpected error → 500
        logger.exception("💥 Error in /auth/token")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/register")
async def register_user(user_data: dict):  # Changed from UserCreate to dict for flexibility
    existing_user = await User.find_one(User.email == user_data['email'])
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Use our create_user method which handles hashing
    await User.create_user(user_data)
    return {"message": "User created successfully"}

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}