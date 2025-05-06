# Flask 인스턴스 생성 
# Flask 앱 생성, routes.py 연결하는 역할

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # DB 연결 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    # 라우트 등록
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    from app.recommender.model_routes import model_bp
    app.register_blueprint(model_bp)
    
    return app