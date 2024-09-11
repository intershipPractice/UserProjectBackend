from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import models
from database import engine
from sqlalchemy.exc import OperationalError
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",    # 또는 "http://localhost:5173"
]
def connect_to_db_with_retry(retries=5, delay=5):
    """
    MySQL에 연결을 재시도하는 함수.
    
    :param retries: 최대 재시도 횟수 (기본값: 5)
    :param delay: 재시도 사이의 대기 시간 (초, 기본값: 5)
    :return: 연결 성공 시 True, 실패 시 False
    """
    attempt = 0
    while attempt < retries:
        try:
            # 데이터베이스 연결 시도
            connection = engine.connect()
            connection.close()
            print("MySQL 데이터베이스 연결 성공!")
            return True
        except OperationalError as e:
            attempt += 1
            print(f"데이터베이스 연결 실패, {attempt}/{retries} 재시도 중... 에러: {e}")
            time.sleep(delay)
    
    print("데이터베이스 연결 실패. 최대 시도 횟수 초과.")
    return False

# FastAPI 이벤트: 애플리케이션이 시작할 때 MySQL 연결 시도
@app.on_event("startup")
async def startup_event():
    connected = connect_to_db_with_retry(retries=10, delay=5)  # 10번 시도, 5초 대기
    if not connected:
        raise RuntimeError("MySQL에 연결할 수 없어 서버를 시작할 수 없습니다.")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}

