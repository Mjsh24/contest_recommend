# --------------------------------------------------------------------------------
# Flask Framework에서 WebServer 설정 파일
# - 파일명 : config.py
# - MySQL DB 사용 버전
# --------------------------------------------------------------------------------

# 모듈 로딩
import os

# 데이터베이스 연결 정보
DB_CONFIG = {
    'user': 'root',          # MySQL 사용자 이름
    'password': '1234',  # MySQL 비밀번호
    'host': 'localhost',      # MySQL 호스트 (로컬 개발 환경이면 localhost)
    'port': 3306,             # MySQL 기본 포트 (3306)
    'database': 'contest',    # 사용할 데이터베이스 이름
    'charset': 'utf8mb4'      # 문자셋 설정
}

# SQLAlchemy 연결 URI (MySQL)
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'


# 기타 SQLAlchemy 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False # 변경 사항 감지 (단, True하면 오류 많이 뜸)