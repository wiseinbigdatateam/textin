import datetime
from crawling.common.reformat import Reformat

rework = Reformat()

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

    def find_page_count(self, text):
        text = text.split("/")
        page_num = int(text[1].replace("건", "").replace("약", "").replace(",", ""))
        page_count = int(page_num / 10)
        if page_count == 0:
            page_count = 1
        return page_count