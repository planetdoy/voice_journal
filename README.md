# MVP 프로젝트

이 프로젝트는 FastAPI와 SQLAlchemy를 사용한 백엔드 API 서버입니다.

## 기술 스택

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (데이터베이스 마이그레이션)

## 시작하기

### 필수 요구사항

- Python 3.8 이상
- PostgreSQL 데이터베이스

### 설치 방법

1. 저장소를 클론합니다:
```bash
git clone [repository-url]
cd mvp
```

2. 가상환경을 생성하고 활성화합니다:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정:
`.env` 파일을 생성하고 다음 변수들을 설정합니다:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

5. 데이터베이스 마이그레이션:
```bash
alembic upgrade head
```

6. 서버 실행:
```bash
uvicorn app.main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API에 접근할 수 있습니다.

## API 문서

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 프로젝트 구조

```
mvp/
├── alembic/              # 데이터베이스 마이그레이션
├── app/
│   ├── api/             # API 엔드포인트
│   ├── core/            # 핵심 설정
│   ├── models/          # 데이터베이스 모델
│   └── schemas/         # Pydantic 스키마
├── tests/               # 테스트 파일
├── .env                 # 환경 변수
├── requirements.txt     # 프로젝트 의존성
└── README.md           # 프로젝트 문서
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 