# JENKINS WEBHOOKTEST
# Textin Readme
### django : front 구성
- mysite : django project	폴더
- django에 gunicorn 및 nginx 연결
	- gunicorn 및 nginx 둘다 기본 포트 사용.
	- AWS 인스턴스 실행시 자동으로 gunicorn 및 nginx 시작.
### python : 분석 part
- es : ElasticSearch와 연결
	- from_es.py
- preprocess : 전처리 부분
	- preprocess : 전처리 실행
	- variable : 형태소, 불용어, 정규식 유형 저장

- Vue-django : Vue.js 3 버전이 설치됨
