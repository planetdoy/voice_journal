from app import create_app
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    # 업로드 폴더 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        logger.info(f"업로드 폴더 생성됨: {app.config['UPLOAD_FOLDER']}")
    
    logger.info("애플리케이션 시작...")
    app.run(host='127.0.0.1', port=8080, debug=True) 