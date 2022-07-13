import pandas as pd
import re
from konlpy.tag import Mecab
from konlpy.tag import Okt


# 인터페이스 Preprocessor
# clean()
# tokenizer()

def remove_words(documents, words_list):
    results = pd.DataFrame(columns=['removed'])
    for document in documents:
        for word in words_list:
            document = document.replace(word, '')
        document = re.sub(r'\s+', ' ', document)
        results.loc[results.shape[0]] = document
    return results

# class needs to impliment Preprocessor
class Preprocessor:
    def __init__(self):
        self.okt = Okt()
        self.ko_mecab = Mecab()

    def clean(self, documents, options, words_list):
        # print('clean()')
        # print(documents)
        # print('docs type', type(documents)) # <class 'pandas.core.series.Series'>
        # print(options)
        results = pd.DataFrame(columns=['cleaned'])
        # (옵션4)입력단어 제거 - 양이 많아지면 오래걸리지 않을까? 단어 단위 처리니까 토크나이징에서?

        for document in documents:
            # print('doc type', type(document)) # str
            # (옵션1)특수문자 제거
            if 1 in options:
                document = re.sub(r'[\-\=\+,\#\/\?\:\^\.\@\*\"\※\~\ㆍ\!\』\‘\|\(\)\[\]\`\'\…\》\”\’\·\{\}]', '', document)

            # (옵션2)영문 제거
            if 2 in options:
                document = re.sub(r'[a-zA-Z]', '', document)

            # (옵션3)숫자 제거
            if 3 in options:
                document = re.sub(r'[0-9]', '', document)

            if 4 in options:
                # documents = remove_words(documents, stop_words)
                for word in words_list:
                    document = document.replace(word, '')
                # for word in stop_words:
                #     document = document.replace(word, '')
            document = re.sub(r'\s+', ' ', document)
            # document = re.sub('[ +]', ' ', document)
            # 처리되지 않는 띄어쓰기 존재 - '    텀  영상 요약  군사 갤러리_ 초기형 키모드 달린거는 총열이 얇아서 쏘다보면 명중률이 떨어지는 문제가 있었음 의 수명이 만발이라는 카더라성 정보를 본적 있는대 아마 이거 버투스가 구버전에 비해 무거워진 이유가 저거였나보내 '
            results.loc[results.shape[0]] = document
        # print('result', type(results))
        return results  # 리턴을 Dataframe? Series? (인자 받을 때는 시리즈임)

    def tokenize(self, documents, option, *user_pos):
        _results = pd.DataFrame(columns=['tokenized'])
        # 기본 품사, 사용자 설정 품사 추가
        reuslt_pos = ['Noun', 'Adjective']  # pos = part of speech : 품사
        if user_pos:
            for pos in user_pos[0]:
                reuslt_pos.append(pos)

        for document in documents:
            # print(type(document))
            result_words = []
            # (옵션1)okt
            if option == 'okt':
                pos = self.okt.pos(document, stem=True)
                # print('okt')
            # (옵션2)mecab
            elif option == 'mecab':
                pos = self.okt.pos(document, stem=True)
                # print('mecab')
            else:
                print('잘못된 토크나이저 입니다.')
                raise Exception

            for word in pos:  # 어간 추출 (norm: 들어가신다, stem: 들어가다)
                # print(word, type(word))  # 튜플 ('차세대', 'Noun')
                if word[1] in reuslt_pos:
                    result_words.append(word[0])
                # print(result_words)
            _results.loc[_results.shape[0]] = ' '.join(result_words)
            # print(results)
        return _results


# if __name__ == '__main__':
#     print('start')
#     df = pd.read_csv('시그 mcx_네이버블로그_20190101_20211125.csv')
#     docs = df['text']
#     clean_options = [1, 2, 3, 4]
#     stop_words = ['안녕하세요', '핸드가드', '개런드']
#     token_option = 'mecab'  # okt, mecab
#
#     pp = Preprocess()
#     result_df = pp.clean(docs, clean_options, stop_words)
#     corpus = result_df['cleaned']
#     # print('corpus', corpus, type(corpus))
#     # results = pp.tokenize(corpus, 'okt')
#     results = pp.tokenize(corpus, token_option, 'Josa', 'Adverb')
#     # {'Adjective': '형용사', 'Adverb': '부사', 'Alpha': '알파벳', 'Conjunction': '접속사', 'Determiner': '관형사',
#     # 'Eomi': '어미', 'Exclamation': '감탄사', 'Foreign': '외국어, 한자 및 기타기호', 'Hashtag': '트위터 해쉬태그',
#     # 'Josa': '조사', 'KoreanParticle': '(ex: ㅋㅋ)', 'Noun': '명사', 'Number': '숫자', 'PreEomi': '선어말어미',
#     # 'Punctuation': '구두점', 'ScreenName': '트위터 아이디', 'Suffix': '접미사', 'Unknown': '미등록어', 'Verb': '동사'}
#     print(results)