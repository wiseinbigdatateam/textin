from urllib.parse import quote
import time
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from blogXpath import Naver_blog_xpath
from blogXpath import Tstory_blog_xpath

qText = "시그 mcx"
start_date = "2019.01.1"  # 시작날짜
end_date = "2021.11.25"  # 종료날짜
chromedriver_path = '/Applications/chromedriver'  # 크롬드라이버 경로


def open_site(driver, args):
    if args == 1:
        xpath_root = Naver_blog_xpath()
        url = "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=" + quote(
            qText)
        driver.get(url)
        driver.implicitly_wait(10)

        if start_date != "" and end_date != "":
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정
            time.sleep(1)

            # 시작날짜를 입력하는 부분
            ## 체크
            s_date = driver.find_element_by_xpath(xpath_root.start_date_button)
            driver.find_element_by_xpath(xpath_root.start_date_button).click()
            s_date.clear()
            time.sleep(0.5)
            for c in start_date:
                s_date.send_keys(c)
                time.sleep(0.2)
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()
            time.sleep(0.5)
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()

            # 종료날짜를 입력하는 부분
            e_date = driver.find_element_by_xpath(xpath_root.end_date_button)
            driver.find_element_by_xpath(xpath_root.end_date_button).click()
            e_date.clear()
            time.sleep(0.5)
            for c in end_date:
                e_date.send_keys(c)
                time.sleep(0.2)
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()
            time.sleep(0.5)
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()
            driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용
        else:
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()
            driver.find_element_by_xpath(xpath_root.one_week).click()
        time.sleep(2)

    elif args == 2:
        xpath_root = Tstory_blog_xpath()
        url = "https://search.daum.net/search?w=blog&f=section&SA=tistory&lpp=10&nil_src=blog&q=" + quote(
            qText) + "&p=1"
        driver.get(url)
        driver.implicitly_wait(10)

        if start_date and end_date != "":
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정

            s_date = driver.find_element_by_xpath(xpath_root.start_date_button)
            driver.find_element_by_xpath(xpath_root.start_date_button).click()
            s_date.clear()
            time.sleep(0.5)
            for c in start_date:
                s_date.send_keys(c)
                time.sleep(0.25)

            click_num = start_date.split(".")[-1]
            driver.find_element_by_link_text(f"{click_num}").click()

            e_date = driver.find_element_by_xpath(xpath_root.end_date_button)
            driver.find_element_by_xpath(xpath_root.end_date_button).click()
            e_date.clear()
            time.sleep(0.5)
            for c in end_date:
                e_date.send_keys(c)
                time.sleep(0.25)

            click_num = end_date.split(".")[-1]
            driver.find_element_by_link_text(f"{click_num}").click()
            driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용

        else:
            driver.find_element_by_xpath(xpath_root.period_setting_button).click()  # 기간설정
            driver.find_element_by_xpath(xpath_root.one_day).click()  # 1일
            driver.find_element_by_xpath(xpath_root.set_period_button).click()  # 적용
        time.sleep(1)
        driver.find_element_by_xpath(xpath_root.select_blog).click()  # 출처 (블로그 종류)
        driver.find_element_by_xpath(xpath_root.select_tstory).click()  # 티스토리 선택
        time.sleep(1)

    return driver


def set_driver(webdriver, args):
    window_size = "1200,800"
    chrome_options = Options()
    # chrome_options.add_argument('headless') # 창 안뜨게
    chrome_options.add_argument(f"--window-size={window_size}")  # 창 사이즈
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.implicitly_wait(10)  # 페이지 로딩될때까지 최대 몇초까지 기다릴것인지
    url = open_site(driver, args).current_url
    driver.implicitly_wait(15)
    driver.get(url)
    time.sleep(1)

    return driver, url
