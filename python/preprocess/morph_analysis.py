from konlpy.tag import *
from textAnalysis.frequency import Frequency
import platform
import itertools
import pandas as pd
from variable import pos_dict, stopwords

class Morph:

    def __init__(self):
        self.df = None
        self.select_column = None
        self.func = None
        self.func_name = None

    # 형태소 선택
    def select_func(self, num):
        if num == 1:
            self.func = Okt()
            self.func_name = 'okt'
        else:
            self.func_name = 'mecab'

            if platform.system() == "Windows":
                self.func = Mecab("C:/mecab/mecab-ko-dic")
            else:
                self.func = Mecab()


    # 형태소 분석
    def get_morph(self, df, select_column, options):

        print(select_column)
        print(df)
        morph_list = list(itertools.chain.from_iterable([pos_dict[self.func_name][num] for num in options]))
        print(morph_list)

        df[select_column] = df[select_column].apply(lambda x: self._extract_morph(x, morph_list))

        morph_name = 'morph_' + select_column

        df[morph_name] = df[select_column].apply(lambda x: self._extract_morph(x, morph_list))
        select_column = morph_name
        df = pd.DataFrame(df[select_column], columns=[select_column])
        # self.dict[self.select_column] = self.df
        # self.columns.append(self.select_column)

        # 토픽모델링
        # _topic = TopicModeling()
        # print('+++++++++++TopicModeling start+++++++++++')
        # _topic.get_topic(df, select_column)
        # result_corpus, dictionary, words = _topic.get_list()
        # _topic.getPyKDAvis(result_corpus, dictionary, words)
        # print('+++++++++++TopicModeling finished+++++++++++')

        # 네트워크 분석
        # _network = network()
        # print('+++++++++++Network start+++++++++++')
        # _network.get_network(df, select_column)
        # result_corpus = _network.network_list()
        # _network.make_network(result_corpus)
        # print('+++++++++++Network finished+++++++++++')

        _freq = Frequency()
        _freq.get_freq(df, select_column)
        _freq._get_word_freq()
        _freq._get_tfidf_score()

        return df

    def _extract_morph(self, text, morph_list):
        try:
            if self.func_name == 'okt':
                text = ' '.join(list(zip(*list(filter(lambda x: x[-1] in morph_list and x[0] not in stopwords and len(x[0])>1,
                                                      self.func.pos(text, norm=True, stem=True)))))[0])
            else:
                text = ' '.join(list(zip(*list(filter(lambda x: x[-1] in morph_list and x[0] not in stopwords and len(x[0])>1, self.func.pos(text)))))[0])
        except: text = ''
        finally: return text