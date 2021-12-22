import pandas as pd
import os

import crawlingconfig
# from bigkinds import Bigkinds
import save

from naverTestVer2 import NaverBlog
from tStoryTestVer2 import TstoryBlog


class Main():
    def __init__(self):
        # 사용자 입력값
        self._keyword = '시그 mcx'
        self._site = 'tstory'
        self._start_date = '2021121'
        self._end_date = '20211222'

        ## 입력받아서 할수 있게 임시로 만들어둔것 입니다. 
        # self._keyword = input('검색어를 입력해 주세요 : ')
        # self._site = input("naver, tstory, bigkinds 중 원하는 사이트를 입력해주세요 : ")
        # self._start_date = input('시작 날짜를 입력해 주세요 (ex. 2021041) : ')
        # self._end_date = input('종료 날짜를 입력해 주세요 (ex. 2021129) : ')

        # 결과 저장 csv 파일명
        self.base_name = f'{self._keyword}_{self._site}_{self._start_date}_{self._end_date}'
        self.save_path = crawlingconfig.save_path

    # def __call__(self, *args, **kwargs):
    #     return self.check_file()

    def check_file(self):
        print('check file()')
        url_ing = 0
        url_fin = 1
        body_ing = 2
        body_fin = 3
        url_ing_file = f'{self.save_path}{self.base_name}_{url_ing}.csv'
        url_fin_file = f'{self.save_path}{self.base_name}_{url_fin}.csv'
        body_ing_file = f'{self.save_path}{self.base_name}_{body_ing}.csv'
        body_fin_file = f'{self.save_path}{self.base_name}_{body_fin}.csv'

        if os.path.isfile(body_fin_file):
            print('본문 크롤링 완료된 파일이 존재합니다.')
            quit()

        elif os.path.isfile(url_fin_file):
            print('url 크롤링이 완료된 파일이 존재합니다.')
            exist_df = url_fin_file
            exist_index = len(pd.read_csv(url_fin_file).index)
            exist_state = url_fin

        elif os.path.isfile(url_ing_file):
            exist_df = pd.read_csv(url_ing_file)
            exist_index = len(exist_df.index)
            exist_state = url_ing
            print(f'URL 작업 중인 파일이 존재 합니다. 행 수: {exist_index}')

        elif os.path.isfile(body_ing_file):
            try:
                exist_df = pd.read_csv(body_ing_file)
                exist_index = len(exist_df.index)
                print(f'본문 작업 중인 URL 파일이 존재 합니다. 행 수: {exist_index}')
                exist_state = body_ing
            except:
                if not os.path.isfile(url_ing_file):
                    print(f'본문 작업 중인 파일이 있으나, 완료된 URL 파일이 존재하지 않습니다.')
                    # url 수집 시작하는 함수 넣기

        else:
            print(f'작업을 새로 시작합니다.')
            # if os.path.isfile(body_ing_file) and os.path.isfile(url_ing_file):
            #     exist_df = pd.DataFrame(columns=["title", "url"])
            # else:
            #     exist_df = pd.DataFrame(columns=["title", "date", "content", "url"])
            exist_df = pd.DataFrame(columns=["title", "date", "content", "url"])
            exist_index = len(exist_df)
            if self._site == 'bigkinds':
                exist_state = 2
            else:
                exist_state = 0
            print(exist_index)
        return exist_df, exist_index, exist_state

    def start_crawling(self):
        # df, start_page, start_list = self.check_file()
        exist_df, exist_index, exist_state = self.check_file()
        print(exist_df, exist_index)
        # if self._site == 'naver':
        #     if os.path.isfile(f'{self.save_path}{self.base_name}_1.csv'):
        #         # naver.bodycrawling(exist_df, exist_index)
        #     else:
        #         # naver.urlcrawling(exist_df, exist_index)
        # if self._site == 'tstory':
        #     if os.path.isfile(f'{self.save_path}{self.base_name}_1.csv'):
        #         # tstory.bodycrawling(exist_df, exist_index)
        #     else:
        #         # tstory.urlcrawling(exist_df, exist_index)
        if self._site == 'bigkinds':
            # bigkinds.bodycrawling(df, start_page, start_list)
            bk = Bigkinds(self._keyword, self._start_date, self._end_date)
            results, state = bk.crawling_body(exist_df, exist_index, exist_state)
            print(f'-----result: {results}\n -----state: {state}')

        elif self._site == 'naver':
            nb = NaverBlog(self._keyword, self._start_date, self._end_date)
            if exist_state != 1:
                first_result_df, state, exist_df = nb.url_crawling(exist_df, exist_index, exist_state)
                url_csv = save.save_to_csv(self.save_path, self.base_name, exist_df, exist_state, first_result_df, state)
                if exist_state == 1:
                    exist_df, exist_state, results_df, state = nb.main_crawling(url_csv, exist_state)

            else:
                print("네이버 url 수집 완료된 파일 존재")
                exist_df, exist_state, results_df, state = nb.main_crawling(exist_df, exist_state)

        elif self._site == 'tstory':
            ts = TstoryBlog(self._keyword, self._start_date, self._end_date)
            if exist_state != 1:
                first_result_df, state, exist_df = ts.url_crawling(exist_df, exist_index, exist_state)
                url_csv = save.save_to_csv(self.save_path, self.base_name, exist_df, exist_state, first_result_df,state)
                exist_df, exist_state, results_df, state = ts.main_crawling(url_csv, exist_state)
            else:
                print("T스토리 url 수집 완료된 파일 존재")
                exist_df, exist_state, results_df, state = ts.main_crawling(exist_df, exist_state)

        save.save_to_csv(self.save_path, self.base_name, exist_df, exist_state, results_df, state)


if __name__ == '__main__':
    crawling = Main()
    crawling.start_crawling()