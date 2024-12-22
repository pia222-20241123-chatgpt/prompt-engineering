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

# 4. 홈텍스 페이지 열기 (쿠키 적용하려면 먼저 해당 도메인에 접근해야 함)
driver.get("https://hometax.go.kr/")
time.sleep(2)  # 페이지가 완전히 로드될 때까지 잠시 대기

# 로그인 버튼 클릭
login_button = driver.find_element(By.ID, "mf_wfHeader_group1503")  # 로그인 버튼의 ID
login_button.click()
time.sleep(2)  # 페이지 로딩 대기

# 5. 아이디 로그인 버튼 클릭
login_button = driver.find_element(By.ID, "mf_txppWframe_anchor15")  # "아이디 로그인" 버튼의 ID
login_button.click()
time.sleep(2)  # 클릭 후 페이지 로딩 대기

# 6. 아이디와 비밀번호 입력
user_id_field = driver.find_element(By.ID, "mf_txppWframe_iptUserId")
user_pw_field = driver.find_element(By.ID, "mf_txppWframe_iptUserPw")

# 아이디와 비밀번호를 입력 (여기에 실제 값을 넣어야 함)
user_id_field.send_keys("your id")  # 실제 아이디 입력
user_pw_field.send_keys("your password")  # 실제 비밀번호 입력

# 7. 로그인 버튼 클릭
login_submit_button = driver.find_element(By.ID, "mf_txppWframe_anchor25")
login_submit_button.click()
time.sleep(10) # 확인하기 위해서.