from selenium import webdriver
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup as bs

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("lang=ko_KR")

driverPath = "../webdriver/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverPath, chrome_options=chrome_options)

keyword = '줄기세포화장품'

# 저장 파일(CSV)
columns = ['newspaper', 'title', 'news_dsc']
crawl_df = pd.DataFrame(columns= columns)
for i in range(4):
    url = 'https://search.naver.com/search.naver?where=news&query='+keyword+'&sort=1&start='+str(i)+'1'

    driver.get(url)

    # 크롤링 페이지 가져오기
    soup = bs(driver.page_source, 'html.parser')
    articles = soup.select('div.news_area')#.get_text().encode('utf-8')

    # 네이버 뉴스만 크롤링 하기( 기사 제목, 신문사, 본문 내용 )

    for article in articles:

        a_list = article.select('div.news_info div.info_group a')
        naver_newspaper = article.select_one('div.news_info div.info_group a.press').get_text()

        if len(a_list) >= 2 :

            naver_article  = a_list[1]
            naver_news_url = naver_article['href']

            # 크롤러 설정
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
            response = requests.get(naver_news_url, headers=headers)
            naverSoup = bs(response.content, 'html.parser')

            # 크롤링
            naver_title = naverSoup.select_one('h3#articleTitle').get_text()
            naver_dsc = naverSoup.select_one('div#articleBodyContents').get_text().encode('euc-kr', 'ignore').decode('euc-kr')
            naver_dsc = naver_dsc.replace('\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가','').replace('\nfunction _flash_removeCallback() {}','')
           
            df_data = {
                "newspaper" : naver_newspaper,
                "title"     : naver_title,
                "news_dsc"  : naver_dsc
            }
            crawl_df = crawl_df.append(df_data, ignore_index=True)

os.makedirs('D:/크롤링 결과물/네이버뉴스/' + keyword , exist_ok=True)
crawl_df.to_csv('D:/크롤링 결과물/네이버뉴스/' + keyword + '/' + keyword +'.csv', encoding='euc-kr')

os.startfile('D:/크롤링 결과물/네이버뉴스/' + keyword)
driver.close()

