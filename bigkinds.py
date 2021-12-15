from selenium import webdriver
# from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import os
import time
import csv
import pandas as pd


class CrawlingBigkinds:
    def __init__(self):
        # chromedriver의 위치를 지정
        chromedriver_path = '/Applications/chromedriver'
        window_size = "1920,1200"
        self.listnum = 10  # 10이 원래 기본, 100으로 설정할 것
        self.url = 'https://www.bigkinds.or.kr/'
        # 사용자 입력 정보
        self._keyword = '에그타르트'
        self._start_date = '20210901'
        self._end_date = '20211130'
        # 결과 저장 csv 파일명
        self.file_name = f'{self._keyword}_bigkinds_{self._start_date}_{self._end_date}'
        self.save_path = "./"


        # 크롬드라이버 옵션
        chrome_options = Options()
        # # 포트 9222로 열어둔(VPN 확장프로그램 설치 및 로그인해 놓은) 크롬창에서 디버그 모드로 실행
        # # 9222포트로 크롬 실행 맥 터미널
        # # /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/ChromeProfile"
        # # 윈도우 실행창
        # # C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
        # # 혹은
        # # C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
        # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

        chrome_options.add_argument("--headless") # 크롬창이 열리지 않음
        chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정. linux, docker 등
        chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정. linux, docker 등
        chrome_options.add_argument(f"--window-size={window_size}")
        chrome_options.add_argument('Content-Type=application/json; charset=utf-8')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15")
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        self.driver.implicitly_wait(3)  # 웹 자원 로드 위해 3초 대기

        # def crawling_body()
        # 본문 크롤링용 xpath
        self.title_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1'
        self.category_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/div/span'
        self.date_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul/li[1]'
        self.content_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]'
        # 모달창 닫기 xpath
        self.modal_close_xpath = '//*[@id="news-detail-modal"]/div/div/div[2]/button'
        # 다음글 xpath
        self.next_xpaths = ['//*[@id="news-detail-modal"]/div/div/div[1]/div/div[4]/ul/li[2]/dd/a',
                            '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[3]/ul/li[2]/dd/a',
                            '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[3]/ul/li[3]/dd/a',
                            '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[4]/ul/li[3]/dd/a'
                            ]

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        self._keyword = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    # 상태 1인 파일있으면 리턴 추가
    def check_exist_file(self):
        print(self.file_name)
        if os.path.isfile(f'{self.save_path}{self.file_name}_0.csv'):
            exist_df = pd.read_csv(f'{self.file_name}_0.csv')
            exist_index = len(exist_df.index)
            print(f'작업 중인 파일이 존재합니다. 행 수: {exist_index}')
            start_page = int(exist_index / self.listnum + 1)
            start_list = exist_index % self.listnum
        else:
            start_page = 1
            start_list = 1
            exist_df = pd.DataFrame(columns=["title", "category", "date", "content"])
        return start_page, start_list, exist_df

    def search_keyword(self):
        # 처음에 상세검색으로 날짜 지정하고 검색 시작 -첫화면url로 시작, 상세검색 클릭 후 날짜 먼저 지정
        self.driver.get(self.url)
        time.sleep(2)

        detail_xpath = '//*[@id="news-search-form"]/div/div[1]/button'
        datetab_xpath = '//*[@id="news-search-form"]/div/div[1]/div[2]/div/div[1]/div[1]/a'
        start_xpath = '//*[@id="search-begin-date"]'
        end_xpath = '//*[@id="search-end-date"]'
        keyword_xpath='//*[@id="total-search-key"]'

        # 상세검색 클릭 후 기간 탭 클릭
        self.driver.find_element(By.XPATH, detail_xpath).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, datetab_xpath).click()
        time.sleep(1)

        # 상세검색 모달창에서 시작일, 종료일 입력한 뒤 키워드 입력 후 엔터 입력하는 체인 실행
        start_box = self.driver.find_element(By.XPATH, start_xpath)
        end_box = self.driver.find_element(By.XPATH,end_xpath)
        search_box = self.driver.find_element(By.XPATH,keyword_xpath)
        # start_box.clear()로 기존 값을 지우면 자동으로 기본값 1990.01.01로 입력됨. return키로 하나씩 값을 지워야 함.
        actions = webdriver.ActionChains(self.driver) \
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
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="news-results-tab"]/div[2]/h3/span[1]/span'))
            )
        finally:
            # 결과 건수 텍스트 추출
            result_keyword = result_keyword.text
            result_number = self.driver.find_element(By.XPATH, '//*[@id="news-results-tab"]/div[2]/h3/span[6]').text
            result_number = int(result_number.replace(',', ''))

        # 100건씩 보기 설정
        if self.listnum == 100:
            self.driver.find_element(By.XPATH, '//*[@id="select2"]/option[4]').click()
        time.sleep(1.5)

        print(f'{result_keyword}이(가) {result_number} 건 검색되었습니다.')
        self.result_number = result_number
        return result_number

    # 해당 페이지로 이동
    def move_to_page(self, i):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(0.5)
        page_num_xpath = '//*[@id="paging_news_result"]'
        page_num_box = self.driver.find_element(By.XPATH, page_num_xpath)
        page_num_box.clear()
        time.sleep(0.5)
        actions = webdriver.ActionChains(self.driver) \
            .send_keys_to_element(page_num_box, i) \
            .send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        print(f'{i}페이지로 이동')
        return

    # 모달 본문 하단 다음글 클릭
    def click_next(self):
        for next_xpath in self.next_xpaths:
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
    def crawling_body(self, start, last):
        results = []
        print(f'------crawling body start: {start}, last: {last}------')
        state = 1
        count = 0
        try:
            for i in range(start, last+1):
                title = self.driver.find_element(By.XPATH, self.title_xpath).text
                category = self.driver.find_element(By.XPATH, self.category_xpath).text
                date = self.driver.find_element(By.XPATH, self.date_xpath).text
                content = self.driver.find_element(By.XPATH, self.content_xpath).text

                # print({'title': title, 'category': category, 'date': date, 'content': content})
                results.append({'title': title, 'category': category, 'date': date, 'content': content})

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
            state = 0

        finally:
            return results, count, state, 1

    def crawling_contents(self, start_page, start_list):
        # self.calculate_start()

        results = []
        total_page = int(self.result_number/self.listnum + 1)
        last_list = self.result_number % self.listnum
        print(f'-총 페이지 수: {total_page}페이지, '
              f'-시작 페이지: {start_page}페이지, '
              f'-한 페이지 게시글 수: {self.listnum}개, '
              f'-첫 페이지 시작 게시글: {start_list}번째, '
              f'-마지막 페이지 끝 게시글: {last_list}번째')

        if start_page > total_page:
            print("시작 페이지가 총 페이지 수보다 큽니다.")
            return

        if start_list > self.listnum:
            print("시작 리스트 인덱스가 설정한 건 수보다 큽니다.")
            return

        if start_page == total_page and start_list > last_list:
            print("시작 리스트 인덱스가 마지막 리스트 인덱스보다 큽니다.")
            return

        start = time.time()
        state = 0

        for i in range(start_page, total_page+1):
            page_start = time.time()

            self.move_to_page(i)

            # 크롤링을 시작할 게시글 클릭
            print('start_list: ', start_list)
            first_title_xpath = f'//*[@id="news-results"]/div[{start_list}]/div/div[2]/a'
            self.driver.find_element(By.XPATH, first_title_xpath).click()
            time.sleep(1)

            # 마지막 페이지
            if i == total_page:
                print(f'마지막 페이지 크롤링 시작: {total_page}페이지')
                body_results, index, state, start_list = self.crawling_body(start_list, last_list)
            else:
                body_results, index, state, start_list = self.crawling_body(start_list, self.listnum)

            results.extend(body_results)
            print(f'******Finished page crawling - page: {i}, list: {index}******')
            page_end = time.time()
            print(f'---{i}페이지 완료, -걸린 시간: {page_end - page_start}, -건 수: {index}')
            i += 1

        end = time.time()
        print('entire time: ', end - start)

        # 크롬드라이버 종료
        # self.driver.close()
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
    bigkinds = CrawlingBigkinds()  # init에 기본값 설정해놓고 set함수 만들기
    # print(bigkinds.check_exist_file())
    start_page, start_list, exist_df = bigkinds.check_exist_file()
    # print(start_page, start_list)
    result_number = bigkinds.search_keyword()
    # print(result_number)
    results, state = bigkinds.crawling_contents(start_page, start_list)
    print(f'총 검색 결과: {result_number}, results 길이: {len(results)}, 상태: {state}')
    # results = ['','','', '']
    # state = 1
    bigkinds.save_to_csv(exist_df, results, state)

    # ==처음에 상세검색으로 날짜 지정하고 검색 시작 -첫화면url로 시작, 상세검색 클릭 후 날짜 먼저 지정==
    # csv name = 키워드_출처_시작날짜_끝날짜, 변수로 총 개수, 상태(실패 0, 정상 1)까지 반환
    # 중간에 끊겼을 때를 대비해 몇번째 페이지 몇번째 리스트부터 시작하도록 작성
    # 시작 페이지를 디폴트 0, 값이 있으면 그 값부터 하도록

    # 해당 제목으로 된 csv파일이 있는지 체크, 있으면 길이가 몇개인지 확인 후 시작 페이지, 인덱스 계산

    # jira
    # git 올리기, 상미씨 초대
    # 주석으로 누가 언제 무슨 이유로 무엇을 수정했다고 기록
    # 내 소스 정리 - 대현씨 소스 형식 맞춰서

