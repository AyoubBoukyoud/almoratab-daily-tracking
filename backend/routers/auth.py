from fastapi import APIRouter, Depends, Response, Cookie, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.database import get_db
from core.security import decode_token, create_access_token
from dependencies.auth import require_admin, get_current_user
from schemas.auth import LoginRequest, TokenResponse, UserTokenPayload
from schemas.user import UserCreate, UserOut
from services.auth_service import authenticate_user
from models.user import User
from core.security import hash_password
from jose import JWTError
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    token_response, refresh_token = await authenticate_user(db, payload)

    # Set refresh token as HTTP-only cookie
    cookie_expires = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=cookie_expires,
        expires=cookie_expires,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        path="/auth" # Limit cookie access to the auth routes
    )
    return token_response

@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    try:
        payload = decode_token(refresh_token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # Query the user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    new_access_token = create_access_token(user.id, user.role)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "user": UserTokenPayload(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            role=user.role
        )
    }

@router.post("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="refresh_token", path="/auth")
    return {"detail": "Logged out successfully"}

@router.post("/register", response_model=UserOut, dependencies=[Depends(require_admin)])
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    hashed_pass = hash_password(payload.password)
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hashed_pass,
        role=payload.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
