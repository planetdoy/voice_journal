# Voice Journal

음성 파일을 텍스트로 변환하여 일기처럼 기록할 수 있는 웹 애플리케이션입니다.

## 주요 기능

- 음성 파일 업로드 및 텍스트 변환
  - 지원 형식: MP3, WAV, M4A, OGG
  - 최대 파일 크기: 16MB
- 사용자 인증 시스템
  - 회원가입 및 로그인
  - 이메일 인증
  - 비밀번호 재설정
- 변환 이력 관리
  - 변환된 텍스트 저장
  - 이력 조회 및 삭제
- 일일 사용량 제한
  - 무료 사용자: 하루 3회
  - 프리미엄 사용자: 하루 10회

## 기술 스택

- Backend
  - Python 3.8+
  - Flask
  - PostgreSQL
  - OpenAI Whisper
- Frontend
  - HTML5
  - CSS3 (Bootstrap 5)
  - JavaScript
- 기타
  - Flask-Mail (이메일 인증)
  - PyJWT (토큰 기반 인증)
  - Gunicorn (WSGI 서버)

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/planetdoy/voice_journal.git
cd voice_journal
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정합니다:
```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/voice_journal
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
JWT_SECRET_KEY=your_jwt_secret_key
```

5. 데이터베이스 초기화
```bash
flask db upgrade
```

6. 애플리케이션 실행
```bash
# 개발 환경
python run.py

# 프로덕션 환경
gunicorn run:app
```

## 배포 방법 (Render.com)

1. Render.com 계정 생성 및 로그인

2. PostgreSQL 데이터베이스 생성
   - "New +" > "PostgreSQL" 선택
   - 데이터베이스 설정
   - 생성된 데이터베이스 URL 복사

3. 웹 서비스 생성
   - "New +" > "Web Service" 선택
   - GitHub 저장소 연결
   - 다음 설정으로 구성:
     - Name: voice-journal
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn run:app`
     - Plan: Free

4. 환경 변수 설정
   - DATABASE_URL: PostgreSQL 데이터베이스 URL
   - 기타 필요한 환경 변수 설정

5. 배포 완료 후 자동으로 서비스 시작

## 사용 방법

1. 회원가입 및 로그인
   - 이메일 인증이 필요합니다
   - 비밀번호를 잊어버린 경우 재설정 가능

2. 음성 파일 업로드
   - 드래그 앤 드롭 또는 파일 선택
   - 지원되는 형식: MP3, WAV, M4A, OGG
   - 최대 파일 크기: 16MB

3. 변환 결과 확인
   - 변환이 완료되면 자동으로 이력 페이지로 이동
   - 변환된 텍스트 확인 및 관리

## 라이선스

MIT License

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 