import requests
import datetime
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import chardet
import pandas as pd
import re



def fn_crawl(url):
    data = requests.get(url)
    print(data,url)

    return data.content


def fn_loginPage(driver, id, pw):

    input_id = driver.find_element_by_css_selector("input[name='username']")
    input_pw = driver.find_element_by_css_selector("input[name='password']")
    submit_btn = driver.find_element_by_css_selector("button.sqdOP")

    input_id.send_keys(id)
    input_pw.send_keys(pw)
    submit_btn.click()
    time.sleep(6)

def fn_inputKeyword():

    input_YN = "Y"
    keywords = []

    while input_YN == "Y":

        keyword = input("검색할 키워드 입력 : ")
        keywords.append("#"+keyword)
        input_YN = input("추가할 키워드가 있습니까? (Y or y)")
        input_YN = input_YN.upper()

    return keywords

def fn_doScrollDown(driver,whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break


def fn_searchKeyword(driver,keyword):

    driver.find_element_by_css_selector("input.XTCLo").send_keys(keyword)
    time.sleep(5)
    keyword = keyword.replace("#","")
    driver.find_element_by_xpath("//a[@href='/explore/tags/"+keyword+"/']").click()
    time.sleep(10)

def fn_textCrawl(driver,df,keyword):

    cc = driver.find_elements_by_css_selector('article.KC1QD > div')[1]
    a_list = cc.find_elements_by_css_selector('div > div > div.Nnq7C > div.v1Nh3 > a')

    try :
        if bs(driver.page_source).select('div.bCRRR') is not None :
            driver.find_element_by_css_selector("svg[aria-label='닫기'] > path[fill-rule='evenodd']").click()
    except :
        pass

    try:
        for a_board in a_list:
            a_board.click()
            time.sleep(6)
            soup = bs(driver.page_source, 'html.parser')
            board_enc = soup.select_one('div.C4VMK > span').get_text().encode('utf-8')
            board = board_enc.decode('utf-8')

            board = re.sub("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]", '', board)

            df = df.append({'data': board, 'keyword': keyword}, ignore_index=True)

            driver.find_element_by_css_selector("svg[aria-label='닫기']> path[fill-rule='evenodd']").click()
            time.sleep(1)
    except:
        print("실패")

    return df


def fn_imgCrawl(driver,df,keyword):

    soup = bs(driver.page_source, 'html.parser')
    review = soup.select('article.KC1QD > div')[1]
    image_tags = review.select('div > div > div > a > div > div > img')
    try :
        for image_tag in image_tags:
            df = df.append({'data': image_tag['src'], 'keyword': keyword}, ignore_index=True)
    except KeyError :
        print("src 속성이 없는 게시물(진짜 없는지 나중에 확인)")
    return df