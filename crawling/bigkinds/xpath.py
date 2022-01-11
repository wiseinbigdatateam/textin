# def crawling_body에서 사용하는 본문 크롤링용 xpath
class BigkindsXpath:
    # search_keyword()
    detail_xpath = '//*[@id="news-search-form"]/div/div[1]/button'
    datetab_xpath = '//*[@id="news-search-form"]/div/div[1]/div[2]/div/div[1]/div[1]/a'
    start_xpath = '//*[@id="search-begin-date"]'
    end_xpath = '//*[@id="search-end-date"]'
    keyword_xpath = '//*[@id="total-search-key"]'
    result_xpath = '//*[@id="news-results-tab"]/div[2]/h3/span[1]/span'
    result_number_xpath = '//*[@id="news-results-tab"]/div[2]/h3/span[6]'
    ten_xpath = '//*[@id="select2"]/option[1]'
    thirty_xpath = '//*[@id="select2"]/option[2]'
    fifty_xpath = '//*[@id="select2"]/option[3]'
    hundred_xpath = '//*[@id="select2"]/option[4]'

    # move_to_page()
    page_num_xpath = '//*[@id="paging_news_result"]'

    # crawling_body()
    title_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1'
    category_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/div/span'
    date_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul/li[1]'
    content_xpath = '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]'
    # 모달창 닫기 xpath
    modal_close_xpath = '//*[@id="news-detail-modal"]/div/div/div[2]/button'
    # 다음글 xpath
    next_xpaths = ['//*[@id="news-detail-modal"]/div/div/div[1]/div/div[4]/ul/li[2]/dd/a',
                   '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[3]/ul/li[2]/dd/a',
                   '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[3]/ul/li[3]/dd/a',
                   '//*[@id="news-detail-modal"]/div/div/div[1]/div/div[4]/ul/li[3]/dd/a'
                   ]






