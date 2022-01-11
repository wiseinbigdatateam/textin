import pandas as pd

from preprocess.preprocessor import Preprocessor, remove_words
from textAnalysis.cwordcloud import Cwordcloud

from collections import Counter

# if __name__ == '__main__':
class Analysis:
    def __init__(self):
        ### preprocess
        self.clean_options = [1, 2, 3, 4]
        self.stop_words_1 = ['안녕하세요', '핸드가드', '개런드']
        self.token_option = 'mecab'  # 'okt', 'mecab'
        self.added_pos = ['Adverb', 'Josa']
        # {'Adjective': '형용사', 'Adverb': '부사', 'Alpha': '알파벳', 'Conjunction': '접속사', 'Determiner': '관형사',
        # 'Eomi': '어미', 'Exclamation': '감탄사', 'Foreign': '외국어, 한자 및 기타기호', 'Hashtag': '트위터 해쉬태그',
        # 'Josa': '조사', 'KoreanParticle': '(ex: ㅋㅋ)', 'Noun': '명사', 'Number': '숫자', 'PreEomi': '선어말어미',
        # 'Punctuation': '구두점', 'ScreenName': '트위터 아이디', 'Suffix': '접미사', 'Unknown': '미등록어', 'Verb': '동사'}
        self.foption = 'tfidf' # 'count', 'tfidf'
        self.stop_words_2=['있다', '이다']


    def start_analysis(self):
        print('Anaysis start')
        # db 연결
        df = pd.read_csv('시그 mcx_네이버블로그_20190101_20211125.csv', index_col=0)

        ### preprocess
        pp = Preprocessor()
        docs = df['text']
        cleaned_result = pp.clean(docs, self.clean_options, self.stop_words_1)
        cleaned_df = pd.concat([df, cleaned_result], axis=1)
        cleaned_docs = cleaned_df['cleaned']
        tokenized_results = pp.tokenize(cleaned_docs, self.token_option, self.added_pos)

        tokenized_df = pd.concat([cleaned_df, tokenized_results], axis=1)
        corpus = list(tokenized_df['tokenized']) # list를 써야하는 분석이 있는 경우 = 공통(DB연결 위해) => def 1. (df, column) -> list    2. df, column, list -> df['clom'=list   3. replace
        # ======분리
        ### 빈도, wordcloud
        clean_corpus = remove_words(corpus, self.stop_words_2)
        corpus = list(clean_corpus['removed'])
        an = Cwordcloud()
        word_count = an.frequency(corpus, self.foption)  # 'count', 'tfidf'
        an.wordcloud(word_count)

if __name__ == '__main__':
    an = Analysis()
    an.start_analysis()