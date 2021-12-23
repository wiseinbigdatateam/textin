import datetime
import re

import reworkBlogContents
from reworkBlogContents import ReworkContents

rework = ReworkContents()


class FindNaverContents():
    def __init__(self):
        self.soup = None

    def find_title(self, soup):
        self.soup = soup
        if soup.find("div", class_="se-module se-module-text se-title-text"):
            title = soup.find("div", class_="se-module se-module-text se-title-text").text
            # print(f"title1 : {title}")

        elif soup.find("span", class_="pcol1 itemSubjectBoldfont"):
            title = soup.find("span", class_="pcol1 itemSubjectBoldfont").text
            # print(f"title2 : {title}")

        elif soup.find("h3", class_="se_textarea"):
            title = soup.find("h3", class_="se_textarea").text
            # print(f"title3 : {title}")

        return title

    # def re_wTime(wTime):
    #     # 20시간 전 처럼 표현되는 시간표현 수정
    #     # 현재 시간에서 표시된 숫자만큼 시간을 뺴준뒤 그 결과를 리턴
    #     if wTime != '':
    #         mtime = int(wTime)
    #         today_date = datetime.datetime.now()
    #         test_time = today_date - datetime.timedelta(hours=mtime)
    #         date_format = "%Y. %m. %d. %H:%M"
    #         re_time = test_time.strftime(date_format)
    #         wTime = re_time
    #
    #     return wTime

    def find_date(self, soup):
        self.soup = soup
        if soup.find(class_="se_publishDate pcol2"):
            wTime = soup.find(class_="se_publishDate pcol2").text
            # print(f"wTime1 : {wTime}")

        elif soup.find("p", class_="date fil5 pcol2 _postAddDate"):
            wTime = soup.find("p", class_="date fil5 pcol2 _postAddDate").text
            # print(f"wTime2 : {wTime}")

        # 한글 제거 후 길이가 다르면 시간 전처리 함수로 이동
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
        an_wTime = re.sub(korean, '', wTime)
        if len(wTime) != len(an_wTime):
            # wTime = Find_contents.re_wTime(an_wTime)
            wTime = reworkBlogContents.ReworkContents.re_wTime(an_wTime)
            wTime = rework.re_wTime(an_wTime)
            # print(f"wTime3 : {wTime}")
        return wTime

    def find_main_post(self, soup):
        self.soup = soup
        if soup.find(class_="se-main-container"):
            main_post = soup.find(class_="se-main-container").text
            # print(f"main_post1 : {main_post}")

        elif soup.find("div", id="postViewArea"):
            main_post = soup.find("div", id="postViewArea").text
            # print(f"main_post2 : {main_post}")

        elif soup.find("div", class_="se_component_wrap sect_dsc __se_component_area"):
            main_post = soup.find("div", class_="se_component_wrap sect_dsc __se_component_area").text
            # print(f"main_post3 : {main_post}")
        return main_post


class FindTsotryContents():
    def __init__(self):
        self.soup = None

    def find_title(self, soup):
        self.soup = soup
        if soup.find(class_="title"):
            title = soup.find(class_="title").text
        elif soup.select_one("h1"):
            title = soup.select_one("h1").text
        elif soup.find(class_="title-article"):
            title = soup.find(class_="title-article").text
        elif soup.find(class_="heading"):
            title = soup.find(class_="heading").text
        elif soup.find(class_="hd-heading lts-narrow p-name"):
            title = soup.find(class_="hd-heading lts-narrow p-name").text
        elif soup.find(class_="tit_post"):
            title = soup.find(class_="tit_post").text
        elif soup.find(class_="titleWrap"):
            title = soup.find(class_="titleWrap").text
        elif soup.find(class_="txt_sub_tit"):
            title = soup.find(class_="txt_sub_tit").text
        else:
            title = "제목 없음"
        title = title.replace("\n", "")
        # print("title : ", title)

        return title

    def find_date(self, soup):
        self.soup = soup
        if soup.find(class_="date"):
            wTime = soup.find(class_="date").text
        elif soup.find(class_="txt_detail my_post"):
            wTime = soup.find(class_="txt_detail my_post").text
            # wTime = re_tTime(wTime)
            wTime = rework.re_tTime(wTime)
        elif soup.find(class_="info-post"):
            wTime = soup.find(class_="info-post").text
            # wTime = re_tTime(wTime)
            wTime = rework.re_tTime(wTime)
        elif soup.find(class_="subinfo__date"):
            wTime = soup.find(class_="subinfo__date").text
        elif soup.find(class_="label label-info"):
            wTime = soup.find(class_="label label-info").text
        elif soup.find(class_="timeago dt-published"):
            wTime = soup.find(class_="timeago dt-published").text
        elif soup.find(class_="jb-article-information-date"):
            wTime = soup.find(class_="jb-article-information-date").text
        elif soup.find(class_="info_post"):
            wTime = soup.find(class_="info_post").text
        else:
            today_date = datetime.datetime.now()
            date_format = "%Y. %m. %d. %H:%M"
            wTime = today_date.strftime(date_format)
        # print("date : ", wTime)

        return wTime

    def find_main_post(self, soup):
        self.soup = soup

        if soup.find(class_="entry-content"):
            main_post = soup.find(class_="entry-content").text
        elif soup.find(class_="article"):
            main_post = soup.find(class_="article").text
        elif soup.find(class_="jb-article"):
            main_post = soup.find(class_="jb-article").text
        elif soup.find(class_="article_view"):
            main_post = soup.find(class_="article_view").text
        elif soup.find(class_="article_cont"):
            main_post = soup.find(class_="article_cont").text
        elif soup.find(class_="area-main"):
            main_post = soup.find(class_="area-main").text
        elif soup.find(class_="area-view"):
            main_post = soup.find(class_="area-view").text
        elif soup.find(class_="tt_article_useless_p_margin contents_style"):
            main_post = soup.find(class_="tt_article_useless_p_margin contents_style").text
        else:
            main_post = "본문 내용을 찾지 못함"

        main_post = rework.text_cleaning(main_post)
        return main_post