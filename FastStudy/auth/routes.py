from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.params import Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from fastapi import Response

from jose import jwt

from models import User
from .dependencies import get_current_user
from .models import Token, UserCreate, RegisterRequest
from .utils import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, SECRET_KEY, ALGORITHM
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
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        user = await User.find_one(User.email == form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token  = create_access_token(data={"sub": user.email},    expires_delta=timedelta(minutes=30))
        refresh_token = create_access_token(data={"sub": user.email},    expires_delta=timedelta(days=7))

        # Now we can set a cookie on the response:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,       # set to False in dev if you’re not on HTTPS
            samesite="none",    # adjust per your needs
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception:
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

@router.post(
  "/refresh",
  response_model=Token,
  summary="Refresh access_token using the httponly refresh_token cookie"
)
async def refresh_token(
  refresh_token: Optional[str] = Cookie(None, alias="refresh_token")
):
  if not refresh_token:
    raise HTTPException(401, "Missing refresh token")
  payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
  email = payload.get("sub")
  if not email:
    raise HTTPException(401, "Invalid token")
  user = await User.find_one(User.email == email)
  if not user:
    raise HTTPException(401, "Unknown user")
  access_token = create_access_token(
    data={"sub": email},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  return {"access_token": access_token, "token_type": "bearer"}
