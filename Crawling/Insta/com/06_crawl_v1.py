from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd
import datetime
import os

# 크롤링
from libs.crawler import fn_inputKeyword
from libs.crawler import fn_loginPage
from libs.crawler import fn_doScrollDown
from libs.crawler import fn_searchKeyword
from libs.crawler import fn_textCrawl
from libs.crawler import fn_imgCrawl

# 이미지 생성
from libs.urlToImg import download_and_resize_image
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("lang=ko_KR")

driver = webdriver.Chrome(executable_path="../webdriver/chromedriver.exe",chrome_options=chrome_options)

# 로그인에 필요한 계정정보
id = input("인스타 ID를 입력 하시오 : ")
pw = input("인스타 비밀번호를 입력 하시오 : ")
url = "https://www.instagram.com/accounts/login/" #로그인 페이지
driver.get(url) # 주소입력하고 enter
driver.implicitly_wait(10)
fn_loginPage(driver, id, pw)  # 로그인

# 크롤링할 인스타 키워드
keywords = fn_inputKeyword()

crawl_type = input("텍스트(1)/이미지(2) 무엇을 크롤링 하시겠습니까? ")

save_path = input("저장할 Drive는 어디 입니까?") + ":/크롤링 결과물/"
os.makedirs(save_path, exist_ok=True)

for keyword in keywords:

    df = pd.DataFrame(columns=['data', 'keyword'])

    fn_searchKeyword(driver,keyword) #키워드 검색

    num = 0
    while df.count()['data'] <= 10: # 크롤링 갯수 설정
        print(str(datetime.datetime.now()) + "   " + keyword + " " + str(num + 1) + "번째 반복!!")
        if crawl_type == '1' :
            df = fn_textCrawl(driver,df,keyword) # 텍스트 크롤링
        else :
            df = fn_imgCrawl(driver,df,keyword) # 이미지 크롤링
        print(df.count()['data'])
        fn_doScrollDown(driver, 5)

        time.sleep(5)
        num = num + 1

    print(keyword + " 성공!!")
    # 저장할 파일 생성
    save_csv_path = save_path+keyword+'.csv'
    df.to_csv(save_csv_path, encoding='euc-kr')
    time.sleep(2)

driver.close()

if(int(crawl_type) == 2):
    if (input("이미지 파일로 만드시겠습니까?(Y/y)").upper() == "Y" ):
        for keyword in keywords:
            save_image_path = save_path + "/" + keyword + "/"
            os.makedirs(save_image_path, exist_ok=True)

            csv = pd.read_csv(save_path+keyword+'.csv', encoding='euc-kr')
            i   = 0
            for url in csv['data']:
                i += 1
                crawl_image_path = save_image_path + keyword + str(i) + '.jpg'
                downloaded_image_path = download_and_resize_image(url, crawl_image_path, 680, 256, False)

os.startfile(save_path)