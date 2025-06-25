from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pymysql
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime

# ====================== 기본 세팅 ======================
BASE_URL = "https://www.heritage.go.kr"
LIST_URL_TEMPLATE = BASE_URL + "/heri/cul/culSelectRegionList.do"

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1111',
    database='project3',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()

# ====================== 유틸 함수 ======================
def parse_date(text):
    for fmt in ('%Y.%m.%d', '%Y-%m-%d'):
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except:
            continue
    return None

def clean_text(text):
    return ' '.join(text.replace('\xa0', ' ').split()).strip() if text else None

def strip_session_id(url):
    parsed = urlparse(url)
    clean_path = parsed.path.split(';')[0]
    return urljoin(BASE_URL, clean_path + '?' + parsed.query)

def crawl_detail(detail_url):
    try:
        driver.get(detail_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.hschDetail_tit")))
    except TimeoutException:
        print(f"[❌ ERROR] 상세 페이지 로딩 실패: {detail_url}")
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title_box = soup.select_one('div.hschDetail_tit')
    name = chinese_name = classification = None

    if title_box:
        strong = title_box.find('strong')
        if strong:
            full_name = strong.get_text(strip=True)
            if '(' in full_name and ')' in full_name:
                name, chinese_name = full_name.split('(', 1)
                name = name.strip()
                chinese_name = chinese_name.replace(')', '').strip()
            else:
                name = full_name.strip()

        p_tag = title_box.find('p')
        if p_tag:
            classification = p_tag.get_text(strip=True)

    table = soup.select_one('table.hschDi_info')
    designation_date = era = location = owner = manager = None

    if table:
        for row in table.select('tr'):
            th = row.find('th')
            td = row.find('td')
            if not th or not td:
                continue
            key = th.get_text(strip=True)
            val = clean_text(td.get_text())
            if key == '지정(등록)일':
                designation_date = parse_date(val)
            elif key == '시 대':
                era = val
            elif key == '소 재 지':
                location = val
            elif key.startswith('소유자'):
                owner = val
            elif key.startswith('관리자'):
                manager = val

    content_tag = soup.select_one('div.hschDetail_tab_cont .krExp')
    content = clean_text(content_tag.get_text()) if content_tag else None

    return {
        'name': name,
        'chinese_name': chinese_name,
        'classification': classification,
        'designation_date': designation_date,
        'era': era,
        'location': location,
        'owner': owner,
        'manager': manager,
        'content': content
    }

# ====================== MAIN LOOP ======================
try:
    for page in range(1, 117):
        print(f"🌐 크롤링 페이지 {page} ...")
        driver.get(LIST_URL_TEMPLATE + f"?s_kdcd=00&s_ctcd=34&culPageNo={page}&region=2")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.tbl.type_1.c_result tbody tr"))
            )
        except TimeoutException:
            print(f"[❌ ERROR] 리스트 페이지 {page} 로딩 실패")
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.select('table.tbl.type_1.c_result tbody tr')

        if not rows:
            print(f"[❌ WARNING] 리스트 페이지 {page}에 데이터 없음.")
            continue

        for row in rows:
            detail_link_tag = row.select_one('td:nth-of-type(3) a')
            if not detail_link_tag:
                print("[❌ WARNING] 상세 링크 없음, 스킵")
                continue

            raw_href = detail_link_tag.get('href')
            detail_url = strip_session_id(raw_href)

            print(f"DEBUG DETAIL CLEAN URL: {detail_url}")
            data = crawl_detail(detail_url)

            if not data or not data.get('name'):
                print(f"[❌ ERROR] 이름 없는 데이터, 스킵: {detail_url}")
                continue

            try:
                cursor.execute("""
                    INSERT INTO heritage (
                        name, chinese_name, classification, designation_number,
                        era, location, owner, manager, designation_date, content
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['name'], data['chinese_name'], data['classification'], None,
                    data['era'], data['location'], data['owner'], data['manager'],
                    data['designation_date'], data['content']
                ))
                print(f"✅ INSERT 완료: {data['name']}")
                time.sleep(0.5)

            except Exception as e:
                print(f"[❌ DB ERROR] {data['name']} - {e}")

except Exception as e:
    print(f"[❌ MAIN LOOP ERROR] {e}")

finally:
    cursor.close()
    conn.close()
    driver.quit()
    print("🎉 모든 크롤링 완료.")
