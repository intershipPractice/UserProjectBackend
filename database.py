# import time
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import configs
# from logger import logger  
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# SQLALCHEMY_DATABASE_URL = configs.sql_alchemy_database_url

# # 데이터베이스 엔진 생성
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def connect_to_db(retries=5, delay=5):
#     """
#     데이터베이스에 연결을 계속 시도하는 함수.
    
#     :param retries: 최대 재시도 횟수 (기본값: 5)
#     :param delay: 재시도 사이의 대기 시간 (초, 기본값: 5)
#     :return: 성공하면 True, 실패하면 False
#     """
#     attempt = 0
#     while attempt < retries:
#         try:
#             # 데이터베이스에 연결 시도
#             db = SessionLocal()
#             db.execute("SELECT 1")  # 간단한 쿼리 실행
#             logger.info("데이터베이스 연결 성공!")
#             db.close()
#             return True
#         except Exception as e:
#             attempt += 1
#             logger.warning(f"데이터베이스 연결 실패. {attempt}/{retries} 시도 중... 에러: {e}")
#             time.sleep(delay)
    
#     logger.error("데이터베이스 연결 실패. 최대 시도 횟수 초과.")
#     return False

# if __name__ == "__main__":
#     connected = connect_to_db()
#     if connected:
#         logger.info("애플리케이션 시작 준비 완료.")
#     else:
#         logger.critical("애플리케이션을 종료합니다.")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configs

SQLALCHEMY_DATABASE_URL = configs.sql_alchemy_database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()