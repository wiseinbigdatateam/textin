import pandas as pd
import os

import crawlingconfig
from bigkinds import Bigkinds
import save


# def printl(x):
#     print(x)
class Main():
    def __init__(self):
        # 사용자 입력값
        self._keyword = '에그타르트'
        self._site = 'bigkinds'
        self._start_date = '20211101'
        self._end_date = '20211130'

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

        if os.path.isfile(url_ing_file):
            exist_df = pd.read_csv(url_ing_file)
            exist_index = len(exist_df.index)
            exist_state = url_ing
            print(f'URL 작업 중인 파일이 존재 합니다. 행 수: {exist_index}')

        elif os.path.isfile(body_ing_file):
            try:
                exist_df = pd.read_csv(url_fin_file)
                exist_index = len(exist_df.index)
                print(f'본문 작업 중인 URL 파일이 존재 합니다. 행 수: {exist_index}')
                exist_state = body_ing
            except:
                if not os.path.isfile(url_ing_file):
                    print(f'본문 작업 중인 파일이 있으나, 완료된 URL 파일이 존재하지 않습니다.')
                    return
        else:
            print(f'작업을 새로 시작합니다.')
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
        save.save_to_csv(self.save_path, self.base_name, exist_df, exist_state, results, state)


if __name__ == '__main__':
    crawling = Main()
    crawling.start_crawling()

