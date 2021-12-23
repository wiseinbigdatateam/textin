from functools import partial
import pandas as pd
import time
import requests as requests
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import quote

from setWebdriver import set_driver as setting_driver, open_site
from blogXpath import Naver_blog_xpath
from findBlogContents import FindNaverContents
from reworkBlogContents import ReworkContents
from webdriver import Webdriver
from naverTest import find_page_count
from saveCsv import df_save_csv

# chromedriver_path = '/Applications/chromedriver'  # 크롬드라이버 경로

# # 테스트용
# keyword = "시그 mcx"
# start_date = "2019.1.1"  # 시작날짜
# end_date = "2021.11.25"  # 종료날짜

# state 값
# 0: url 크롤링 중
# 1: url 크롤링 완료
# 2: body 크롤링 중
# 3: body 크롤링 완료(전체 크롤링 완료)

# 파일명 이제 지정
# 키워드_시작날짜_끝날짜로 저장되게 수정하기
# csvFileName = f"{qText}_네이버블로그_{start_date}_{end_date}_url"  # url 수집을 저장하는 파일명
# mainCsvFileName = f"{qText}_네이버블로그_{start_date}_{end_date}"  # 최종수집결과를 저장하는 파일명


find_content = FindNaverContents()  # 크롤링 데이터 탐색 부분
rework_content = ReworkContents()  # 전처리 부분
xpath_root = Naver_blog_xpath()


class NaverBlog:
    def __init__(self, keyword, start_date, end_date):
        self._keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.driver = Webdriver().driver
        self.url = "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=" + quote(
            keyword)
        self.csvFileName = f"{keyword}_naver_{start_date}_{end_date}"  # url 수집을 저장하는 파일명
        self.mainCsvFileName = f"{keyword}_naver_{start_date}_{end_date}"  # 최종수집결과를 저장하는 파일명

    def find_page_count(self, text):
        page_num = int(text.replace(",", '').replace("건", ""))
        page_count = int(page_num / 7) + 1
        if page_count == 0:
            page_count = 1
        return page_count

    def search_keyword(self, t_start_date, t_end_date):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        setting_period = self.driver.find_element_by_xpath(xpath_root.period_setting_button)  # 기간설정
        setting_period.click()
        time.sleep(1)

        s_date = self.driver.find_element_by_xpath(xpath_root.start_date_button)
        s_date.click()
        s_date.clear()
        time.sleep(0.2)
        for c in t_start_date:
            s_date.send_keys(c)
            time.sleep(0.2)
        setting_period.click()
        time.sleep(0.25)
        setting_period.click()

        e_date = self.driver.find_element_by_xpath(xpath_root.end_date_button)
        e_date.click()
        e_date.clear()
        time.sleep(0.25)
        for c in t_end_date:
            e_date.send_keys(c)
            time.sleep(0.2)
        setting_period.click()
        time.sleep(0.25)
        setting_period.click()
        self.driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용 버튼
        return self.driver

    def xpath_is_exist(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def url_crawling(self, exist_df, exist_index, exist_state):
        state = exist_state
        start_time = time.time()
        # 타이틀, url, 횟수
        return_title_list = []
        return_url_list = []
        count_num = 0

        self.driver = self.search_keyword(self.start_date, self.end_date)

        url = self.driver.current_url
        page_num_text = self.driver.find_element_by_xpath(xpath_root.page_all_text).text

        page_count = find_page_count(page_num_text)  # 페이지 수 파악
        print("총 페이지 : ", page_count)

        start_page = int(exist_index / 7) + 1

        if start_page != page_count:
            url_1 = url[:56]
            url_2 = url[57:]
            url = url_1 + f"{start_page}" + url_2
            self.driver.get(url)

        try:
            for i in range(start_page, page_count):
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                post_list = soup.findAll("a", class_="desc_inner")
                time.sleep(1)
                for post in post_list:
                    post_ti = post.get_text()
                    post_url = post.attrs['href']

                    # 중복체크
                    if post_url not in return_url_list and post_ti not in return_title_list:
                        return_title_list.append(post_ti)
                        return_url_list.append(post_url)

                    count_num += 1

                now_page = self.driver.current_url.split("&")[0][-1]
                next_page_num = (int(now_page)) % 10 + 1
                # print("next_page_num : ", next_page_num, ", i : ", i)

                click_page_num = """//*[@id="content"]/section/div[3]/span[""" + str(next_page_num) + "]/a"

                if next_page_num == 1:
                    if self.driver.find_element_by_link_text("다음"):
                        self.driver.find_element_by_link_text("다음").click()
                        print("다음10페이지")
                        time.sleep(1)

                elif self.xpath_is_exist(click_page_num):
                    print("next page click, next page num = ", next_page_num)
                    self.driver.find_element_by_xpath(click_page_num).click()
                    time.sleep(1)
            print("크롤링 완료됨")
            print("state setting")
            state = 1

        except:
            print("크롤링 중단됨")

        finally:
            endTime = time.time()
            print("url 크롤링 수 : ", count_num)
            print(f"url 소요시간 : {endTime - start_time:.5f} 초")
            print("state ", state)
            first_result_df = pd.DataFrame(data={'title': return_title_list, 'url': return_url_list})
            # first_csv = df_save_csv(first_df, self.csvFileName, state, exist_df)
            return first_result_df, state, exist_df

    def check_exist_file(self, data):
        if os.path.isfile(f"{self.mainCsvFileName}_2.csv"):
            # print("동일명 파일 있음")
            exist_df = pd.read_csv(f"{self.mainCsvFileName}_2.csv")
            restart_url = exist_df['url'][-1:].values
            url = restart_url[0]
            csv_file = pd.read_csv(f"{self.csvFileName}_1.csv")['url']
            start_point = csv_file.index[csv_file == url].tolist()
            start_point = int(start_point[0]) + 1
            # print("start_point : ", start_point)
        elif os.path.isfile(f"{self.mainCsvFileName}_3.csv"):
            print(f"{self.mainCsvFileName}_3.csv 존재, 확인필요")
            sys.exit(0)
        else:
            exist_df = pd.DataFrame(columns=["title", "date", "text", "url"])
            start_point = 0
        return start_point, exist_df

    def main_crawling(self, data, exist_state):
        # if not os.path.isfile(f"{self.csvFileName}_1.csv"):
        #     print(f"{self.csvFileName}_1.csv 파일이 존재 하지 않음")
        #     self.driver.close()
        #     sys.exit()
        state = 2

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

        url_load = pd.read_csv(data)
        num_list = len(url_load)
        print("num_list : ", num_list)

        start_point, exist_df = self.check_exist_file(data)

        try:
            for i in range(start_point, num_list):
                temp_pass_count = pass_count
                url = url_load['url'][i]
                original_url = url  # 원래 url을 기억
                url = rework_content.delete_iframe(url)  # url 재정리
                self.driver.get(url)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                self.driver.implicitly_wait(10)

                # 게시글 제목
                title = find_content.find_title(soup)
                self.driver.implicitly_wait(10)

                # 작성 시간 파악
                wTime = find_content.find_date(soup)
                self.driver.implicitly_wait(10)

                # 본문 내용
                main_post = find_content.find_main_post(soup)
                self.driver.implicitly_wait(10)

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

                self.driver.implicitly_wait(10)
                print(f"메인 크롤링 {crawling_count}회")
                print(f"pass {pass_count}회")
                if pass_count != temp_pass_count:
                    # print(f"제외 인덱스 Num : {except_idx_list}")
                    print(f"제외 인덱스 title : {except_title_list}")
                    print(f"제외 인덱스 url : {except_url_list}")

            print("state setting")
            state = 3

        except:
            print(f"크롤링 중단됨. 인덱스 : {i}")
            pass_count += 1

        finally:
            print("state ", state)
            results_df = pd.DataFrame(
                {'title': blog_title_list, 'date': blog_time_list, 'text': blog_post_list, 'url': blog_url_list})
            # df_save_csv(last_df, self.mainCsvFileName, state, exist_df_1)
            # self.driver.close()
            return exist_df, exist_state, results_df, state

# if __name__ == '__main__':
#     startTime = time.time()
#     naver_blog = NaverBlog()
#
#     start_page, exist_df = naver_blog.check_exist_file()
#     first_data, exist_df = naver_blog.content_crawling(start_page, exist_df)
#     naver_blog.main_crawling(first_data, exist_df)
#
#     endTime = time.time()
#     print(f"소요시간 : {endTime - startTime:.5f} 초")
