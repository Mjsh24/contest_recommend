from flask import Blueprint, render_template, request, jsonify
from .models import get_contests_from_db, get_all_reviews
from .db_utils import get_db_connection
import pymysql
from datetime import datetime
from config import DB_CONFIG

import re  # 정규표현식 모듈 추가

def parse_total_prize(value):
    """ total_prize 문자열을 숫자로 변환하는 함수 """
    if not value:
        return None
    
    value = value.replace(',', '').replace(' ', '')

    # ~ 있으면 앞쪽 값만
    if '~' in value:
        value = value.split('~')[0]

    # 숫자 + 단위 매칭
    match = re.match(r'(\d+)(천|만)?', value)
    if not match:
        return None

    num, unit = match.groups()
    num = int(num)

    if unit == '천':
        return num * 1000
    elif unit == '만':
        return num * 10000
    else:
        return num

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main.html')

@main_bp.route('/input')
def input_page():
    nickname = request.args.get('nickname', '')
    return render_template('input.html', nickname=nickname)


@main_bp.route('/recommend', methods=['POST'])
def recommend():
    nickname = request.form.get('nickname', '')
    description = request.form.get('description', '')
    category = request.form.get('category', '')  # 여기서 미리 받아야 함
    targets = request.form.getlist('target')     # 대상 여러 개 받기
    prize_range = request.form.get('prize_range', '')  # 상금 범위

    table_name = category.replace('/', '_')
    contests = get_contests_from_db(table_name)  # DB에서 contest 리스트 불러오기

    recommended = []  

    for contest in contests:
        
        match_category = (contest['category'] == category)

        match_target = (not targets) or (contest['qual'] in targets)

        match_prize = True
        if prize_range:
            total_prize_raw = contest.get('total_prize', '')
            total_prize = parse_total_prize(total_prize_raw)

            if prize_range == '기타':
                # 숫자로 변환이 아예 안 되는 경우만 기타로 분류
                if total_prize is not None:
                    continue
            else:
                # 상금 범위 필터링
                if total_prize is None:
                    continue

                if prize_range == '150만원 이하':
                    match_prize = (total_prize <= 150)
                elif prize_range == '300만원 이하':
                    match_prize = (total_prize <= 300)
                elif prize_range == '500만원 이하':
                    match_prize = (total_prize <= 500)
                elif prize_range == '500만원 초과':
                    match_prize = (total_prize > 500)

        if match_category and match_target and match_prize:
            recommended.append(contest)
        
        # D-Day 계산
        today = datetime.today().date()
    for contest in recommended:
        deadline_str = contest.get('register_end')
        if deadline_str:
            try:
                if isinstance(deadline_str, str):
                    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                else:
                    deadline_date = deadline_str
                d_day = (deadline_date - today).days
                contest['d_day'] = d_day
            except Exception as e:
                contest['d_day'] = None
        else:
            contest['d_day'] = None

    return render_template('result.html', contests=recommended, name=nickname)


@main_bp.route('/review')
def review_page():
    nickname = request.args.get('nickname', '')
    try:
        reviews = get_all_reviews()
        return render_template('review.html', nickname=nickname, reviews=reviews)
    except Exception as e:
        print('리뷰 불러오기 에러:', e)
        return render_template('review.html', nickname=nickname, reviews=[])

@main_bp.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        nickname = request.form.get('nickname', '')
        review_content = request.form.get('review_content', '')

        connection = get_db_connection()
        cursor = connection.cursor()

        sql = "INSERT INTO review (nickname, review_content) VALUES (%s, %s)"
        cursor.execute(sql, (nickname, review_content))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': '리뷰 저장에 성공했습니다.'})
    except Exception as e:
        print('리뷰 저장 에러:', e)
        return jsonify({'message': '리뷰 저장에 실패했습니다.'}), 500


@main_bp.route('/load_reviews', methods=['GET'])
def load_reviews():
    try:
        reviews = get_all_reviews()
        return jsonify(reviews)  # 리뷰 리스트를 JSON 형태로 반환
    except Exception as e:
        print('리뷰 목록 불러오기 에러:', e)
        return jsonify([])

# # 민우님 모델
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# @main_bp.route('/model/result_base', methods=['GET'])
# def result_base():
#     nickname = request.args.get('nickname')
#     keyword = request.args.get('keyword')
    
#     # 여기서는 예를 들어 모델1이 아니라 모델2 방식으로 처리하는 부분이 들어간다!
#     # 일단 더미로 keyword를 그대로 넘겨주는 것도 가능해

#     return render_template('result_base.html', nickname=nickname, keyword=keyword)

# @main_bp.route('/model/result_transfer', methods=['GET'])
# def result_transfer():
#     nickname = request.args.get('nickname')
#     keyword = request.args.get('keyword')
    
#     contests = get_recommended_contests(keyword)
    
#     # 여기에 모델 예측 코드 넣기
#     return render_template('result_transfer.html', nickname=nickname, keyword=keyword)




# ### test ## 
# @main_bp.route('/test-db')
# def test_db_connection():
#     try:
#         connection = pymysql.connect(
#             host=DB_CONFIG['host'],
#             user=DB_CONFIG['user'],
#             password=DB_CONFIG['password'],
#             database=DB_CONFIG['database'],
#             port=DB_CONFIG['port'],
#             charset=DB_CONFIG['charset']
#         )
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM 광고_마케팅")
#         result = cursor.fetchall()
#         cursor.close()
#         connection.close()
#         return f"DB 연결 성공! 데이터: {result}"
#     except Exception as e:
#         return f"DB 연결 실패! 에러: {e}"
