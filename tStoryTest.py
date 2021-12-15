import sys
import os
import pandas as pd
import numpy as np
import time
import re
import datetime

import requests as requests
import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from csv import writer
from urllib.parse import quote

from blogXpath import Tstory_blog_xpath
from findBlogContents import FindTsotryContents
from reworkBlogContents import ReworkContents
from saveCsv import df_save_csv
from setWebdriver import set_driver as setting_driver

chromedriver_path = '/Applications/chromedriver'
# qText = input("검색어를 입력 해주세요 : ")
qText = "시그 mcx"
start_date = "2020.12.1"  # ex 2021.12.2 or 16 식으로 입력
end_date = "2021.12.15"

csvFileName = f"{qText}_티스토리_{start_date}_{end_date}_url.csv"
mainCsvFileName = f"{qText}_티스토리_{start_date}_{end_date}.csv"

xpath_root = Tstory_blog_xpath()
find_content = FindTsotryContents()  # 크롤링 데이터 탐색 부분
rework_content = ReworkContents()  # 전처리 부분


# def open_site(driver):
#     url = "https://search.daum.net/search?w=blog&f=section&SA=tistory&lpp=10&nil_src=blog&q=" + quote(qText) + "&p=1"
#     driver.get(url)
#     driver.implicitly_wait(10)
#
#     if start_date and end_date != "":
#         driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정
#
#         s_date = driver.find_element_by_xpath(xpath_root.start_date_button)
#         driver.find_element_by_xpath(xpath_root.start_date_button).click()
#         s_date.clear()
#         time.sleep(0.5)
#         for c in start_date:
#             s_date.send_keys(c)
#             time.sleep(0.25)
#
#         click_num = start_date.split(".")[-1]
#         driver.find_element_by_link_text(f"{click_num}").click()
#
#         e_date = driver.find_element_by_xpath(xpath_root.end_date_button)
#         driver.find_element_by_xpath(xpath_root.end_date_button).click()
#         e_date.clear()
#         time.sleep(0.5)
#         for c in end_date:
#             e_date.send_keys(c)
#             time.sleep(0.25)
#
#         click_num = end_date.split(".")[-1]
#         driver.find_element_by_link_text(f"{click_num}").click()
#         driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용
#
#     else:
#         driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정
#         driver.find_element_by_xpath(xpath_root.one_day).click()  # 1일
#         driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용
#     time.sleep(1)
#     driver.find_element_by_xpath(xpath_root.select_blog).click()  # 출처 (블로그 종류)
#     driver.find_element_by_xpath(xpath_root.select_tstory).click()  # 티스토리 선택
#     time.sleep(1)
#
#     return driver


# 검색 결과에 따른 총 페이지 수 파악
def find_page_count(text):
    text = text.split("/")
    page_num = int(text[1].replace("건", "").replace("약", "").replace(",", ""))
    page_count = int(page_num / 10)
    if page_count == 0:
        page_count = 1
    return page_count


# def set_driver(webdriver):
#     window_size = "1200,800"
#     chrome_options = Options()
#     # chrome_options.add_argument('headless')  # 창 안뜨게
#     chrome_options.add_argument(f"--window-size={window_size}")  # 창 사이즈
#     driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
#     driver.implicitly_wait(10)  # seconds
#     url = open_site(driver).current_url
#     driver.implicitly_wait(15)
#     driver.get(url)
#     time.sleep(1)
#
#     return driver, url


def tistory_url_crwaling():
    startTime = time.time()
    # 타이틀, url, 횟수
    return_title_list = []
    return_url_list = []
    count_num = 0

    driver, url = setting_driver(webdriver, 2)  # 셀레니움 드라이버 설정

    page_num_text = driver.find_element_by_xpath(xpath_root.page_all_text).text
    page_count = find_page_count(page_num_text)
    print("총 페이지 : ", page_count)

    if os.path.isfile(csvFileName):
        print("동일 url.csv 파일 존재")
        url_count = pd.read_csv(csvFileName)
        url_start_count = len(url_count)
        # print(url_start_count)
        re_start_page = int(url_start_count / 10) + 1
        if re_start_page != page_count:
            url_1 = url[:102]
            url = url_1 + f"{re_start_page}"
            driver.get(url)
        elif re_start_page >= page_count:
            print("url 수집 완료.csv 파일")
            return csvFileName

    try:
        for page in range(page_count):
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            post_list = soup.findAll("a", class_="f_link_b")
            time.sleep(1)

            for post in post_list:
                post_ti = post.get_text()
                # print(post_ti)
                post_url = post.attrs['href']
                # print(post_url)
                if post_url not in return_url_list:
                    return_title_list.append(post_ti)
                    return_url_list.append(post_url)

                count_num += 1

            # 페이지 변화가 없을때 끝내기 위해서 페이지 확인
            last_page = driver.current_url.split("&")[6]
            last_page = last_page.split('=')[-1]
            # print("last page: ", last_page )
            if last_page != page_count:
                driver.find_element_by_xpath(xpath_root.next_page_button).click()
                print(f"{last_page}에서 다음페이지로")
            time.sleep(0.5)

    except:
        print("크롤링 종료")

    finally:
        endTime = time.time()
        print("링크 크롤링 수 : ", count_num)
        print(f"url 소요시간 : {endTime - startTime:.5f} 초")
        # print("first_df : ", first_df)
        first_df = pd.DataFrame({'title': return_title_list, 'url': return_url_list})
        first_csv = df_save_csv(first_df, csvFileName)
        return first_csv


def main_crawling(data):
    # 셀레니움 설정 옵션
    window_size = "1200,1200"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--window-size={window_size}")

    # 로그 파일 만들어서처리하기
    crawling_count = 0
    pass_count = 0
    # url_load = data  # DateFrame 기준
    url_load = pd.read_csv(csvFileName)
    num_list = len(url_load)

    # 크롤링 한 결과를 담아두는 리스트
    blog_title_list = []
    blog_time_lsit = []
    blog_post_list = []
    blog_url_list = []

    # 제외된 부분 확인을 위한 리스트
    except_idx_list = []
    except_title_list = []
    except_url_list = []

    try:
        for i in range(0, num_list):
            temp_pass_count = pass_count
            url = url_load['url'][i]
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            driver.implicitly_wait(10)

            # 게시글 제목
            title = find_content.find_title(soup)
            driver.implicitly_wait(10)

            # 작성 시간 파악
            wTime = find_content.find_date(soup)
            driver.implicitly_wait(10)

            # 본문 내용
            main_post = find_content.find_main_post(soup)
            driver.implicitly_wait(10)
            # print("text : ", main_post)
            # 해당 url
            blog_url = driver.current_url

            if title != '' and wTime != '' and main_post != '':
                blog_title_list.append(title)
                blog_time_lsit.append(wTime)
                blog_post_list.append(main_post)
                blog_url_list.append(blog_url)
                crawling_count += 1

            else:
                except_idx_list.append(i)
                except_title_list.append(url_load['title'][i])
                except_url_list.append(url_load['url'][i])
                pass_count += 1
                pass
            # driver.close()
            # 일부 빈값에서 중복 입력방지 초기화
            title = ''
            wTime = ''
            main_post = ''
            print(f"메인 크롤링 {crawling_count}회")
            print(f"pass {pass_count}회")
            # print(temp_pass_count)
            if pass_count != temp_pass_count:
                print(f"제외 인덱스 Num : {except_idx_list}")
                print(f"제외 인덱스 title : {except_title_list}")
                print(f"제외 인덱스 url : {except_url_list}")

    except:
        print(f"크롤링 실패. 인덱스 : {i}")
        print(f"제목 : {url_load['title'][i]}, url :  {url_load['url'][i]}")
        except_idx_list.append(i)
        except_title_list.append(url_load['title'][i])
        except_url_list.append(url_load['url'][i])
        pass_count += 1

    finally:
        last_df = pd.DataFrame(
            {'title': blog_title_list, 'date': blog_time_lsit, 'text': blog_post_list, 'url': blog_url_list})
        df_save_csv(last_df, mainCsvFileName)


if __name__ == '__main__':

    startTime = time.time()

    # DateFreme로 동작하는 부분
    first_df = tistory_url_crwaling()
    main_crawling(first_df)

    endTime = time.time()
    print(f"소요시간 : {endTime - startTime:.5f} 초")
