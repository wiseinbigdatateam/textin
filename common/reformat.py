import datetime
import time
import re
import requests as requests
from bs4 import BeautifulSoup


class Reformat:
    def __init__(self):
        self.url = None
        self.text = None
        self.an_wTime = None
        self.wTime = None

    def delete_iframe(self, url):
        self.url = url
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        src_url = "http://blog.naver.com/" + soup.iframe["src"]

        return src_url

    def re_date(self, an_wTime):
        # 20시간 전 처럼 표현되는 시간표현 수정
        # 현재 시간에서 표시된 숫자만큼 시간을 뺴준뒤 그 결과를 리턴
        self.an_wTime = an_wTime
        if an_wTime != '':
            mtime = int(an_wTime)
            # print("mtime" ,mtime)
            today_date = datetime.datetime.now()
            test_time = today_date - datetime.timedelta(hours=mtime)
            date_format = "%Y. %m. %d. %H:%M"
            re_time = test_time.strftime(date_format)
            wTime = re_time

        print("시간 수정 완료")
        return wTime

    # 상태값을 받아오는걸로 네이버 티스토리 구분하ㅐ서 돌아가게 하기
    def re_tTime(self, wtTime):  # 티스토리 시간값 변경
        self.an_wTime = wtTime
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
        wtTime = re.sub(korean, '', wtTime)
        wtTime = re.sub('[a-zA-z]', '', wtTime)
        wtTime = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '', wtTime)
        wtTime = re.sub("\n", '', wtTime)

        return wtTime

    def text_cleaning(self, text):
        startTime = time.time()
        self.text = text

        text = text.replace("\n", "")
        pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'  # E-mail 제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'  # URL제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '<[^>]*>'  # HTML 태그 제거
        text = re.sub(pattern=pattern, repl='', string=text)
        pattern = '[^\w\s]'  # 특수기호제거
        text = re.sub(pattern=pattern, repl='', string=text)

        endTime = time.time()
        # print(f"간단 전처리 소요시간 : {endTime - startTime:.5f} 초")
        return text