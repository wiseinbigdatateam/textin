import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search

class FromES:

    def __init__(self):

        # domain 설정
        self.domain = "3.38.45.198"

        # port 설정 : default는 9200
        self.port = 9200

        self.host = str(self.domain) + ":" + str(self.port)

        # ElasticSearch 객체 생성
        self.es = Elasticsearch(self.host)

        # 입력할 topic, default는 None으로 설정
        self.idx = None

    # ES에서 data를 받아 오는 함수
    def get_data(self, idx=None):

        # 입력 받은 idx가 있다면 self.idx로 저장
        self.idx = idx

        # 입력 받은 idx가 없다면 전체 리스트 호출
        if self.idx == None:
            self.idx = self.get_idx_list()
            print(*self.idx, sep='\n')
            print("----------------------------------------")

            # idx_list를 출력하여 사용자가 어떤 idx를 할지 직접입력, 1개 이상 가능
            # 잘못된 idx 입력시 에러 파트 아직 작성안함
            self.idx = list(input().split(","))
            self.idx = [idx.strip() for idx in self.idx]
            print('----------------------------------------')
            print(*self.idx, sep="\n")

        idx_col_dict = self.get_col(self.idx)


        # DataFrame을 지정할 dict 생성
        # idx별 df를 저장하기 위해 dict로 생성

        key = idx_col_dict
        s = Search(using=self.es, index=key)
        df = pd.DataFrame([hit.to_dict() for hit in s.scan()])
        return df

        # df_dict = {}
        # for key in idx_col_dict.keys():
        #     s = Search(using=self.es, index=key)
        #     df = pd.DataFrame([hit.to_dict() for hit in s.scan()])
        #     df_dict[key] = (df[idx_col_dict[key]])
        #
        # print("DataFrame의 개수 :", len(df_dict))
        #
        # return df_dict


    # 특정 indices를 입력하지 않았을 경우 모든 indices 출력
    def get_idx_list(self):
        indice_list = sorted(self.es.indices.get_alias().keys())
        idx_list = [key for key in indice_list if not key.startswith(".")]

        return idx_list

    # 유효한 column 추출
    def get_col(self, idx):
        idx_col_dict = {}

        if type(self.idx) == list:
            for key in self.idx:
                idx_col_dict[key] = self.find_col(key)

        else: idx_col_dict[self.idx] = self.find_col(self.idx)

        return idx_col_dict

    # 해당 idx로 들어가 column만 추출
    def find_col(self, key):
        not_ues_col = ['Id', 'log', 'event', '@timestamp', 'message', 'host', '@version']
        tmp_index = self.es.search(index=key)
        test_keys = list(tmp_index['hits']['hits'][0]['_source'].keys())
        valid_keys = [key for key in test_keys if key not in not_ues_col]

        return valid_keys

# if __name__ == "__main__":
#         test = FromES()
#         tm = test.get_data()
#         print(*tm.keys(), sep="\n")
#         col = input()
#         print(tm[col])