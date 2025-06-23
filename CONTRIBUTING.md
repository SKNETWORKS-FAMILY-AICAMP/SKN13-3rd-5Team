# 🛠 Contributing Guidelines

안녕하세요! 이 프로젝트에 관심 가져주셔서 감사합니다. 원활하고 효율적인 협업을 위해 아래의 지침을 꼭 읽고 따라주시기 바랍니다.

---

## 📁 디렉토리 구조

```
root/
├── app.py                       # Streamlit 메인 실행 파일
├── pages/
│   ├── 1_EDA.py                # 탐색적 데이터 분석
│   └── 2_Prediction.py         # 이탈 예측 시뮬레이션
├── requirements.txt             # 의존성 패키지 목록
├── .streamlit/
│   └── config.toml              # Streamlit 배포 설정
├── data/
│   ├── raw/
│   │   └── customer_data.csv    # 원본 데이터
│   └── processed/
│       └── churn_ready.pkl      # 전처리된 데이터 / 모델 입력용
├── model/
│   ├── train_model.py           # 모델 학습 스크립트
│   └── churn_model.pkl          # 학습된 모델 파일
├── utils/
│   └── preprocessing.py         # 전처리 함수 모음
├── notebooks/
│   └── eda.ipynb                # 탐색적 분석 Jupyter 노트북
├── CONTRIBUTING.md              # 기여 가이드라인 (본 문서)
└── README.md                    # 프로젝트 소개
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
