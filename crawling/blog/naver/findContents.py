import re
from crawling.common.reformat import Reformat

rework = Reformat()

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
        # print(an_wTime)
        if len(wTime) != len(an_wTime):
            # wTime = Find_contents.re_wTime(an_wTime)
            wTime = Reformat.re_date(self, an_wTime)
            # wTime = rework.re_wTime(an_wTime)
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

    def find_page_count(self, text):
        page_num = int(text.replace(",", '').replace("건", ""))
        page_count = int(page_num / 7) + 1
        if page_count == 0:
            page_count = 1
        return page_count