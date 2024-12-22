from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
from bs4 import BeautifulSoup

# 1. ChromeDriver 경로 설정
driver_path = "D:/gmail/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # 정확한 chromedriver 경로
service = Service(driver_path)

# 2. Chrome 옵션 설정
options = Options()
# options.add_argument("--headless")  # 헤드리스 모드 (브라우저를 띄우지 않고 실행)

# 3. ChromeDriver 초기화
driver = webdriver.Chrome(service=service, options=options)

# 4. 네이버 페이지 열기 (쿠키 적용하려면 먼저 해당 도메인에 접근해야 함)
driver.get("https://mail.naver.com/")
time.sleep(15)  # 페이지가 완전히 로드될 때까지 잠시 대기

# 5. 쿠키 로드하여 추가
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))  # 쿠키 파일이 있다면 로드
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("쿠키 로드 완료!")

except FileNotFoundError:
    print("쿠키 파일이 없습니다. 로그인 후 쿠키를 저장해 주세요.")

# 6. 쿠키 적용 후 페이지 새로 고침 (로그인 상태로 유지)
driver.refresh()

# 7. 웹 페이지에서 크롤링 시작 (예: 이메일 제목 추출)
time.sleep(5)  # 페이지가 완전히 로드될 때까지 대기

# 페이지 HTML을 BeautifulSoup으로 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 이메일 리스트 추출
mail_list = soup.select('li.mail_item')

# 각 메일 항목별로 정보 추출
mail_data = []

for item in mail_list:
    try:
        # 보낸 사람
        sender = item.select_one('.button_sender').text.strip() if item.select_one('.button_sender') else '발신자 없음'
        
        # 발신자가 '네이버'인 경우 제외        
        if sender == '보낸 사람네이버':
            continue
        
        # 제목
        title = item.select_one('.mail_title .text').text.strip() if item.select_one('.mail_title .text') else '제목 없음'
        
        # 본문 링크 클릭하여 본문 내용 추출
        mail_link = item.select_one('.mail_title_link')['href'] if item.select_one('.mail_title_link') else None
        if mail_link:
            # 본문 링크를 클릭하여 메일 내용 가져오기
            driver.get("https://mail.naver.com" + mail_link)  # 메일 상세 페이지로 이동
            time.sleep(3)  # 페이지 로딩 대기
            mail_page_html = driver.page_source
            mail_page_soup = BeautifulSoup(mail_page_html, 'html.parser')
            
            # 메일 본문 내용 추출 (본문 영역 선택)
            body_content = mail_page_soup.select_one('#mail_read_scroll_view > div > div.mail_view_body > div > div')  # 메일 본문 영역
            body_text = body_content.text.strip() if body_content else '본문 없음'
        else:
            body_text = '본문 없음'
        
        # 메일 데이터를 CSV 리스트에 추가
        mail_data.append([sender, title, body_text])
        
        # 결과 출력 (선택 사항)
        print(f"보낸 사람: {sender}")
        print(f"제목: {title}")
        print(f"내용: {body_text}")
        print("-" * 50)  # 구분선

    except Exception as e:
        print(f"오류 발생: {e}")

# 8. pandas를 이용해 CSV로 저장
df = pd.DataFrame(mail_data, columns=["보낸 사람", "제목", "내용"])
df.to_csv('email_data.csv', index=False, encoding='utf-8-sig')  # 'utf-8-sig'로 저장하여 한글 깨짐 방지

print("CSV 파일 저장 완료!")

# 9. 브라우저 종료
driver.quit()
