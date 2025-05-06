from flask import Blueprint, request, render_template,jsonify
from sqlalchemy import select
from datetime import datetime
from .model.base_model_utils import *
from app.db_utils import get_db_connection
from app.recommender.transfer_model import TransferRecommender
from app import db
import json


model_bp = Blueprint('model', __name__, url_prefix='/model')

# 추천 모델 준비
recommender = None
corpus_data = []
@model_bp.route('/')
def index():
    return '바보'
def calculate_d_day(end_date):
    """
    마감일로부터 남은 일수 계산 (D-Day 형식)
    """
    today = datetime.today().date()
    d_day = (end_date - today).days
    if d_day > 0:
        return f"D-{d_day}"
    elif d_day == 0:
        return "D-Day"
    else:
        return "마감"

@model_bp.route('/result_base', methods=['POST'])
def model_recommend():
    data = request.get_json()  # json으로 받기
    nickname = data.get('nickname')
    keyword = data.get('keyword')
    contests = data.get('contests')
    model=Predict_name(contests,r'C:\Users\KDP-28-\Desktop\KDT\WEB_FLASK\project_root\app\recommender\model\word2vec.model')
    recommended_contests=model.pred(keyword,number=5)
    print(recommended_contests)
    if not contests or not keyword:
        return "Invalid input", 400
    # 결과를 템플릿에 넘기기
    return render_template('result_base.html', recommended_contests=recommended_contests, name=nickname)

@model_bp.route('/result_transfer', methods=['POST'])
def model_transfer():
    global recommender, corpus_data
    data = request.get_json()  # json으로 받기
    # # 1. 사용자 입력 받기
    # field = request.form.get('field')
    # keyword = request.form.get('keyword', '').strip()

    # if not field or not keyword:
    #     return "분야와 키워드를 모두 입력해주세요.", 400

    # # 2. 테이블 데이터 불러오기 (pymysql로)
    # contests = get_contests_from_table(field)
    today = datetime.today().date()
    nickname = data.get('nickname')
    keyword = data.get('keyword')
    contests = data.get('contests')
    
    # 3. 마감일 필터링 및 설명(description) 추출
    # valid_contests = []
    # descriptions = []

    # for contest in contests:
    #     end_date_str = contest.get('register_end')

    #     if end_date_str:
    #         try:
    #             end_date = datetime.strptime(str(end_date_str), "%Y-%m-%d").date()
    #         except Exception:
    #             end_date = None
    #     else:
    #         end_date = None

    #     if not end_date or end_date >= today:
    #         valid_contests.append(contest)
    #         descriptions.append(contest.get('description', ''))

    # 4. 추천기 초기화
    # if recommender is None or corpus_data != descriptions:
    #     corpus_data = descriptions
    #     recommender = TransferRecommender(descriptions)

    # # 5. 추천 실행
    # recommendations = recommender.recommend(keyword)

    # # 6. 추천 결과 매칭 + D-Day 추가
    # recommended_contests = []
    # for idx, score in recommendations:
    #     if idx < len(valid_contests):
    #         contest = valid_contests[idx]
    #         contest['score'] = round(float(score), 3)

    #         end_date_str = contest.get('register_end')
    #         if end_date_str:
    #             contest['d_day'] = calculate_d_day(str(end_date_str))
    #         else:
    #             contest['d_day'] = "일정 미정"

    #         recommended_contests.append(contest)

    # # 7. 추천 결과를 점수 순으로 정렬
    # recommended_contests = sorted(recommended_contests, key=lambda x: x.get('score', 0), reverse=True)
    recom=TransferRecommender(contests)
    recommended_contests=recom.recommend(keyword)
    # 8. 결과 전달
    return render_template(
        'result_transfer.html',
        recommended_contests=recommended_contests,
        name=nickname
        # keyword=keyword,
        # field=field
    )
