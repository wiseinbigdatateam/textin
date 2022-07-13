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