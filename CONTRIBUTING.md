# 🛠 Contributing Guidelines

안녕하세요! 이 프로젝트에 관심 가져주셔서 감사합니다. 원활하고 효율적인 협업을 위해 아래의 지침을 꼭 읽고 따라주시기 바랍니다.

---

## 📁 디렉토리 구조

```
SKN13-3rd-5Team/
├── agent/ # 에이전트 관련 실행 파일 및 메인 로직 포함
│   ├── agent_AgentExecutor.py 
│   ├── agent_langgraph.py
│   └── app.py
├── dataset/ # CSV 데이터 및 데이터 로더 스크립트 포함
│   ├── Busan_heritage_with_detail_and_desc.csv
│   ├── Chungbuk_heritage_with_detail_and_desc.csv
│   ├── Chungnam_heritage_with_detail_and_desc.csv
│   ├── Daegu_heritage_with_detail_and_desc.csv
│   ├── Daejeon_heritage_with_detail_and_desc.csv
│   ├── Gangwon_heritage_with_detail_and_desc.csv
│   ├── Gawngju_heritage_with_detail_and_desc.csv
│   ├── Gyeongbuk_heritage_with_detail_and_desc.csv
│   ├── Gyeonggi_heritage_with_detail_and_desc.csv
│   ├── Gyeongnam_heritage_with_detail_and_desc.csv
│   ├── Incheon_heritage_with_detail_and_desc.csv
│   ├── Jeju_heritage_with_detail_and_desc.csv
│   ├── Jeonbuk_heritage_with_detail_and_desc.csv
│   ├── Jeonnam_heritage_with_detail_and_desc.csv
│   ├── Sejong_heritage_with_detail_and_desc.csv
│   ├── Seoul_heritage_with_detail_and_desc.csv
│   ├── Ulsan_heritage_with_detail_and_desc.csv
│   └── csv_loader.py
├── image/  # 프로젝트 관련 이미지 및 팀원 사진 저장 폴더
│   ├── 국가유산포털.png
│   ├── 김승호_사진.png
│   ├── 김지민_사진.png
│   ├── 박수빈_사진.png
│   ├── 서울숭례문_예시.png
│   ├── 우지훈_사진.png
│   ├── CSV_예시.png
│   └── IMG_9470.jpeg
├── llm_tools/ # LLM 연동 도구 및 API 호출 모듈 포함
│   ├── chat_history_manager.py
│   ├── chat_history_manager2.py
│   ├── get_weather.py
│   ├── google_places.py
│   ├── naver_search.py
│   └── retriever.py
├── notebook/ # Jupyter 노트북 및 실험용 스크립트 저장 폴더
│   ├── 날씨조회_API.ipynb
│   ├── 크롤링_우지훈.ipynb
│   ├── crawling_heritage.py
│   ├── langgraph.ipynb
│   ├── test_csv_loader.ipynb
│   └── test_retriever.ipynb
├── .env # 환경 변수 및 API 키 관리 파일
├── .gitignore # Git 버전 관리에서 제외할 파일 및 폴더 목록
├── app.py
├── CONTRIBUTING.md # 프로젝트 기여 가이드 문서
└── README.md # 프로젝트 소개 및 문서화 파일

```

---

## ✅ 커밋 메시지 규칙

- 커밋 메시지는 작업의 **의도와 변경사항**을 명확히 전달해야 합니다.
- 아래의 prefix를 사용하여 커밋 유형을 명시해주세요.

| 타입 | 설명 |
|------|------|
| `feat:` | 새로운 기능 추가 |
| `fix:` | 버그 수정 |
| `refactor:` | 코드 리팩토링 (기능 변화 없음) |
| `docs:` | 문서 작성/수정 |
| `style:` | 코드 포맷팅 (세미콜론, 들여쓰기 등 비기능 수정) |

**예시:**
```bash
feat: [홍길동] 데이터셋 csv load 기능 추가
fix: [김지민] 전처리 오류 수정
docs: [우지훈] README에 프로젝트 목적 추가
```

---

## 📦 라이브러리 및 의존성 관리

1. **새로운 라이브러리 설치 시:**
```bash
pip install <package-name>
```

2. **설치한 라이브러리를 `requirements.txt`에 반영:**
```bash
pip freeze > requirements.txt
```

3. **다른 팀원이 환경을 맞추는 방법:**
```bash
pip install -r requirements.txt
```

> ⚠️ 가상환경 사용을 권장합니다:  
> `python -m venv venv` → `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)

---

## 🧼 코드 컨벤션

- **Python 버전**: 3.9 이상 권장
- **형식 통일을 위해** `black`, `flake8`, `isort` 등의 사용을 권장합니다.
- PR(Pull Request) 전에는 반드시 코드를 정리하고 커밋해주세요.

---

필요 시 이 문서는 언제든지 업데이트될 수 있습니다. 변경 사항은 PR 또는 팀 회의 등을 통해 공유해주세요.  
좋은 협업을 기대합니다 😊
