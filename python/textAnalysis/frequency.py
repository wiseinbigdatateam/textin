import numpy as np
import pandas as pd
import itertools
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from tabulate import tabulate
from wordcloud import WordCloud

class Frequency():

    def __init__(self):
        self.df = None
        self.select_column = None


    # 빈도 만드는 파트
    def get_freq(self, df, select_column):
        self.df = df
        self.select_column = select_column

    def _get_word_freq(self):
        _word_frequency = Counter(' '.join(list(self.df[self.select_column])).split(' ')).most_common(100)
        print(tabulate(_word_frequency, headers=['Word', 'Frequency']))

    def _get_tfidf_score(self):
        _corpus = list(itertools.chain(list(self.df[self.select_column])))
        _tfidfv = TfidfVectorizer().fit(_corpus)
        _tfidfv_arr = _tfidfv.transform(_corpus).toarray()
        _tfidfv_vocab = _tfidfv.vocabulary_
        _tmp_df = pd.DataFrame(_tfidfv_arr)
        _tmp_df.columns = sorted(_tfidfv_vocab)
        _tmp_df = _tmp_df.T
        _tmp_df['sum'] = _tmp_df.sum(axis=1)
        print(_tmp_df['sum'].nlargest(100, keep='first'))

    def getWordcloud(self, matrix, words, width=1200, height=800, margin=2,
                 ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
                 color_func=None, max_words=200, min_font_size=4,
                 stopwords=None, random_state=None, background_color='black',
                 max_font_size=None, font_step=1, mode="RGB",
                 relative_scaling='auto', regexp=None, collocations=True,
                 colormap=None, normalize_plurals=True, contour_width=0,
                 contour_color='black', repeat=False,
                 include_numbers=False, min_word_length=0, collocation_threshold=30):

        vector = TfidfVectorizer()
        matrix = vector.fit_transform(list(self.df[self.select_column]))
        words = vector.get_feature_names_out()
        cnt_matrix = matrix.sum(axis=0)
        cnt = np.squeeze(np.asarray(cnt_matrix))
        word_cnt = list(zip(words, cnt))

        wc = WordCloud(font_path="../NanumGothic.ttf", width=width, height=height, margin=margin,
                 ranks_only=ranks_only, prefer_horizontal=prefer_horizontal, mask=mask, scale=scale,
                 color_func=color_func, max_words=max_words, min_font_size=min_font_size,
                 stopwords=stopwords, random_state=random_state, background_color=background_color,
                 max_font_size=max_font_size, font_step=font_step, mode=mode,
                 relative_scaling=relative_scaling, regexp=regexp, collocations=collocations,
                 colormap=colormap, normalize_plurals=normalize_plurals, contour_width=contour_width,
                 contour_color=contour_color, repeat=repeat,
                 include_numbers=include_numbers, min_word_length=min_word_length, collocation_threshold=collocation_threshold)

        cloud = wc.generate_from_frequencies(dict(word_cnt))
        cloud.to_file("./tmp/test.jpg")

if __name__ == "__main__":
    print("hi")