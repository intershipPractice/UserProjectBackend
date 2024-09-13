from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .crud import get_user, create_user, create_tokens_in_body, authenticate_refresh_token, authenticate_user
from .schemas import Token, UserBase
from .auth import AuthJWT
from app.logger import logger
from app.models import get_db

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

@router.post("/token", summary="새로운 엑세스 토큰 반환", status_code=200, response_model=Token)
async def get_token(Authorize: AuthJWT = Depends()):
    """
        새로운 엑세스 토큰 반환
    """
    token = authenticate_refresh_token(Authorize=Authorize)
    return JSONResponse({"access_token": token})


@router.post("/signup", summary="회원가입", status_code=201, response_model=None)
async def signup(
                email: str = Form(..., description="User email"),
                password: str = Form(..., description="User password"),
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db),
                ):
    """
        회원가입
    """
    user = get_user(db, email)
    logger.info(user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 아이디입니다.",
        )
    userForm = UserBase(email=email, password=password)
    
    result = create_user(db, userForm)
    
    logger.info(result)
    if result != True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=result)
    
    response_body = create_tokens_in_body(email, Authorize)
    response_body["message"] = "유저 생성 및 로그인 성공"
    return JSONResponse(content=response_body, status_code=201)


@router.post("/login", summary="로그인", status_code=200, response_model=None)
async def login(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
        로그인
    """
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호나 아이디가 틀렸습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    response_body = create_tokens_in_body(email, Authorize)
    logger.info(f"엑세스 토큰 기간 {Authorize._access_token_expires}")
    logger.info(f"디버깅용 유저 정보 {user.email}")
    return JSONResponse(status_code=200, content=response_body)
