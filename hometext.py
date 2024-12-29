from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert

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
user_id_field.send_keys("")  # 실제 아이디 입력
user_pw_field.send_keys("")  # 실제 비밀번호 입력

# 7. 로그인 버튼 클릭
login_submit_button = driver.find_element(By.ID, "mf_txppWframe_anchor25")
login_submit_button.click()
time.sleep(2)

# 8. 사업장 전환
business_button = driver.find_element(By.ID,'mf_wfHeader_group1508')
business_button.click()
time.sleep(2)

# 9. 사업자 등록번호 조회
# mf_wfHeader_UTXPPAAA24_wframe_iptBsno
business_num = driver.find_element(By.ID, "mf_wfHeader_UTXPPAAA24_wframe_iptBsno")
business_num.send_keys("")  # 사업자 등록번호
time.sleep(2)
button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'w2trigger') and @value='조회']"))
)
button.click()
time.sleep(2)

# 10 사업자 전환버튼 클릭
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ml5') and contains(@class, 'btn_cm') and contains(@class, 'crud')]"))
)
button.click()



# 현재 윈도우 핸들을 저장
main_window = driver.current_window_handle
# 11 확인버튼 클릭 
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'w2trigger') and contains(@class, 'btn_cm') and contains(@class, 'crud') and @value='확인']"))
)
button.click()

# 새로운 창이 열리기를 기다리기
time.sleep(3)
# 새창으로 전환
new_window = driver.window_handles[-1]
driver.switch_to.window(new_window)
#새 창에서 취소 버튼 클릭
cancel_button = driver.find_element(By.ID, "mf_btnCncl") 
cancel_button.click()
time.sleep(2)
# 취소팝업 처리
alert = Alert(driver)
alert.accept() # 확인버튼으로 팝업 닫힘

# 작업 후 원래 창으로 돌아가기
driver.switch_to.window(main_window)
time.sleep(5)

# 계산서 영수증 카드
link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "mf_wfHeader_wq_uuid_328"))
)
link.click()
time.sleep(2)

# 신용카드 매입
# 요소 선택 (XPath 또는 CSS Selector 사용 가능)
element = driver.find_element(By.XPATH, '//*[@id="menu_46_grp_4608000000"]/a')
element.click()

# 사업용 신용카드 사용내역
element = driver.find_element(By.XPATH, '//*[@id="menuA_46_4608020000"]/a')
element.click()

# 매입세액 공제 확인/변경
element = driver.find_element(By.XPATH, '//*[@id="menuAtag_4608020100"]')
element.click()
time.sleep(2)



radio_button = driver.find_element(By.ID, "mf_txppWframe_rdoSearch_input_2")
driver.execute_script("arguments[0].click();", radio_button)  # 자바스크립트를 이용한 클릭
time.sleep(2)

# #분기별 선택  기본 1분기 ------------------------------
# # 조회
# search_button = driver.find_element(By.XPATH, "//input[@value='조회']")
# search_button.click()
# time.sleep(2)

# #내려 받기
# download_button = driver.find_element(By.XPATH, "//input[@value='내려받기']")
# download_button.click()
# time.sleep(1)

# # 엑셀 선택
# excel_button = driver.find_element(By.XPATH, "//input[@value='엑셀']")
# excel_button.click()
# time.sleep(1)
# # 파일을 받으시겠습니까 -확인
# alert = Alert(driver)
# alert.accept() # 확인버튼으로 팝업 닫힘

# #닫기
# close_button = driver.find_element(By.ID, "mf_txppWframe_UTECRCB055_wframe_trigger10001") 
# close_button.click()
# time.sleep(20)

# Select 객체 생성 (분기 선택 드롭다운)
from selenium.webdriver.support.ui import Select
quarter_select = Select(driver.find_element(By.ID, "mf_txppWframe_selectQrt"))

# 분기별 옵션 반복 처리
for i in range(1, 5):  # 1분기부터 4분기까지
    print(f"Processing {i}분기...")
    
    # 분기 선택
    quarter_select.select_by_visible_text(f"{i}분기")  # 예: "1분기", "2분기" 등
    time.sleep(2)  # 선택 후 페이지 로드 대기
    
    # 조회 버튼 클릭
    search_button = driver.find_element(By.XPATH, "//input[@value='조회']")
    search_button.click()
    time.sleep(2)  # 조회 결과 로드 대기
    
    # 내려받기 버튼 클릭
    download_button = driver.find_element(By.XPATH, "//input[@value='내려받기']")
    download_button.click()
    time.sleep(1)
    
    # 엑셀 선택
    excel_button = driver.find_element(By.XPATH, "//input[@value='엑셀']")
    excel_button.click()
    time.sleep(1)
    
    # 파일 다운로드 확인 팝업 처리
    alert = Alert(driver)
    alert.accept()  # 확인 버튼으로 팝업 닫기
    time.sleep(1)
    
    # 창 닫기
    close_button = driver.find_element(By.ID, "mf_txppWframe_UTECRCB055_wframe_trigger10001")
    close_button.click()
    time.sleep(1)
    
    print(f"{i}분기 data processed successfully.")

