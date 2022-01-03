#파이썬 버전 3.8.2 64bit
#파이썬 편집기 VisualStudioCode
#Chrome 버전 83(드라이버 설치 시 버전확인 필수)
#네이버에 로그인 필수!

#전체 코드 흐름
#1. 카페 게시물 리스트 페이지 접속
#2. 전체 게시물 수만큼 페이지 확장
#3. 카페 각 게시물의 url가져오기
#4. 가져온 게시물들의 url각각으로 접속
#5. 데이터 긁어오기(제목, 작성일, 내용)

#이슈사항 네이버 카페가 자동으로 블락을 먹음

from selenium import webdriver #라이브러리 설치(화면 호출 및 타입변환) -> pip install selenium
import requests #라이브러리 설치(url호출) -> pip install requests
from bs4 import BeautifulSoup as bs #라이브러리 설치(타입변환) -> pip install BeautifulSoup
import pyperclip 
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random

#드라이버 경로 설정(회사)
driver = webdriver.Chrome('D:/옥동철 주임/99. 개인 자료/파이썬 크롤링/driver_83/chromedriver.exe')
driver.implicitly_wait(3)

#게시물 url(예시)
#url1 = 'https://m.cafe.naver.com/ca-fe/web/cafes/10197921/articles/23572201?menuid=682&query=한국산업기술대학교&art=aW50ZXJuYWwtY2FmZS1hcnRpY2xlLXJlYWQtaW5DYWZlLXNlYXJjaC1saXN0.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjYWZlVHlwZSI6IkNBRkVfSUQiLCJhcnRpY2xlSWQiOjIzNTcyMjAxLCJpc3N1ZWRBdCI6MTU5MTA5OTk0NjgzMiwiY2FmZUlkIjoxMDE5NzkyMX0._n4labMCFUECo08948_gLVTjpppJkVljtcQDl-74ta8'

#기존 url
url1 = 'https://m.cafe.naver.com/ArticleSearchList.nhn?search.query=산기대&search.menuid=0&search.searchBy=0&search.sortBy=date&search.clubid=10197921&search.option=0&search.defaultValue=1'


driver.get(url1)

#총 게시물 갯수 구하기
soup1 = bs(driver.page_source,'html.parser')
total_num = soup1.find('span','num')
total_num = int(total_num.text)

#버튼을 클릭하는 횟수 구하기
click_num = 0
if total_num%20 == 0:
    click_num = int(total_num/20) - 1
else:
    click_num = int(total_num/20)

#더보기 버튼 클릭
for a in range(click_num):
    #'더보기' 버튼 찾아가기
    driver.find_element_by_xpath("//a[@id='moreButton']").click()
    time.sleep(random.randrange(1,3))

#더보기 버튼이 최대한 확장된 페이지를 불러오기
soup2 = bs(driver.page_source, 'html.parser')
a_list = soup2.find_all('a')

#url을 담을 저장공간
ls = []
for a in a_list:
    #각 게시물들의 url을 가져오기
    a_nm = a.get('href')
#    ls.append(a_nm)
    if a_nm.split('.')[0] == '/ArticleRead':
        #실제 접속할 url로 만들기   
        link = 'https://m.cafe.naver.com'+a_nm 
        ls.append(link)
#print(len(ls))

#데이터를 저장할 txt파일 열기(집)
txt = open('D:/옥동철 주임/99. 개인 자료/파이썬 크롤링/한기대/저장파일/산기대_naver_cafe.txt','r+' , encoding='utf-8')
i = 1
title_sen = ''
date_sen = ''
post_sen = ''
for url2 in ls:
    driver.get(url2)
    time.sleep(random.randrange(1,3))
    # soup3 = bs(driver.page_source, 'html.parser')
    # div=soup3.find('div','ArticleContentWrap')

    session = bs(driver.page_source,'html.parser').find('div','top_readcopy')
    #지속적으로 크롤링을 하였을 때, 네이버 봇이 감지하여 로그인을 해제함
    #로그인창으로 이동하였을 경우를 확인을 하여, 다시 재 로그인
    if session is not None:
        login_id = driver.find_element_by_xpath("//div[@id='id_area']/span[@class='input_box']/input[@class='int']")
        login_pw = driver.find_element_by_xpath("//div[@id='pw_area']/span[@class='input_box']/input[@class='int']")
        login_btn = driver.find_element_by_xpath("//div[@class='btn_login']/input[@class='btn_global']")
        login_id.clear()
        time.sleep(1)
        
        #ID입력
        login_id.click()
        pyperclip.copy('jogary12')
        login_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        #PASSWORD입력
        login_pw.click()
        pyperclip.copy('qzc46002.')
        login_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        login_btn.click()

    #제목 추출
    title = bs(driver.page_source, 'html.parser').find('title')
    driver.implicitly_wait(10)
    print(title.get_text().strip())
    if title is not None:
        title_sen = title.get_text().strip()
    else :
        title_sen = '값이 없습니다.'

    #작성일 추출
    date = bs(driver.page_source, 'html.parser').find('span','date') #div.select('span.date')[0]
    driver.implicitly_wait(10)
    print(date.get_text().strip())
    if date is not None:
        date_sen = date.get_text().strip()
    else :
        date_sen = '값이 없습니다.'

    #내용 추출
    post = bs(driver.page_source, 'html.parser').find('div','post_cont') #div.select('div.post_cont')[0]
    driver.implicitly_wait(10)
    print(post.get_text().strip())
    if post is not None:
        post_sen = post.get_text().strip()
    else :
        post_sen = '값이 없습니다.'
    
    txt.write(str(i)+'|'+title.get_text().strip()+'|'+date.get_text().strip()+'|'+post.get_text().strip()+'\n')
    i = i + 1