from es import from_es
import pandas as pd
from preprocessing import Preprocessor
from morph_analysis import Morph

class DataDict:

    def __init__(self):
        # dataframe
        self.df = None

        # 생성되는 데이터 프레임들을 기억하는 부분
        self.columns = None

        self.select_column = None

        # dict에 각 dataframe 컬럼명으로 데이터를 저장
        self.dict = {}

        self.fes = None

        self.morph_analysis = None

        self.ps = None

    # preprocess 총괄 함수
    def start_preprocess(self, options=None, keywords=None):

        if self.morph_analysis == None:
            self.morph_analysis = Morph()
            self.morph_analysis.select_func(int(input("형태소 선택 //  1: Okt  //  2: Mecab")))

        if self.df == None:
            self.fes = self.get_df()

        if self.ps == None:
            self.ps = Preprocessor()

        for i in range(10):
            self.clean(options, keywords)
            print("다른 데이터로 전처리를 진행하실꺼면 1, 종료는 2 : ")
            if input() == '2':
                self.fes.send_es(self.df, self.select_column)
                break

    # elasticsearch로 부터 dataframe을 갖고 옴
    def get_df(self):
        fes = from_es.FromES()
        dict_df = fes.get_data()
        print(*dict_df.keys(), sep="\n")
        print("원하는 dataframe 선택:")
        df_name = input()
        self.df = dict_df[df_name].loc[1:]
        self.df = self.df.reset_index(drop=True)
        self.df.columns = ['original']
        self.dict['original'] = self.df

        return fes

    def _input_options(self):
        print("# 1 : 특수문자  /  2 : 영문  / 3 : 숫자  /  4 : 한자 / 5 : 해당 키워드 삭제  /  6 : 해당 키워드가 있는 문서 삭제")
        options = list(map(int, input("하고자 하는 옵션 :").split(",")))
        print(options)
        if 5 in options or 6 in options:
            keywords = input("삭제할 keyword :").split(',')
        else: keywords = None
        return options, keywords

    def clean(self, options=None, keywords=None):

        self.columns = list(self.dict.keys())
        print("현재 갖고 있는 dataframe :", self.columns)
        self.select_column = input("전처리를 할 dataframe 선택 : ")
        self.df = self.dict[self.select_column]
        if options == None:
            options, keywords = self._input_options()

        _name = 'preprocess_'

        for i in range(10):
            # 처음 입력받은 dataframe 정제 => null값 제거
            self.ps.df, self.ps.select_column = self.df, self.select_column
            self.ps.delete_field(keywords)

            self.df = self.ps.df

            if len(self.dict) <= 1:
                _col_num = 0
                self._create_df(_col_num)

            else:
                _col_list = self.columns
                _col_list.sort(reverse=True)
                _col_num = int(list(filter(lambda x: _name in x, _col_list))[0].split("_")[-1])
                self._create_df(_col_num)

            # 옵션에 따른 전처리 실행
            # 1 : 특수문자  /  2 : 영문  / 3 : 숫자  /  4 : 한자 제거  /  5 : 해당 키워드 삭제  /  6 : 해당 키워드가 있는 문서 삭제
            if options != None:
                print(options)
                # self.ps.clean_text(options, keywords)
                self.ps.clean_text(self.df, self.select_column, options, keywords)


            self.dict[self.select_column] = self.ps.df

            print(_col_num, "차 전처리 완료")
            print(self.dict[self.select_column])
            print("추가 전처리 1 / 종료 2")
            if input() == '2':
                break
            else:
                print("column list :", self.columns)
                _select_column = input("수정할 Column, Default는 최근 전처리한 column :")
                if _select_column != '':
                    self.select_column = _select_column
                self.df = self.dict[self.select_column]
                options, keywords = self._input_options()

        morph_options = list(map(str, input("추출하고자 하는 형태소, 1:명사, 2:동사, 3:형용사 :").split(",")))

        self.morph_analysis.get_morph(self.df, self.select_column, morph_options)

    def _create_df(self, col_num):
        # self.columns.append(_name + str(_col_num+1))
        # print("nameeeeeeeeeeeeeeeeeeeeeeeeeeee : ", self.select_column)
        # if len(self.dict) == 1:
        # print(self.dict[self.select_column])
        # print("*************************************************")
        self.select_column = 'preprocess_' + str(col_num+1)

        tmp_df = pd.DataFrame(self.df)
        tmp_df.columns = [self.select_column]
        self.df = tmp_df.dropna().reset_index(drop=True)
        self.dict[self.select_column] = self.df
        self.columns = list(self.dict.keys())
        self.df = self.dict[self.select_column]