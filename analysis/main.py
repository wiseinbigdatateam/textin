import pandas as pd

from preprocess.preprocessor import Preprocessor, remove_words
from textAnalysis.cwordcloud import Cwordcloud


# if __name__ == '__main__':
class Analysis:
    print('Anaysis start')
    # db 연결
    df = pd.read_csv('시그 mcx_네이버블로그_20190101_20211125.csv', index_col=0)

    ### preprocess
    clean_options = [1, 2, 3, 4]
    stop_words_1 = ['안녕하세요', '핸드가드', '개런드']
    token_option = 'mecab'  # 'okt', 'mecab'

    pp = Preprocessor()
    docs = df['text']
    cleaned_result = pp.clean(docs, clean_options, stop_words_1)
    cleaned_df = pd.concat([df, cleaned_result], axis=1)
    cleaned_docs = cleaned_df['cleaned']
    tokenized_results = pp.tokenize(cleaned_docs, token_option, 'Adverb')
    # {'Adjective': '형용사', 'Adverb': '부사', 'Alpha': '알파벳', 'Conjunction': '접속사', 'Determiner': '관형사',
    # 'Eomi': '어미', 'Exclamation': '감탄사', 'Foreign': '외국어, 한자 및 기타기호', 'Hashtag': '트위터 해쉬태그',
    # 'Josa': '조사', 'KoreanParticle': '(ex: ㅋㅋ)', 'Noun': '명사', 'Number': '숫자', 'PreEomi': '선어말어미',
    # 'Punctuation': '구두점', 'ScreenName': '트위터 아이디', 'Suffix': '접미사', 'Unknown': '미등록어', 'Verb': '동사'}
    tokenized_df = pd.concat([cleaned_df, tokenized_results], axis=1)
    # print(tokenized_df)
    corpus = list(tokenized_df['tokenized'])

    ### 빈도, wordcloud
    stop_words_2=['있다']
    clean_corpus = remove_words(corpus[0], stop_words_2)
    corpus[0] = clean_corpus
    an = Cwordcloud()
    word_count = an.frequency(corpus, 'count')  # 'count', 'tfidf'
    print(word_count)
    an.wordcloud(word_count)

