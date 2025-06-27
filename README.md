###### SKN13_3rd_5TEAM

# 임 시

## 🏷️ 목 차

1️⃣ [팀 소개](#1️⃣-팀-소개)

2️⃣ [프리뷰](#2️⃣-프리뷰)

3️⃣ [기술 스택](#3️⃣-기술-스택)

4️⃣ [시스템 아키텍처](#4️⃣-시스템-아키텍처)

5️⃣ [업무 분류 체계](#5️⃣-업무-분류-체계)

6️⃣ [수집한 데이터 및 전처리 요약](#6️⃣-수집한-데이터-및-전처리-요약)

7️⃣ [테스트 계획 및 결과 보고서](#7️⃣-테스트-계획-및-결과-보고서)

8️⃣ [성능 개선 노력](#8️⃣-성능-개선-노력) 

9️⃣ [추후 개선점](#9️⃣-추후-개선점)

🔍 [한 줄 회고](#🔍한-줄-회고고) 

## 주제 

### 1️⃣ 팀 소개
 ### 팀 명 : 여행 나래
#### 🗓️ 개발 기간
> 2025.06.27 ~ 2025.06.30
### 👥 팀원
<table>
  <tr>
    <td align="center">
      <img src="image/임.png" width="100"/><br/>우삣삐
    </td>
    <td align="center">
      <img src="image/시.png" width="100"/><br/>박삣삐
    </td>
    <td align="center">
      <img src="image/사.png" width="100"/><br/>승삣삐
    </td>
    <td align="center">
      <img src="image/진.png" width="100"/><br/>민삣비
    </td>
  </tr>
</table>

   
### 2️⃣ 프리뷰

#### 📖 프로젝트 소개  
데이터코스 추천 챗봇 "📚**여행 나래**"는 사용자의 관심사, 목표, 수준에 맞는 데이터 분야 학습 경로를 자동으로 설계해 주는 LLM 기반 챗봇입니다.  
사용자는 챗봇에게 질문하거나 목표를 입력하면, 챗봇이 공공데이터와 내장 템플릿을 활용해 맞춤형 데이터 학습 코스를 추천해줍니다.

#### ⭐ 프로젝트 필요성

<table>
  <tr>
    <td>데이터 분야 진입 장벽</td>
    <td>데이터 분석, 인공지능 등 데이터 분야에 처음 입문하는 사람들은 방대한 자료와 다양한 학습 경로 중 어디서부터 시작해야 할지 어려움을 겪음</td>
  </tr>
  <tr>
    <td>비효율적인 자료 탐색</td>
    <td>인터넷에 흩어진 수많은 강의와 자료를 직접 비교·선택해야 하므로, 시간과 노력이 많이 소요됨</td>
  </tr>
</table>

#### 🎯 프로젝트 목표

<table>
  <tr>
    <td>맞춤형 데이터코스 챗봇 구현</td>
    <td>사용자의 목표, 관심사, 수준을 분석하여 최적의 데이터 학습 경로를 자동 추천</td>
  </tr>
  <tr>
    <td>공공데이터 기반 추천</td>
    <td>공공데이터포털 및 오픈 강의 데이터를 활용해 신뢰성 높은 학습 자료를 추천</td>
  </tr>
  <tr>
    <td>개인화 및 진도 관리</td>
    <td>사용자별 학습 진도 추적과 피드백을 통해 지속적인 동기부여와 학습 효과 극대화</td>
  </tr>
</table>

<hr>

### 3️⃣ 기술 스택
| 항목                | 내용 |
|---------------------|------|
| **Language**        | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Development**     | ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white) |
| **Crawler**         | ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white)<br>![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white) |
| **Embedding**       | ![TEXT-EMBEDDING-3-LARGE](https://img.shields.io/badge/TEXT--EMBEDDING--3--LARGE-353535?style=for-the-badge&logoColor=white) |
| **LLM Model**       | ![gpt-4.1](https://img.shields.io/badge/gpt--4.0-4B91FF?style=for-the-badge&logo=openai&logoColor=white) |
| **Collaboration Tool** | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) |
| **Vector DB**| ![Chroma](https://img.shields.io/badge/Chroma-ff5c83?style=for-the-badge&logo=databricks&logoColor=white) |


### 4️⃣ 시스템 아키텍처

![diagram](https://github.com/user-attachments/assets/f3a87011-9285-41a3-9932-b20db7992b11)

1. 질문 입력
→ 사용자가 데이터코스 추천 챗봇에 관심사, 목표, 수준 등 학습 관련 질문이나 요청을 입력합니다.

2. 문서 검색
→ 챗봇은 사용자의 질문을 분석하여 관련 학습 자료, 공공데이터 API, 내장 코스 템플릿 등에서 임베딩을 생성하고, FAISS 등의 벡터 검색 엔진을 통해 유사한 학습 경로 및 자료를 검색합니다.

3. Prompt 구성
→ 검색된 학습 자료와 사용자 프로필 정보를 바탕으로 LLM에게 전달할 Prompt를 구성하여 개인화된 학습 경로 추천 요청을 만듭니다.

4. 모델 응답 생성
→ Fine-Tuning된 LLM 또는 Retrieval-Augmented Generation 구조의 모델이 Prompt를 받아 최적의 데이터코스 추천 답변을 생성합니다.

생성된 답변을 User에게 반환
→ 생성된 맞춤형 학습 경로 및 추천 결과가 사용자에게 대화형으로 전달되어 학습 계획 수립에 도움을 줍니다.


### 5️⃣ 업무 분류 체계

| 작업 명             | 시작일 | 종료일 | 담당자                | 산출물                 | 의존 작업           |
|------------------|:------:|:------:|-------------------|----------------------|------------------|
| 프로젝트 주제 선정    | 06-27 | 06-30 | ALL                | 없음                  | 없음              |
| 크롤링           | 06-27 | 06-30 | ALL                 | CSV                    | Streamlit 작업     |
| API 찾기        | 06-27 | 06-30 | 홍길동 김순자 기가차드 | 없음                | Streamlit 작업     |
| 데이터 - DB 연동           | 06-27 | 06-30 | 홍길동 김순자 기가차드 | Chroma_db        | 없음              |
| Streamlit 화면 설계 | 06-27 | 06-30 | 홍길동 김순자 기가차드| 설계파일<br>WEB 화면     | 없음              |
| Streamlit-DB 연동  | 06-27 | 06-30 | 홍길동 김순자 기가차드| DB 테이블              | Streamlit 화면     |
| Streamlit 화면 구현 | 06-27 | 06-30 | 홍길동 김순자 기가차드 | Streamlit 화면         | 크롤링<br>데이터 수집 |
| 코드 취합           | 06-27 | 06-30 | 홍길동 김순자 기가차드 | Web, DB 데이터         | 크롤링<br>데이터 수집 |
| README.md 작성     | 06-27 | 06-30 | 홍길동 김순자 기가차드 | GitHub README.md      | GitHub            |
| 최종 점검           | 06-27 | 06-30 | 홍길동 김순자 기가차드 | 없음                  | 없음              |



### 6️⃣ 수집한 데이터 및 전처리 요약
`사진넣고 수정예정`

### 7️⃣ 테스트 계획 및 결과 보고서

### 8️⃣ 성능 개선 노력

### 9️⃣ 추후 개선점

### 🔍 한 줄 회고
