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
📚 여행나래는 사용자의 질문에 문화유산 정보를 설명하고, 날짜·날씨·위치에 따라 맞춤형 여행 코스를 추천해주는 LLM 기반 대화형 큐레이터 챗봇입니다.
해설가 없이도 문화유산을 쉽고 즐겁게 탐방할 수 있도록 돕습니다.


#### ⭐ 프로젝트 필요성
📌 1. 기존 문화유산 정보의 한계
     
     대부분 정적이고 일방향적으로 제공되어,
     
     현장에서 궁금한 점이 생겨도 즉시 설명을 듣기 어렵고,
     
     사용자가 직접 검색하고 해석해야 하는 불편함이 존재합니다.

📌 2. 여행·데이트 시의 실질적인 어려움
     
     낯선 장소에서 코스를 직접 계획하는 것 자체가 부담스럽고,

     날씨, 거리, 동선 등을 고려하다 보면 계획이 복잡해집니다.

     필요한 정보가 흩어져 있어 여러 앱을 번갈아 확인해야 하는 번거로움도 있습니다.



🎯 "AI 큐레이터가 내 상황에 맞춰 안내해준다면?"

    자연어로 질문하면 문화유산 해설을 즉시 제공
    
    날씨와 날짜, 위치 정보를 반영해 👉 나에게 딱 맞는 코스 추천까지 가능

    " 해설가 + 여행 가이드 역할을 동시에 수행 "

> 대화형 AI **여행나래**🤖 는
단순 정보 제공을 넘어,
문화유산을 더 쉽게, 더 즐겁게 경험할 수 있는 새로운 방식입니다.



#### 🎯 프로젝트 목표

1. 문화유산 해설 챗봇 구현

     사용자가 자연어로 질문하면, 해당 문화유산에 대한 정보를 대화 형태로 제공

2. 날씨·일정 기반 여행 코스 추천

     사용자의 여행 날짜, 위치, 날씨 정보를 반영해 맞춤형 방문 코스 설계

3. 대화형 인터페이스를 통한 사용자 편의성 향상

     복잡한 검색 없이, 누구나 쉽게 질문하고 정보를 얻을 수 있는 경험 제공

4. 공공데이터와 LLM을 연계한 실용적인 AI 서비스 개발

     문화 콘텐츠에 특화된 대화형 AI 큐레이터의 실제 활용 가능성 탐색



<hr>

### 3️⃣ 기술 스택
| 항목                | 내용 |
|---------------------|------|
| **Language**        | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Development**     | ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white) |
| **Crawler**         | ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white)<br>![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white) |
| **Embedding**       | ![TEXT-EMBEDDING-3-LARGE](https://img.shields.io/badge/TEXT--EMBEDDING--3--LARGE-353535?style=for-the-badge&logoColor=white) |
| **LLM Model**       | ![gpt-4.1](https://img.shields.io/badge/gpt--4.1-4B91FF?style=for-the-badge&logo=openai&logoColor=white) |
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
```python
def crawl_heritage_data():
    base_url = "https://www.heritage.go.kr"
    url_template = (url_template)
    header = ['연번', '종목', '명칭', '소재지', '관리자', '상세페이지링크']
    all_data = []

    for page in range(1, page):
        url = url_template.format(page=page)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.select("#txt > table > tbody > tr"):
            tds = row.find_all('td')
            if len(tds) < 6:
                continue
            num = tds[0].get_text(strip=True)
            category = tds[1].get_text(strip=True)
            name = tds[2].get_text(strip=True)
            location = tds[4].get_text(strip=True)
            manager = tds[5].get_text(strip=True)
            a_tag = tds[2].find('a')
            link = urllib.parse.urljoin(base_url, a_tag['href']) if a_tag and a_tag.has_attr("href") else ''
            all_data.append([num, category, name, location, manager, link])
        time.sleep(0.5)
```
### 코드 주요 변수 및 동작 설명

- **base_url**  
  상세페이지 링크를 만들 때 기준이 되는 사이트 주소입니다.

- **url_template**  
  각 페이지별로 접근할 수 있는 URL 형식입니다.  
  (예시: `"https://www.heritage.go.kr/heri/cul/culSelectRegionList.do?culPageNo={page}&region=2"`)

- **header**  
  CSV 파일의 첫 번째 줄에 들어갈 컬럼명 리스트입니다.

- **all_data**  
  긁어온 모든 데이터를 저장할 빈 리스트입니다.

- **num**  
  연번(번호)

- **category**  
  종목(문화재 종류)

- **name**  
  명칭(문화재 이름)

- **location**  
  소재지(위치)

- **manager**  
  관리자(관리 기관)

- **반복 동작 설명**  
  1페이지부터 마지막 페이지까지 반복하면서,
  각 페이지의 표에서 한 줄씩 원하는 정보를 뽑아 리스트에 저장합니다.

- **time.sleep(0.5)**  
  너무 빠른 요청으로 서버에 부담을 주지 않도록,  
  각 페이지마다 0.5초씩 잠깐 쉬어줍니다.

+ 전처리 관련 작성해야됨 (연변삭제)



### 7️⃣ 테스트 계획 및 결과 보고서

### 8️⃣ 성능 개선 노력

### 9️⃣ 추후 개선점

### 🔍 한 줄 회고
