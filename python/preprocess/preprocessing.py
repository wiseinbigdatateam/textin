import pandas as pd
from variable import pattern_dict

class Preprocessor:

    def __init__(self):
        # dataframe
        self.df = None

        self.select_column = None

    def clean_text(self, df, select_column, options, keywords=None):
        self.df = df
        self.select_column = select_column

        if len(options) > 1:
            for num in options: self.del_pattern(num, keywords)
        else:
            self.del_pattern(options[0], keywords)

    # Null값 제거, keyword 리스트가 있을 경우 해당 키워드가 있는 문서도 제거
    def delete_field(self, keywords=None):

        # 키워드가 여러개 있을 경우 list로 받음
        if type(keywords) == list:
            for keyword in keywords:
                self.df = self.df[self.df[self.select_column].str.contains(keyword) == False]

        # 키워드 1개만 삭제할 경우
        elif type(keywords) == str:
            self.df = self.df[self.df[self.select_column].str.contains(keywords) == False]

        # 키워드가 삭제되면서 문서가 null이 될 수도 있기에 dropna를 항상 함
        self.df = pd.DataFrame(self.df)
        self.df = self.df.dropna().reset_index(drop=True)


    # 특정 키워드 제거
    def del_pattern(self, num, keywords):
        print("**********************del_pattern****************************")
        print(keywords)
        if num < 5:
             self.df[self.select_column] = self.df[self.select_column].str.replace(pattern_dict[num], ' ', regex=True)

        elif num == 5 and keywords != None:
            print(keywords)
            for keyword in keywords:
                self.df[self.select_column] = self.df[self.select_column].str.replace(keyword, ' ')

        # 옵션 6 : 해당 키워드가 있는 문서 삭제
        elif num == 6 and keywords != None:
            self.delete_field(keywords)

        self.df[self.select_column] = self.df[self.select_column].str.replace(' +', ' ', regex=True)