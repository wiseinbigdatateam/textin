# -*- coding: utf-8 -*-
import pyLDAvis
import pyLDAvis.gensim_models
from gensim.models.ldamodel import LdaModel
from gensim.models.callbacks import CoherenceMetric
from gensim.models.callbacks import PerplexityMetric
from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora
import gensim


class TopicModeling():
    def __init__(self):
        self.df = None
        self.select_column = None

    def get_topic(self, df, select_column):
        self.df = df
        self.select_column = select_column

    # df 리스트화
    def get_list(self):
        text_list = list(self.df[self.select_column])
        # print('text_list\n =============================\n', text_list)

        words = []
        for text in text_list:
            words.append(text.split(' '))
        # print('words\n++++++++++++++++++++++++++++++++++\n', words)

        dictionary = corpora.Dictionary(words)
        # dictionary.filter_extremes(no_below=2, no_above=0.5)  # 빈도가 2이상인 단어, 전체의 50퍼를 차지 하는 단어 필터링
        corpus = [dictionary.doc2bow(text) for text in words]
        # print('corpus\n+++++++++++++++++++++++\n', corpus)
        # print(len(dictionary))

        return corpus, dictionary, words


    def getPyKDAvis(self, corpus, dictionary, words):
        perplexity_logger = PerplexityMetric(corpus=corpus, logger='shell')
        coherence_logger = CoherenceMetric(corpus=corpus, coherence="u_mass", logger='shell')

        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=15)
        topics = ldamodel.print_topics(num_words=20)

        coherence_model_lda = CoherenceModel(model=ldamodel, texts=words, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score (c_v): \n', coherence_lda)

        coherence_model_lda = CoherenceModel(model=ldamodel, texts=words, dictionary=dictionary, coherence="u_mass")
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score (u_mass): \n', coherence_lda)

        # 저장하는 부분
        lda_visualization = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary, sort_topics=False)
        pyLDAvis.save_html(lda_visualization, f'{self.select_column}_test_pyLDAvis.html')
        print(f'{self.select_column}_test_pyLDAvis.html 저장 완료')