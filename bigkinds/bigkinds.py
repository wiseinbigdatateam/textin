from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import os
import time
import csv
import pandas as pd

from webdriver import Webdriver
from bigkinds.xpath import BigkindsXpath as xpath


class Bigkinds:
    def __init__(self):
        self.driver = Webdriver().driver
        self.listnum = 10  # 10 기본, 30, 50, 100 선택 가능
        self.url = 'https://www.bigkinds.or.kr/'

    def set_start_point(self, index):
        start_page = int(index / self.listnum + 1)
        start_list = index % self.listnum if index % self.listnum != 0 else 1
        print(start_page, start_list)
        return start_page, start_list

    def search_keyword(self):
        # 처음에 상세검색으로 날짜 지정하고 검색 시작 -첫화면url로 시작, 상세검색 클릭 후 날짜 먼저 지정
        self.driver.get(self.url)
        time.sleep(2)

        # 상세검색 클릭 후 기간 탭 클릭
        self.driver.find_element(By.XPATH, xpath.detail_xpath).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, xpath.datetab_xpath).click()
        time.sleep(1)

        # 상세검색 모달창에서 시작일, 종료일 입력한 뒤 키워드 입력 후 엔터 입력하는 체인 실행
        start_box = self.driver.find_element(By.XPATH, xpath.start_xpath)
        end_box = self.driver.find_element(By.XPATH, xpath.end_xpath)
        search_box = self.driver.find_element(By.XPATH, xpath.keyword_xpath)
        # start_box.clear()로 기존 값을 지우면 자동으로 기본값 1990.01.01로 입력됨exist_dfreturn키로 하나씩 값을 지워야 함.
        actions = self.driver.ActionChains(self.driver) \
            .send_keys_to_element(start_box, Keys.RETURN) \
            .send_keys_to_element(start_box, Keys.RETURN) \
            .send_keys_to_element(start_box, Keys.RETURN) \
            .send_keys_to_element(start_box, self.start_date) \
            .send_keys_to_element(end_box, Keys.RETURN) \
            .send_keys_to_element(end_box, Keys.RETURN) \
            .send_keys_to_element(end_box, Keys.RETURN) \
            .send_keys_to_element(end_box, self.end_date) \
            .send_keys_to_element(search_box, self.keyword) \
            .send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2)

        # 검색 결과가 늦게 뜰 경우 방어 로직.
        try:
            result_keyword = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath.result_xpath))
            )
        finally:
            # 결과 건수 텍스트 추출
            result_keyword = result_keyword.text
            result_number = self.driver.find_element(By.XPATH, xpath.result_number_xpath).text
            result_number = int(result_number.replace(',', ''))

        # 10건씩 보기 설정(기본)
        # if self.listnum == 10:
        #     self.driver.find_element(By.XPATH, xpath.ten_xpath).click()
        # time.sleep(1.5)

        # 30건씩 보기 설정
        if self.listnum == 30:
            self.driver.find_element(By.XPATH, xpath.thirty_xpath).click()
        time.sleep(1.5)

        # 50건씩 보기 설정
        if self.listnum == 50:
            self.driver.find_element(By.XPATH, xpath.fifty_xpath).click()
        time.sleep(1.5)

        # 100건씩 보기 설정
        if self.listnum == 100:
            self.driver.find_element(By.XPATH, xpath.hundred_xpath).click()
        time.sleep(1.5)

        print(f'{result_keyword}이(가) {result_number} 건 검색되었습니다.')
        return result_number

    # 해당 페이지로 이동
    def move_to_page(self, i):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(0.5)
        page_num_box = self.driver.find_element(By.XPATH, xpath.page_num_xpath)
        page_num_box.clear()
        time.sleep(0.5)
        actions = self.webdriver.ActionChains(self.driver) \
            .send_keys_to_element(page_num_box, i) \
            .send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        print(f'{i}페이지로 이동')
        return

    # 모달 본문 하단 다음글 클릭
    def click_next(self):
        for next_xpath in xpath.next_xpaths:
            try:
                self.driver.find_element(By.XPATH, next_xpath).click()
                # print(f'클릭된 index: {self.next_xpaths.index(next_xpath)}')
                time.sleep(1)
                return
            except NoSuchElementException:
                continue
            except ElementNotInteractableException:
                continue

    # 모달 본문 크롤링
    # 페이지 수를 받아와서 해당 페이지 본문 크롤링하고 리턴
    def crawling_modal(self, start, last):
        results = []
        print(f'------crawling body start: {start}, last: {last}------')
        state = 2
        count = 3
        try:
            for i in range(start, last+1):
                title = self.driver.find_element(By.XPATH, xpath.title_xpath).text
                # category = self.driver.find_element(By.XPATH, xpath.category_xpath).text
                date = self.driver.find_element(By.XPATH, xpath.date_xpath).text
                content = self.driver.find_element(By.XPATH, xpath.content_xpath).text
                results.append({'title': title, 'date': date, 'content': content, 'url': ''})

                # 건 수 카운팅
                count += 1
                if count % 10 == 0:
                    print(f'{count}건을 가져왔습니다.')

                # 해당 리스트 페이지의 마지막 인덱스 본문 크롤링을 마치면 모달창 닫음
                if i == last:
                    self.driver.find_element(By.XPATH, self.modal_close_xpath).click()
                    time.sleep(1)

                # 다음 글이 있으면 모달 본문 하단의 다음 글 클릭
                else:
                    self.click_next()
        except:
            state = 2

        finally:
            return results, count, state, 3

    def crawling_body(self, df, index):
        state = 2
        results = []
        start_page, start_list = self.set_start_point(index)
        result_number = self.search_keyword()
        total_page = int(result_number/self.listnum + 1)
        last_list = result_number % self.listnum
        print(f'-총 페이지 수: {total_page}페이지, '
              f'-시작 페이지: {start_page}페이지, '
              f'-한 페이지 게시글 수: {self.listnum}개, '
              f'-첫 페이지 시작 게시글: {start_list}번째, '
              f'-마지막 페이지 끝 게시글: {last_list}번째')

        # if start_page > total_page:
        #     print("시작 페이지가 총 페이지 수보다 큽니다.")
        #     return
        #
        # if start_list > self.listnum:
        #     print("시작 리스트 인덱스가 설정한 건 수보다 큽니다.")
        #     return
        #
        # if start_page == total_page and start_list > last_list:
        #     print("시작 리스트 인덱스가 마지막 리스트 인덱스보다 큽니다.")
        #     return

        start = time.time()
        for i in range(start_page, total_page+1):
            page_start = time.time()

            self.move_to_page(i)

            # 크롤링을 시작할 게시글 클릭
            print('start_list: ', start_list)
            first_title_xpath = f'//*[@id="news-results"]/div[{start_list}]/div/div[2]/a'  ### 이건 어떻게 빼지?
            self.driver.find_element(By.XPATH, first_title_xpath).click()
            time.sleep(1)

            # 마지막 페이지
            if i == total_page:
                print(f'마지막 페이지 크롤링 시작: {total_page}페이지')
                modal_results, modal_index, state, start_list = self.crawling_modal(start_list, last_list)
            else:
                modal_results, modal_index, state, start_list = self.crawling_modal(start_list, self.listnum)

            results.extend(modal_results)

            page_end = time.time()
            print(f'---{i}페이지 완료, -걸린 시간: {page_end - page_start}, -건 수: {modal_index}')
            i += 1
        end = time.time()
        print('Entire Crawling Time: ', end - start)

        # 크롬드라이버 종료
        self.driver.close()
        return results, state

    # 데이터가 많을 경우 데이터프레임이 속도가 더 빠를 것으로 추정됨
    def save_to_csv(self, exist_df, results, state):
        # 기존 데이터프레임과 새로 크롤링한 데이터프레임 결합
        result_df = exist_df.append(pd.Series(results, index=exist_df.columns), ignore_index=True)
        # 기존 진행중 파일 삭제
        os.remove(f'{self.save_path}{self.file_name}_0.csv')
        # 결합한 데이터 프레임 저장
        result_df.to_csv(f'{self.save_path}{self.file_name}_{state}.csv', encoding = 'utf-8')
        # file = open(f"{file_name}", mode="w")
        # writer = csv.writer(file)
        # writer.writerow(["title", "category", "date", "content"])
        # for result in results:
        #     writer.writerow(list(result.values()))
        print('file saved')
        return


if __name__ == '__main__':
    bigkinds = Bigkinds()  # init에 기본값 설정해놓고 set함수 만들기
    # print(bigkinds.check_exist_file())
    start_page, start_list, exist_df = bigkinds.check_exist_file()
    # print(start_page, start_list)
    result_number = bigkinds.search_keyword()
    # print(result_number)
    results, state = bigkinds.crawling_modal(start_page, start_list)
    print(f'총 검색 결과: {result_number}, results 길이: {len(results)}, 상태: {state}')
    # results = ['','','', '']
    # state = 1
    bigkinds.save_to_csv(exist_df, results, state)
