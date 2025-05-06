import pymysql
from config import DB_CONFIG  # DB 연결 정보 불러오기

# DB에서 공모전 데이터 가져오기
def get_contests_from_db(table_name):
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port'],
        charset=DB_CONFIG['charset']
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # 테이블명을 직접 넣어서 쿼리
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    contests = cursor.fetchall()

    cursor.close()
    connection.close()

    return contests

def get_all_reviews():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port'],
        charset=DB_CONFIG['charset']
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # 리뷰 테이블에서 데이터 가져오기
    query = "SELECT * FROM review ORDER BY created_at DESC"
    cursor.execute(query)

    reviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return reviews


