import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm


class network():
    def __init__(self):
        self.df = None
        self.select_column = None

    def get_network(self, df, select_column):
        self.df = df
        self.select_column = select_column

    def network_list(self):
        text_list = list(self.df[self.select_column])
        # print('text_list\n+++++++++++++++++++++++++++=\n', text_list, '\n+++++++++++++++++++++++++++=\ntext_list')
        corpus = []
        corpus.append(' '.join(text_list))
        # print('coupus\n+++++++++++++++++++++++++++++++\n', corpus, '\n+++++++++++++++++++++++++++++++\ncoupus')
        return corpus

    def make_network(self, corpus):
        # print('corpus\n', corpus)
        net_tfidfVectorizer = TfidfVectorizer(max_features=50)
        net_dtm = net_tfidfVectorizer.fit_transform(corpus)

        # print(net_dtm)
        net_dtm_dense = net_dtm.todense()
        net_ttm = np.dot(net_dtm_dense.T, net_dtm_dense)
        words_name = net_tfidfVectorizer.get_feature_names_out()
        # print('net_ttm\n', net_ttm)

        # font_path = "../NanumGothic.ttf"
        # font_name = fm.FontProperties(fname="textin/python/NanumGothic.ttf").get_name()
        # plt.re('font', family=font_name)
        font = "AppleGothic"  # 변경 필요
        font_size = 16
        node_color = 'dodgerblue'
        edge_color = 'grey'
        plt.figure(figsize=(12, 10))
        g = nx.Graph(net_ttm[:, :])
        en_map = dict(zip(g.nodes(), words_name))

        # networkx의 layout 종류
        # layouts = {'spring': nx.spring_layout(g),
        #            'spectral': nx.spectral_layout(g),
        #            'shell': nx.shell_layout(g),
        #            'circular': nx.circular_layout(g),
        #            'kamada_kawai': nx.kamada_kawai_layout(g),
        #            'random': nx.random_layout(g),
        #            'fruchterman_reingold': nx.layout.fruchterman_reingold_layout(G)
        #            }
        pos = nx.spring_layout(g) # k= 노드들 사이의 거리, 숫자가 클수록 멀어짐. None일시 거리는 1/sqrt(n)로 설정 n=노드갯수
        nx.draw_networkx(g, pos=pos, labels=en_map, with_labels=True,
                font_family=font, font_size=font_size,
                node_color=node_color, node_size=800, node_shape='s',
                edge_color=edge_color, width=0.3)
        plt.savefig(f"{self.select_column}.png", facecolor='#eeeeee', bbox_inches='tight')
        print('분석이미지 저장 완료') # 이미지 출력 전에 저장을 해야 정상적으로 저장 됨
        plt.show()