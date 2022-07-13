# -*- coding: utf-8 -*-
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.callbacks import CoherenceMetric
from gensim.models.callbacks import PerplexityMetric
import logging
import pyLDAvis.gensim_models
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import os

from analysis.analysisConfig import SAVE_PATH

import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)

class TopicModeling():
    def __init__(self, file_name):
        self.save_path = SAVE_PATH
        self.file_name = file_name

    def getTopicModelingDic(self, text_list):
        words = []
        for document in text_list:
            words.append(document.split(' '))
        # print(words)  # [['차세대', '분대', '화기', '미육군', '진행중', '신형', '식', '화기',

        # 정수 인코딩과 빈도수 생성
        dictionary = corpora.Dictionary(words)
        # print('dictionary', dictionary)  # dictionary Dictionary(572 unique tokens: ['가능성', '가능하다', '가스', '가장', '간단하다']...)

        # 출현빈도가 적거나 자주 등장하는 단어는 제거 ??????????? 나중에 제거(테스트 데이터 양적어서 제거하면 데이터 사라짐...)
        # dictionary.filter_extremes(no_below=10, no_above=0.05)

        corpus = [dictionary.doc2bow(word) for word in words]
        # print('corpus[0]', corpus[0])  # corpus[0] [(0, 1), (1, 3), (2, 1), (3, 2), (4, 4), #(word, frequency)

        # 최적의 토픽 수 찾기
        # self.find_optimal_number_of_topics(dictionary, corpus, words)
        return corpus, dictionary, words

    def getPyLDAvis(self, corpus, dictionary, words):
        file_name = f'{self.save_path}{self.file_name}_pyLDAvis.html'
        # print(type(corpus), corpus)  # <class 'list'> [[(0, 1), (1, 3), (2, 1), (3, 2), (4, 4), (5, 2), (6, 2), (7, 2), (8, 1), (9, 5), (10, 1), (11, 1), (12, 1),
        # print(type(dictionary), dictionary)  # <class 'gensim.corpora.dictionary.Dictionary'> Dictionary(572 unique tokens: ['가능성', '가능하다', '가스', '가장', '간단하다']...)
        # print(type(words), words)  # <class 'list'> [['차세대', '분대', '화기', '미육군', '진행중', '신형', '식', '화기', '개발', '사업', '기존', '총탄', '한계', '총탄', '장점',

        perplexity_logger = PerplexityMetric(corpus=corpus, logger='shell')
        coherence_logger = CoherenceMetric(corpus=corpus, coherence="u_mass", logger='shell')

        lda_model = LdaModel(corpus, id2word=dictionary, num_topics=8, passes=30,
                             callbacks=[coherence_logger, perplexity_logger])

        topics = lda_model.print_topics(num_words=20)

        # for topic in topics:
        # print(topic)

        coherence_model_lda = CoherenceModel(model=lda_model, texts=words, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        # print('\nCoherence Score (c_v): ', coherence_lda)

        coherence_model_lda = CoherenceModel(model=lda_model, texts=words, dictionary=dictionary, coherence="u_mass")
        coherence_lda = coherence_model_lda.get_coherence()
        # print('\nCoherence Score (u_mass): ', coherence_lda)

        lda_visualization = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary, sort_topics=False)
        pyLDAvis.save_html(lda_visualization, file_name)

    # def compute_coherence_values(self, dictionary, corpus, texts, limit, start=2, step=3):
    #     coherence_values = []
    #     model_list = []
    #     for num_topics in range(start, limit, step):
    #         model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    #         model_list.append(model)
    #         coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
    #         coherence_values.append(coherencemodel.get_coherence())
    #
    #     return model_list, coherence_values
    #
    # def find_optimal_number_of_topics(self, dictionary, corpus, processed_data):
    #     file_name = f'{self.save_path}{self.file_name}_topicModeling_score.png'
    #
    #     limit = 20
    #     start = 2
    #     step = 2
    #
    #     model_list, coherence_values = self.compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=processed_data,
    #                                                             start=start, limit=limit, step=step)
    #     x = range(start, limit, step)
    #     plt.plot(x, coherence_values)
    #     plt.xlabel("Num Topics")
    #     plt.ylabel("Coherence score")
    #     plt.legend(("coherence_values"), loc='best')
    #     plt.show()
    #
    #     plt.savefig(file_name)

if __name__ == '__main__':
    corpus = [
        '차세대 분대 화기 미육군 진행중 신형 식 화기 개발 사업 기존 총탄 한계 총탄 장점 신형 총탄 도입 함 동시 과거 미군 사용 화기 대체 신형 탄약 사용 수 있다 소총 기관총 선정 사업 이다 경쟁 기업 총 곳 그 우어 제너럴 다이내믹스 텍스트 론 시스템 사격 통제 광학 장치 개발 사업 개그 오늘 볼 부문 그 사우 어사 강력하다 마케팅 진행중 스피어 해당 블로그 관련 글 이하 유튜브 채널 인터뷰 영상 기반 정리 동영상 그 디펜스 사업 개발 및 마케팅 담당자 미육군 년 복무 경력 제이슨 세인트 존 사업 본래 기존 플랫폼 탄약 사용 수 있다 크기 것 시작 사업 과거 미육군 진행 다른 개발 프로그램 위해 것 사업 등장 적절하다 판단 지원 사업 근본 의도 병사 기존 플랫폼 비슷하다 작법 를 지급 함 훈련 시간 단축 친숙하다 기존 기반 사이즈 소총 정도 기본 설계 구조 동일하다 대표 특징 접이식 개 머리 판 독특하다 내부 구조 덕분 가능하다 기능 좁다 공간 진입 차량 탑승 같다 상황 부피 수 있다 아주 유용하다 접이식 개 머리 판 접 때 완벽하다 고정 덜렁 거리 버튼 고리 같다 별다르다 동부 없이 간단하다 수 있다 기본 장전 손잡이 뿐 아니다 몸 왼쪽 측면 비 왕복 장전 손잡이 추가 소총 장전 손잡이 격발 시 왕복 운동 사용 몸 적 거리 오른손잡이 사수 입장 전통 계열 작법 달리 총기 몸 간단하다 조작 수 있다 의 강력하다 장점 중 하나 총기 모든 동부 손 조작 가능하다 직관 조작 간단하다 가스 조절 부 그 사업 가장 메리트 소통 기관 군경 현역 전역 민간 시장 유저 피드백 최대한 수집 설계 과정 최대한 반영 제작 다 융통성 있다 피드백 반영 함 현재 설계 사업 추구 결정 체 도달 볼 수 있다 다음 단계 도약 위 설계 교체 가능성 충분하다 존재 미래 민간 시장 유통 판매 것 기업 기준 년 월 약 개월 이후 정도 예상 다 총기 총탄 위해 개발 총열 교체 총탄 사용 수 있다 순정 탄창 발 랜서 탄창 사용 계열 탄창 모두 호환 가능하다 경쟁 사 탄환 다르다 하이브리드 설계 채택 때 한계 점 없다 궁극 하이브리드 설계 기존 탄피 바닥 부분 정도 스테인레스 스틸 제작 무게 구도 상승 탄환 관련 상세 정보 이하 나무 위키 문서 탄환 기반 설계 상당하다 압력 수 있다 구성 자랑 일반 탄약 압력 아니다 그 이상 탄약 폭발 압력 수 있다 충분하다 구도 신뢰 궁극 목표 사업 선정 를 소총 교체 플랫폼 기존 소총 유저 군경 사이 괜찮다 성능 구도 검증 이미 일부 국가 군경 현용 소총 도입 및 채택 특히 목적 하나 플랫폼 다양하다 탄약 사용 수 있다 모듈러 시스템 장점 이다 이렇다 소총 장점 사업 도입 시킴 시점 가장 유력하다 선정 후보 거론 있다 차세대 화기 사업 이름 미래 군인 화기 존 플랫폼 형태 아직 의존 입장 고수 것 아니다 비판 여론 또한 존재 소총 모듈러 시스템 엄청나다 장점 사업 유력하다 선정 후보 게 개인 입장 더 야하다 노릇 이다 추후 기관총 사업 미육군 그 우어 신형 기관총 지난 포스팅 간단하다 미육군 차세대 분대 화기 사업 경쟁 사 중 그 우어',
        '요즘 검은색 기본 달러 선 걍 거저 먹음 요즘 딱하다 급하다 없다 천천히 매물 보고 있다 도 뭐 젠 세팅할 생각',
        '세라 코트 맛집 마 이스터 이다 대략 정 이상 작업 듯 그만큼 대세 라이플 확실하다 세라 코트 때 더욱더 특별하다 라이플 듯 지금 작업 를 소개 최근 작업 컬러 이다 바디 상 하부 레일 스컬 레톤 스톡 모두 동일하다 색상 맞춤 아무리 색 버젼 해도 이렇게 통일 색감 기기 힘들다 완성 모습 못 조립 제품 고객 부럽다 고객 요청 비슷하다 다른 두 가지 컬러 믹스 매칭 작업 상부 적용 컬러 노란색 글록 색상 도색 하부 색상 조합 처음 사진 유튜브 사진 그 조합 이렇다 식 투톤 조합 최대한 사진 비슷하다 느낌 조합 색상 비교 색감 차이 확실하다 조립 완료 사진 고객 하나 돌격 소총 스타일 또 다른 사진 스타일 고객 만족하다 정말로 보람 찬 작업 지금 작업 색상 중 가장 많이 작업 그레이 색상 이다 그레이 크게 두 가지 있다 해당 색상 펄 세라 코트 택티컬 그레이 컬러 이다 택티컬 느낌 물씬 펄 있다 약간 빛 달라 매력 있다 감촉 또한 약간 표현 때문 섬세하다 듯 듯 라이플 너무 조합 이다 에어소프트 전문 리뷰 유튜버 로이 카브 동영상 소개 역시 택티컬 그레이 도색 처음 색상 콘셉트 대해 기도 항상 트렌드 로이 카브 방송 시청 후 동일 또는 비슷하다 컬러 작업 문의 많다 개인 그레이 약간 민 수용 느낌 강하 이상하다 조합 그렇다 느낌 이렇다 식 동일하다 택티컬 그레이 고객 요청 색감 좀 더 진하다 수도 있다 막상 더 어둡다 수 있다 묵직하다 느낌 블랙 가깝다 보이 펄 가득하다 다크 그레이 정말 멋 스럽다 레일 또한 레틀러 사이즈 컴팩트 느낌 블랙 색상 일 때 훨씬 더 강력하다 느낌 추가 탄피 배 출구 삽 쪽 부품 머 블랙 도색 전체 라이플 피막 구성 해당 작업 브론즈 색 이징 레일 바디 레틀러 레일 비슷하다 컬러 도색 사례 이다 사실 이징 느낌 세라 코트 내기 여러 가지 색상 조색 색상 이징 특유 메탈릭 느낌 힘들다 바디 상하 맥풀 그린 도색 우리 일반 알 있다 맥풀 스톡 색상 컬러 보시 처음 바디 추후 바디 색감 마음 레일 추가 작업 완성 그린 색상 를 직접 앞 세팅 트렌드 조심 예상 그레이 적용 색상 중 펄 안 리지 널 느낌 가장 흡사하다 그 다크 그레이 색상 이다 그레이 색상 실제 느낌 정말 차분하다 다크 그레이 적용 권총 바디 상하 고객 다양하다 컬러 작업 진심 대세 정도 매력 라이플 이다 이상 그 의 세라 코트 도색 포스팅 세라 코트 조금 더 독특하다 에어소프트 문화',
        '고정용 후크 체결 나중 메탈 프린터 금속 부품 생각 어요 대충 토이 스타 하부 결합 쪽 좀 상부 리시버 체결 용 베이스 이제 튼튼하다 고정 어음 배럴 고정용 클램프 부품 구멍 좀 어렵다 기도 실물 사진 안쪽 저렇게 파 총열 실물 없다 그루 브 개 하부 상 하부 결함 바디 핀 결합부 손 레버액션 하부 쪽 구도 위해 벽 증설 탄창 멈치 주변 둑 제작 촥 좌우 연동 탄창 멈 치가 바닥 눌렸을때 장애물 의하다 탄창 교체 일 방지 위해 저렇게 둑 또 있다 모양 실물 사진 상 하부 결 차 위해 포 맥스 도 기존 상부 리시버 좌우 두껍다 일 권총 손잡이 결 베이스 손잡이 뒤쪽 둥글다 부분 갈아 마지막 사진 더 지저분하다 그 버퍼 튜브 필요없다 구조 개 머리 판이 접힌채로 사격 가능하다 심지어 없다 문제 없다 그 개 머리 판 상황 취향 교체 간편하다 피카 티니 레일 뒤쪽 나 있다 특이하다 구조 의 조각 레일 사용 조금 두껍다 두께 조절 붙이 나사 조인 후 필요없다 레일 칸 덮어서 부분 칼 그대로 레일 각도 실물 사진 임시 조립 모습 뒤쪽 바디 핀 결합부 겸 내부 벽 두께 상부 조각 붙이 완성 아카데미 의 수축 개 머리 판 실물 약간 길다 제작 적당하다 조절 야하다 테이프 표시 개 머리 판이 이제 완전하다 안 요렇게 권총 손잡이 새롭다 만들기',
        '텀 영상 요약 군사 갤러리 초기 키 모드 총열 얇다 명중 률 문제 있다 의 수명 만발 카더라 정보 본적 있다 아마 거 버투스 버전 무겁다 이유 거']
    file_name = 'test'

    tm = TopicModeling(file_name)
    result_corpus, result_dic, words = tm.getTopicModelingDic(corpus)
    tm.getPyLDAvis(result_corpus, result_dic, words)
