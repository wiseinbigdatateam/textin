import sys
import os
import pandas as pd
import time

from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import quote

from .xpath import Tstory_blog_xpath
from .findContents import FindTsotryContents
from crawling.common.reformat import Reformat
from crawling.common.webdriver import Webdriver

xpath_root = Tstory_blog_xpath()
find_content = FindTsotryContents()  # 크롤링 데이터 탐색 부분
rework_content = Reformat()  # 전처리 부분

class TstoryBlog:
    def __init__(self, keyword, start_date, end_date):
        self._keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.driver = Webdriver().driver
        self.url = "https://search.daum.net/search?w=blog&f=section&SA=tistory&lpp=10&nil_src=blog&q=" + quote(keyword) + "&p=1"
        self.csvFileName = f"{keyword}_tstory_{start_date}_{end_date}"  # url 수집을 저장하는 파일명
        self.mainCsvFileName = f"{keyword}_tstory_{start_date}_{end_date}"

    # def find_page_count(self, text):
    #     text = text.split("/")
    #     page_num = int(text[1].replace("건", "").replace("약", "").replace(",", ""))
    #     page_count = int(page_num / 10)
    #     if page_count == 0:
    #         page_count = 1
    #     return page_count

    def search_keyword(self, start_date, end_date):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        setting_period = self.driver.find_element_by_xpath(xpath_root.period_setting_button)  # 기간설정
        setting_period.click()
        time.sleep(1)

        # 티스토리만 날짜갑 입력 방식이 다르기 때문에 수정
        num = start_date[:4]
        num1 = start_date[4:6]
        num2 = start_date[6:]
        re_start_date = num + "." + num1 + "." + num2
        num3 = end_date[:4]
        num4 = end_date[4:6]
        num5 = end_date[6:]
        re_end_date = num3 + "." + num4 + "." + num5

        s_date = self.driver.find_element_by_xpath(xpath_root.start_date_button)
        s_date.click()
        s_date.clear()
        time.sleep(0.3)
        for c in re_start_date:
            s_date.send_keys(c)
            time.sleep(0.2)

        start_click_num = re_start_date.split(".")[-1]
        self.driver.find_element_by_link_text(f"{start_click_num}").click()

        e_date = self.driver.find_element_by_xpath(xpath_root.end_date_button)
        e_date.click()
        e_date.clear()
        time.sleep(0.3)
        for c in re_end_date:
            e_date.send_keys(c)
            time.sleep(0.2)

        end_click_num = re_end_date.split(".")[-1]
        self.driver.find_element_by_link_text(f"{end_click_num}").click()
        self.driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용

        self.driver.find_element_by_xpath(xpath_root.select_blog).click()  # 출처 (블로그 종류)
        self.driver.find_element_by_xpath(xpath_root.select_tstory).click()  # 티스토리 선택
        time.sleep(1)

        return self.driver

    def xpath_is_exist(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def url_crawling(self, exist_df, exist_index, exist_state):
        state = exist_state
        startTime = time.time()
        # 타이틀, url, 횟수
        return_title_list = []
        return_url_list = []
        count_num = 0

        self.driver = self.search_keyword(self.start_date, self.end_date)
        time.sleep(1)

        url = self.driver.current_url
        page_num_text = self.driver.find_element_by_xpath(xpath_root.page_all_text).text
        page_count = find_content.find_page_count(page_num_text)
        print("총 페이지 : ", page_count)

        re_start_page = int(exist_index / 10) + 1
        if re_start_page != page_count and re_start_page != 1:
            url_1 = url[:102]
            url = url_1 + f"{re_start_page}"
            self.driver.get(url)
            start_page = re_start_page
        else:
            start_page = 0

        try:
            for page in range(start_page, page_count):
                html = self.driver.page_source
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
                last_page = self.driver.current_url.split("&")[6]
                last_page = last_page.split('=')[-1]
                # print("last page: ", last_page )
                # if last_page != page_count:
                #     self.driver.find_element_by_xpath(xpath_root.next_page_button).click()
                #     print(f"{last_page}에서 다음페이지로")

                if self.xpath_is_exist(xpath_root.next_page_button):
                    self.driver.find_element_by_xpath(xpath_root.next_page_button).click()
                    print(f"{last_page}에서 다음페이지로")

            time.sleep(0.5)
            print("크롤링 완료됨")
            print("state setting")
            state = 1

        except:
            print("크롤링 중단됨")

        finally:
            endTime = time.time()
            print("링크 크롤링 수 : ", count_num)
            print(f"url 소요시간 : {endTime - startTime:.5f} 초")
            print("state : ", state)
            first_result_df = pd.DataFrame(data={'title': return_title_list, 'url': return_url_list})
            # first_csv = df_save_csv(first_df, self.csvFileName, state, exist_df)
            return first_result_df, state, exist_df

    def check_exist_file(self):
        if os.path.isfile(f"{self.mainCsvFileName}_2.csv"):
            # print("동일명 파일 있음")
            exist_df = pd.read_csv(f"{self.mainCsvFileName}_2.csv")
            restart_url = exist_df['url'][-1:].values
            url = restart_url[0]
            csv_file = pd.read_csv(f"{self.csvFileName}_1.csv")['url']
            start_point = csv_file.index[csv_file == url].tolist()
            start_point = int(start_point[0]) + 1
            print("start_point : ", start_point)
        elif os.path.isfile(f"{self.mainCsvFileName}_3.csv"):
            print(f"{self.mainCsvFileName}_3.csv 존재, 확인필요")
            sys.exit(0)
        else:
            exist_df = pd.DataFrame(columns=["title", "date", "text", "url"])
            start_point = 0
        return start_point, exist_df

    def main_crawling(self, first_result_df, exist_state):
        data = first_result_df
        state = 2
        exist_state = 2

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

        start_point, exist_df = self.check_exist_file()

        try:
            for i in range(start_point, num_list):
                temp_pass_count = pass_count
                url = url_load['url'][i]
                original_url = url
                self.driver.get(url)
                self.driver.implicitly_wait(15)

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
                # print("text : ", main_post)
                # 해당 url
                # blog_url = self.driver.current_url

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
                    pass

            print(f"메인 크롤링 {crawling_count}회")
            print(f"pass {pass_count}회")
            # print(temp_pass_count)
            # if pass_count != temp_pass_count:
            #     print(f"제외 인덱스 Num : {except_idx_list}")
            #     print(f"제외 인덱스 title : {except_title_list}")
            #     print(f"제외 인덱스 url : {except_url_list}")
            print("state setting")
            state = 3

        except:
            print(f"크롤링 중단.")
            # print(f"제목 : {url_load['title'][i]}, url :  {url_load['url'][i]}")
            except_idx_list.append(i)
            except_title_list.append(url_load['title'][i])
            except_url_list.append(url_load['url'][i])
            pass_count += 1

        finally:
            print("state ", state)
            print(exist_df)
            results_df = pd.DataFrame(
                {'title': blog_title_list, 'date': blog_time_list, 'text': blog_post_list, 'url': blog_url_list})
            # df_save_csv(last_df, self.mainCsvFileName, state, exist_df_1)
            # self.driver.close()
            return exist_df, exist_state, results_df, state
