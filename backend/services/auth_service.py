from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_password, create_access_token, create_refresh_token
from models.user import User
from schemas.auth import LoginRequest, TokenResponse, UserTokenPayload
from fastapi import HTTPException, status

async def authenticate_user(
    db: AsyncSession,
    payload: LoginRequest
) -> TokenResponse:
    # Query user by email
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated"
        )

    # Create access and refresh tokens
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)

    # Prepare response
    token_response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserTokenPayload(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            role=user.role
        )
    )
    # We will attach the refresh token as a cookie in the router.
    # Return both the response schema and the refresh token
    return token_response, refresh_token
