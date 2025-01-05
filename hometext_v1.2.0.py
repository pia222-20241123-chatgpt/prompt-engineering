from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import os, shutil
from selenium.webdriver.support.ui import Select
from datetime import datetime
def main():
    # ############################## 주의사항 #################################
    # 크롬브라이져의 설정에서 파일 다운로드 경로를 "d:/temp_download" 설정한다
    # bs_lists.csv  파일의 구조
    # id psw business_no
    # abc password 123456789
    # 와 같이 구성되어야 함
    # ########################################################################

    # 1. ChromeDriver 경로 설정
    driver_path = "D:/gmail/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # 정확한 chromedriver 경로
    service = Service(driver_path)

    # 1. ChromeDriver 설정 (다운로드 경로 지정)
    download_path = "C:/Users/user/Downloads"
    # if not os.path.exists(download_path):
    #     os.makedirs(download_path)  # 다운로드 폴더가 없으면 생성

    # 사업자 번호별 디렉터리 경로
    business_base_dir = "D:/hometax_business"
    if not os.path.exists(business_base_dir):
        os.makedirs(business_base_dir)

    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    # 4. 홈텍스 페이지 열기 (쿠키 적용하려면 먼저 해당 도메인에 접근해야 함)
    driver.get("https://hometax.go.kr/")
    time.sleep(2)  # 페이지가 완전히 로드될 때까지 잠시 대기

    # 아이디패스워드 및 사업자 번호
    df = pd.read_csv('d:/bs_lists.csv')

    # 이전 아이디를 추적하고, 변경 시점을 출력
    previous_id = None
    for idx,current_id in enumerate(df.id):                
        psw = df.loc[idx,'psw']
        if previous_id != current_id:  # 아이디가 변경되었을 때
            # previous_id 값이 있으면 현재 로그인되어 있으나 아이디가 변경되었음
            if previous_id is not None:
                # 로그아웃
                logout_button = driver.find_element(By.ID, 'mf_wfHeader_group1503')
                logout_button.click()                
                time.sleep(2)
                # 확인버튼
                logout_button = driver.find_element(By.XPATH, "//*[contains(@class, 'w2trigger') and contains(@class, 'btn_cm') and contains(@class, 'crud')]")
                logout_button.click()
                time.sleep(2)
            # 새로운 아이디로 로그인  #####################################################
            # 로그인 버튼 클릭
            button = driver.find_element(By.ID, "mf_wfHeader_group1503")  # 로그인 버튼의 ID
            button.click()
            time.sleep(2)  # 페이지 로딩 대기

            # 5. 아이디 로그인 버튼 클릭
            button = driver.find_element(By.ID, "mf_txppWframe_anchor15")  # "아이디 로그인" 버튼의 ID
            button.click()
            time.sleep(2)  # 클릭 후 페이지 로딩 대기

            # 6. 아이디와 비밀번호 입력
            user_id_field = driver.find_element(By.ID, "mf_txppWframe_iptUserId")
            user_pw_field = driver.find_element(By.ID, "mf_txppWframe_iptUserPw")

            # 아이디와 비밀번호를 입력 (여기에 실제 값을 넣어야 함)    
            user_id_field.send_keys(current_id)  # 실제 아이디 입력
            user_pw_field.send_keys(psw)  # 실제 비밀번호 입력

            # 7. 로그인 버튼 클릭
            button = driver.find_element(By.ID, "mf_txppWframe_anchor25")
            button.click()
            time.sleep(2)    
            # 이전아이디 = 현재 아이디
            previous_id = current_id      

               
       

        for idx,bs_no in enumerate(df.business_no):
            try:
                # 8. 사업장 전환
                button = driver.find_element(By.ID,'mf_wfHeader_group1508')
                button.click()
                time.sleep(2)

                # 사업자 전환        
                button = driver.find_element(By.ID, "mf_wfHeader_UTXPPAAA24_wframe_iptBsno")    
                button.send_keys(bs_no)  # 사업자 등록번호
                time.sleep(2)
                button = driver.find_element(By.XPATH, "//input[contains(@class, 'w2trigger') and @value='조회']")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # 10 사업자 전환버튼 클릭
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ml5') and contains(@class, 'btn_cm') and contains(@class, 'crud')]"))
                )
                button.click()

                if idx == 0:  # 최초 진입시만
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
                    
                else:
                    # 11 확인버튼 클릭 
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'w2trigger') and contains(@class, 'btn_cm') and contains(@class, 'crud') and @value='확인']"))
                    )
                    button.click()

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

                # 년도 선택
                year_select = Select(driver.find_element(By.ID, "mf_txppWframe_selectYear"))
                current_year = datetime.now().year
                years = [current_year-1,current_year]
                for year in years:
                    year_select.select_by_visible_text(f"{year}년")
                    time.sleep(2)


                    # Select 객체 생성 (분기 선택 드롭다운)    
                    quarter_select = Select(driver.find_element(By.ID, "mf_txppWframe_selectQrt"))

                    # 분기별 옵션 반복 처리
                    for i in range(1, 5):  # 1분기부터 4분기까지
                        try:
                            print(f"Processing {i}분기...")
                            # 분기 선택
                            quarter_select.select_by_visible_text(f"{i}분기")  # 예: "1분기", "2분기" 등
                            time.sleep(2)  # 선택 후 페이지 로드 대기
                            
                            # 조회 버튼 클릭
                            search_button = driver.find_element(By.ID, "mf_txppWframe_btnSearch")
                            search_button.click()
                            time.sleep(2)  # 조회 결과 로드 대기
                            
                            # 내려받기 버튼 클릭
                            download_button = driver.find_element(By.XPATH, "//input[@value='내려받기']")
                            download_button.click()
                            time.sleep(2)
                            
                            # 엑셀 선택
                            excel_button = driver.find_element(By.XPATH, "//input[@value='엑셀']")
                            excel_button.click()
                            time.sleep(2)
                            
                            # 파일 다운로드 확인 팝업 처리
                            alert = Alert(driver)
                            alert.accept()  # 확인 버튼으로 팝업 닫기
                            time.sleep(5)  # 다운로드 대기
                            
                            # 최신 다운로드된 파일 경로 확인
                            download_path='C:/Users/user/Downloads'
                            downloaded_files = [os.path.join(download_path, f) for f in os.listdir(download_path)]    
                            
                            # 최신 파일 찾기 (다운로드 시간 기준 정렬)
                            downloaded_files.sort(key=os.path.getmtime, reverse=True)
                            original_file = downloaded_files[0]  # 가장 최근 파일
                            print(f"Latest downloaded file: {original_file}")

                            # 사업자 번호별 디렉터리로 이동        
                            business_base_dir = 'D:/hometax_business'
                            business_dir = os.path.join(business_base_dir, str(bs_no) )  # 사업자 번호 디렉터리
                            if not os.path.exists(business_dir):
                                os.makedirs(business_dir)  # 사업자 디렉터리가 없으면 생성
                            
                            # 새 파일 이름 설정    
                            new_file = os.path.join(business_dir, f"{bs_no}_{year}_{i}분기.xlsx")
                            shutil.move(original_file, new_file)  # 파일 이동 및 이름 변경
                            print(f"Saved file: {new_file}")
                            
                            # 창 닫기
                            close_button = driver.find_element(By.ID, "mf_txppWframe_UTECRCB055_wframe_trigger10001")
                            close_button.click()
                            time.sleep(1)

                            print(f"{i}분기 data processed successfully.")
                        except Exception as e:
                            print(f'분기 에러 {e}')

                    time.sleep(2)
            except Exception as e:
                print(f'전체 에러 {e}')
    # 메일 for end ##################################################
    driver.quit()  # 작업 완료 후 브라우저 종료

if __name__ == "__main__":
    main()
