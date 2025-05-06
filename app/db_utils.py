# app/db_utils.py

import pymysql
from config import DB_CONFIG

def get_db_connection():
    """MySQL 커넥션 생성"""
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port'],
        charset=DB_CONFIG['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def get_contests_from_table(table_name):
    """특정 테이블에서 공모전 리스트 가져오기"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = f"SELECT * FROM `{table_name}`"  # 테이블명은 안전하게 백틱(`)으로 감싸줌
        cursor.execute(query)
        contests = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return contests
