"""Endpoints регистрации, входа и текущего пользователя."""

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead
from app.services.auth import AuthError, AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, session: DbSession) -> UserRead:
    try:
        user = await AuthService(session).register(data.email, data.password)
    except AuthError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: DbSession) -> TokenResponse:
    try:
        token = await AuthService(session).login(data.email, data.password)
    except AuthError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUser) -> UserRead:
    return UserRead.model_validate(current_user)
