from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # 업로드 폴더 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(host='0.0.0.0', port=5001, debug=True) 