from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다.'
    
    # 업로드 디렉토리 생성
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 블루프린트 등록
    from app.routes import auth, main
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(main.bp)
    
    # 데이터베이스 생성
    with app.app_context():
        db.create_all()
    
    return app 