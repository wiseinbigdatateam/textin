from functools import partial
import pandas as pd
import time
import requests as requests
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import quote

from blogXpath import Naver_blog_xpath
from findBlogContents import FindNaverContents
from reworkBlogContents import ReworkContents
from saveCsv import df_save_csv

chromedriver_path = '/Applications/chromedriver'  # 크롬드라이버 경로

# 테스트용
qText = "시그 mcx"
start_date = "20190101"  # 시작날짜
end_date = "20211125"  # 종료날짜

# 파일명 이제 지정
# 키워드_시작날짜_끝날짜로 저장되게 수정하기
csvFileName = f"{qText}_네이버블로그_{start_date}_{end_date}_url.csv"  # url 수집을 저장하는 파일명
mainCsvFileName = f"{qText}_네이버블로그_{start_date}_{end_date}.csv"  # 최종수집결과를 저장하는 파일명

xpath_root = Naver_blog_xpath()  # xpath 경로
find_content = FindNaverContents()  # 크롤링 데이터 탐색 부분
rework_content = ReworkContents()  # 전처리 부분


def open_site_re(driver):
    url = "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=" + quote(qText)
    driver.get(url)
    driver.implicitly_wait(10)

    if start_date != "" and end_date != "":
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정
        time.sleep(1)

        # 시작날짜를 입력하는 부분
        ## 체크
        s_date = driver.find_element_by_xpath(xpath_root.start_date_button)
        driver.find_element_by_xpath(xpath_root.start_date_button).click()
        s_date.clear()
        time.sleep(0.5)
        for c in start_date:
            s_date.send_keys(c)
            time.sleep(0.2)
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()
        time.sleep(0.5)
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()

        # 종료날짜를 입력하는 부분
        e_date = driver.find_element_by_xpath(xpath_root.end_date_button)
        driver.find_element_by_xpath(xpath_root.end_date_button).click()
        e_date.clear()
        time.sleep(0.5)
        for c in end_date:
            e_date.send_keys(c)
            time.sleep(0.2)
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()
        time.sleep(0.5)
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()
        driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용
    else:
        driver.find_element_by_xpath(xpath_root.period_setting_button).click()
        driver.find_element_by_xpath(xpath_root.one_week).click()
    time.sleep(2)

    return driver


# 검색 결과에 따른 총 페이지 수 파악
def find_page_count(text):
    page_num = int(text.replace(",", '').replace("건", ""))
    page_count = int(page_num / 7) + 1
    if page_count == 0:
        page_count = 1
    return page_count


def content_crawling():
    start_time = time.time()

    # 타이틀, url, 횟수
    return_title_list = []
    return_url_list = []
    count_num = 0

    window_size = "1200,800"
    chrome_options = Options()
    # chrome_options.add_argument('headless') # 창 안뜨게
    chrome_options.add_argument(f"--window-size={window_size}")  # 창 사이즈

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.implicitly_wait(10)  # 페이지 로딩될때까지 최대 몇초까지 기다릴것인지
    url = open_site_re(driver).current_url
    driver.implicitly_wait(15)
    driver.get(url)
    time.sleep(1)

    page_num_text = driver.find_element_by_xpath(xpath_root.page_all_text).text
    page_count = find_page_count(page_num_text) # 페이지 수 파악
    print("총 페이지 : ", page_count)

    # 수집중 중단 되었을때 다시 시작하기 위한 조건
    if os.path.isfile(csvFileName):
        print("동일 url.csv 파일 존재")
        url_count = pd.read_csv(csvFileName)
        url_start_count = len(url_count)
        # print(url_start_count)
        re_start_page = int(url_start_count / 7) + 1
        # print("re_start_page : ", re_start_page)
        if re_start_page != page_count:
            url_1 = url[:56]
            url_2 = url[57:]
            url = url_1 + f"{re_start_page}" + url_2
            driver.get(url)
        elif re_start_page >= page_count:
            print("url 수집 완료.csv 파일")
            return csvFileName
    time.sleep(2)

    try:
        for _ in range(page_count):
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            post_list = soup.findAll("a", class_="desc_inner")
            time.sleep(1)
            for post in post_list:
                post_ti = post.get_text()
                post_url = post.attrs['href']

                # 중복체크
                if post_url not in return_url_list or post_ti not in return_title_list:
                    return_title_list.append(post_ti)
                    return_url_list.append(post_url)

                count_num += 1

                now_page = driver.current_url.split("&")[0][-1]
                next_page_num = (int(now_page) + 1) % 10

            if next_page_num != 1 and next_page_num != 0:
                driver.find_element_by_xpath(
                    """//*[@id="content"]/section/div[3]/span[""" + str(next_page_num) + "]/a").click()
                time.sleep(1)
            elif next_page_num == 0:
                driver.find_element_by_xpath("""//*[@id="content"]/section/div[3]/span[10]/a""").click()
                time.sleep(1)
            else:
                driver.find_element_by_link_text("다음").click()
                print("다음")
                time.sleep(1)
        driver.close()

    except Exception as ex:
        print("크롤링 종료")

    finally:
        endTime = time.time()
        print("url 크롤링 수 : ", count_num)
        print(f"url 소요시간 : {endTime - start_time:.5f} 초")
        first_df = pd.DataFrame(data={'title': return_title_list, 'url': return_url_list})
        # print("first_df : ", first_df)
        return df_save_csv(first_df, csvFileName)


def main_crawling(data):
    # 크롤링 한 결과를 담아 두는 리스트
    blog_title_list = []
    blog_time_list = []
    blog_post_list = []
    blog_url_list = []

    # 제외된 부분 확인을 위한 리스트
    except_idx_list = []
    except_title_list = []
    except_url_list = []

    # 로그 확인용
    crawling_count = 0
    pass_count = 0

    # 셀레니움 설정 옵션
    window_size = "1200,1200"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--window-size={window_size}")

    url_load = pd.read_csv(data)
    num_list = len(url_load)

    # 파일 유무확인하고 있을시에 전체 길이를 확인, 시작값 변경
    if os.path.isfile(mainCsvFileName):
        # print("동일명 파일 있음")
        re_url_load = pd.read_csv(mainCsvFileName)
        restart_url = re_url_load['url'][-1:].values
        url = restart_url[0]
        csv_file = pd.read_csv(csvFileName)['url']
        start_point = csv_file.index[csv_file == url].tolist()
        start_point = int(start_point[0]) + 1
        # print("start_point : ", start_point)
        if start_point + 1 >= num_list:
            print("완료된 파일, 확인필요")
            sys.exit(0)
    else:
        start_point = 0

    for i in range(start_point, num_list):
        temp_pass_count = pass_count
        url = url_load['url'][i]
        original_url = url  # 원래 url을 기억
        try:
            url = rework_content.delete_iframe(url) # url 재정리
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

            # 전처리
            title = rework_content.text_cleaning(title)
            main_post = rework_content.text_cleaning(main_post)

            if title != '' and wTime != '' and main_post != '':
                blog_title_list.append(title)
                blog_time_list.append(wTime)
                blog_post_list.append(main_post)
                blog_url_list.append(original_url)
                crawling_count += 1

            else:
                except_idx_list.append(i)
                except_title_list.append(url_load['title'][i])
                except_url_list.append(url_load['url'][i])
                pass_count += 1
                # 본문 내용만 있어나 한것도 별도로 저장하기
                pass
            driver.implicitly_wait(10)

        except:
            print(f"네이버 블로그가 아닙니다. 인덱스 : {i}")
            pass_count += 1
            middle_df = pd.DataFrame(
                {'title': blog_title_list, 'date': blog_time_list, 'text': blog_post_list, 'url': blog_url_list})
            df_save_csv(middle_df, mainCsvFileName)
            pass
        # driver.close()
        print(f"메인 크롤링 {crawling_count}회")
        print(f"pass {pass_count}회")
        if pass_count != temp_pass_count:
            # print(f"제외 인덱스 Num : {except_idx_list}")
            print(f"제외 인덱스 title : {except_title_list}")
            print(f"제외 인덱스 url : {except_url_list}")

    last_df = pd.DataFrame(
        {'title': blog_title_list, 'date': blog_time_list, 'text': blog_post_list, 'url': blog_url_list})
    df_save_csv(last_df, mainCsvFileName)


if __name__ == '__main__':
    startTime = time.time()

    first_data = content_crawling()
    main_crawling(first_data)

    endTime = time.time()
    print(f"소요시간 : {endTime - startTime:.5f} 초")


# 주석 : 년월일 수정자 주석으로 적어주기, 수정내용을 전부 주석으로 처리해두기
