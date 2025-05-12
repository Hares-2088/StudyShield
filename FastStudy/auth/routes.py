from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime

from models import User
from .dependencies import get_current_user
from .models import Token, UserCreate, RegisterRequest
from .utils import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
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

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(oauth2_scheme)):
    """
    “Logout” just returns 200. The client should delete its stored token.
    If you want true revocation, you’d save this token’s jti in a blacklist.
    """
    # Example of how you _could_ start a blacklist:
    # jti = decode_jwt_and_get_jti(token)
    # await TokenBlacklist(jti=jti).insert()
    return {"detail": "Successfully logged out"}

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(req: RegisterRequest):
    # 1) Check for existing
    if await User.find_one(User.email == req.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2) Hash & insert
    user_dict = req.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    new_user = await User(**user_dict).create()

    # 3) Issue JWT
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": new_user.email}, expires_delta=expires)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}