import pandas as pd
import os

import crawlingconfig
import tstory
import naver
import bigkinds

# def printl(x):
#     print(x)
class Main():
    def __init__(self):
        self._keyword = '에그타르트'
        self._site = 'naver'
        self._start_date = '20210901'
        self._end_date = '20211130'
        # 결과 저장 csv 파일명
        self.base_name = f'{self._keyword}_{self._site}_{self._start_date}_{self._end_date}'
        self.save_path = crawlingconfig.save_path

    # def __call__(self, *args, **kwargs):
    #     return self.check_file()

    def check_file(self):
        print('check file()')
        url_ing = 0
        body_ing = 2
        url_file = f'{self.save_path}{self.base_name}_{url_ing}.csv'
        body_file = f'{self.save_path}{self.base_name}_{body_ing}.csv'
        if os.path.isfile(url_file):
            exist_df = pd.read_csv(url_file)
            exist_index = len(exist_df.index)
            print(f'URL 작업 중인 파일이 존재 합니다. 행 수: {exist_index}')
            start_page, start_list = self.cal_start(url_ing, exist_index)
        # 수정 필요
        elif os.path.isfile(body_file):
            exist_df = pd.read_csv(url_file)
            exist_index = len(exist_df.index)
            print(f'본문 작업 중인 URL 파일이 존재 합니다. 행 수: {exist_index}')
            start_page, start_list = self.cal_start(body_ing, exist_index, url_file)
        else:
            print(f'작업을 새로 시작합니다.')
            exist_df = pd.DataFrame(columns=["title", "date", "content", "url"])
            start_page = 1
            start_list = 1
        return exist_df, start_page, start_list

    # 수정 필요
    def cal_start(self, state, index, *args):
        print('cal_start')
        start_page = 1
        start_list = 1
        if self._site == 'naver':
            if state == 0:
                print('naver url')
                start_page = int(index / 7) + 1

            if state == 2:
                print('naver body')
                url_file = pd.read_csv(args.url_file)
                start_list = url_file['url'][-1:].index

        if self._site == 'tstory':
            if state == 0:
                print('tstory url')
                start_page = int(index / 7) + 1

            if state == 2:
                print('tstory body')
                url_file = pd.read_csv(args.url_file)
                start_list = url_file['url'][-1:].index

        if self._site == 'bigkinds':
            if state == 2:
                print('bigkinds body')
                start_page = int(index / self.listnum + 1)
                start_list = index % self.listnum

        return start_page, start_list

    def start_crawling(self):
        df, start_page, start_list = self.check_file()
        if self._site == 'naver':
            if os.path.isfile(f'{self.save_path}{self.base_name}_1.csv'):
                naver.bodycrawling(df, start_page, start_list)
            else:
                naver.urlcrawling(df, start_page, start_list)
        if self._site == 'tstory':
            if os.path.isfile(f'{self.save_path}{self.base_name}_1.csv'):
                tstory.bodycrawling(df, start_page, start_list)
            else:
                tstory.urlcrawling(df, start_page, start_list)
        if self._site == 'bigkinds':
            bigkinds.bodycrawling(df, start_page, start_list)


if __name__ == '__main__':
    crawling = Main()
    # print(crawling.check_file())
    print(crawling.start_crawling())

