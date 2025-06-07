from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config
import os
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    logger.info("애플리케이션 초기화 시작...")
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다.'
    
    # 업로드 디렉토리 생성
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    logger.info(f"업로드 디렉토리 생성됨: {app.config['UPLOAD_FOLDER']}")
    
    # 블루프린트 등록
    from app.routes import auth, main
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(main.bp)
    logger.info("블루프린트 등록 완료")
    
    # 데이터베이스 생성
    with app.app_context():
        db.create_all()
        logger.info("데이터베이스 테이블 생성 완료")
    
    logger.info("애플리케이션 초기화 완료")
    return app 