class Naver_blog_xpath():
    def __init__(self):
        super(Naver_blog_xpath).__init__()
        # xpath 경로들
        self.period_setting_button = """// *[ @ id = "content"] / section / div[1] / div[2] / div / div / a"""  # 기간 설정
        self.set_period_button = """//*[@id="periodSearch"]"""  # 기간 적용
        self.start_date_button = """//*[@id="search_start_date"]"""  # 시작 날짜 입력
        self.end_date_button = """//*[@id="search_end_date"]"""  # 끝나는 날짜 입력
        self.page_all_text = """// *[ @ id = "content"] / section / div[1] / div[2] / span / span / em"""  # 총 검색 건수
        self.all_date = """//*[@id="content"]/section/div[1]/div[2]/div/div/div/a[1]"""  # 기간 전체
        self.one_week = """//*[@id="content"]/section/div[1]/div[2]/div/div/div/a[2]"""  # 최근 1주
        self.one_month = """//*[@id="content"]/section/div[1]/div[2]/div/div/div/a[3]"""  # 최근 1달

class Tstory_blog_xpath():
    def __init__(self):
        super(Tstory_blog_xpath, self).__init__()
        self.period_setting_button = """//*[@id="blogColl"]/div[2]/div/div[1]/a"""  # 기간 설정
        self.set_period_button = """//*[@id="blogColl"]/div[2]/div/div[1]/div/div/button"""  # 기간 적용
        self.start_date_button = """//*[@id="datepicker"]"""  # 시작 날짜
        self.end_date_button = """//*[@id="dp1624882221568"]"""  # 종료 날짜
        self.page_all_text = """// *[ @ id = "blogColl"] / div[1] / div[2] / span"""  # 검색 건수
        self.next_page_button = """//*[ @ id = "pagingArea"]/span/span[3]/a"""  # 다음 페이지
        self.select_blog = """//*[@id="blogColl"]/div[2]/div/div[2]/a"""
        self.select_tstory = """//*[@id="blogColl"]/div[2]/div/div[2]/div/ul/li[3]/a"""  # 티스토리 선택
        self.all_date = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[1]/a"""  # 전체
        self.one_day = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[2]/a"""  # 최근 1일
        self.one_week = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[3]/a"""  # 최근 1주
        self.one_month = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[4]/a"""  # 최근 1달
        self.six_month = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[5]/a"""  # 최근 6달
        self.one_year = """//*[@id="blogColl"]/div[2]/div/div[1]/div/ul/li[6]/a"""  # 최근 1년




