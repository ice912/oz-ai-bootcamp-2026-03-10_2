from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Body, HTTPException, status
from sqlalchemy import select

from auth.password import hash_password, verify_password
from database.connection import engine, get_session
from database.orm import Base, User
from request import SignUpRequest, LogInRequest
from response import UserResponse

@asynccontextmanager
async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/users",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,)
async def signup_handler(
    body: SignUpRequest = Body(...),
    session = Depends(get_session),
):
# email 중복 검사
    stmt = select(User).where(User.email == body.email)
    user: User | None = await session.scalar(stmt)

    if user:
        raise HTTPException(status_code=409, detail="email already exists")

    # 새로운 유저 데이터 추가 & 비밀번호 해싱(hashing)
    new_user = User(
        email=body.email, 
        password_hash=hash_password(plain_password=body.password),
    )
    #새로운 유저 데이터 추가
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

@app.post(
    "/users/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_handler(
    body: LogInRequest = Body(...),
    session = Depends(get_session),
):
    stmt = select(User).where(User.email == body.email)
    user: User | None = await session.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    verified = verify_password(plain_password=body.password, password_hash=user.password_hash)

# 1. 'if' 문 뒤에 콜론(:) 추가
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")

    # [중요] return은 'if not verified'와 동일한 세로 라인에 있어야 합니다.
    return {"result": "ok"}





