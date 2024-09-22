import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from utils.utils import scroll_to_bottom


def get_page_urls(driver:webdriver.Chrome, first_page_url: str):
    """
    _获取搜索页面的所有分页URL。_

    该方法从给定的第一页URL开始，利用Selenium滚动到底部并提取分页链接，生成从第一页到最后一页的所有分页URL。

    Args:
        driver (webdriver.Chrome): 已初始化的Selenium Chrome浏览器驱动。
        first_page_url (str): 搜索结果第一页的URL。

    Returns:
        list: 包含从第一页到最后一页所有分页的URL列表。

    Examples:
        >>> driver = webdriver.Chrome()
        >>> urls = get_page_urls(driver, 'https://photodune.com/search?page=1')
        >>> print(urls)
        ['https://photodune.com/search?page=1', 'https://photodune.com/search?page=2', ...]
    """
    # photodune搜索页面的第一页网址
    driver.get(first_page_url)
    
    scroll_to_bottom(driver)
    
    # 定位页面元素
    page_selector = "#content > div.search-index_content__searchResults > main > div.search-index_content__searchResultsWrapper > nav > ul"
    
    # 等待页面的初始加载，直到目标元素出现在页面中
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, page_selector))
    )
    page_element = driver.find_element(By.CSS_SELECTOR, page_selector)
    li_elements = page_element.find_elements(By.XPATH, './li')
    
    # 获取最后一页的网址表达
    last_page_href = li_elements[-2].find_element(By.XPATH, './a').get_attribute('href')
    # 使用正则表达式匹配 page= 后的数字
    match = re.search(r"page=(\d+)", last_page_href)
    if match:
        # 提取最大页码
        max_page = int(match.group(1))
        
        # 生成从1到 max_page 的所有url
        urls = [re.sub(r"page=\d+", f"page={i}", last_page_href) for i in range(1, max_page+1)]
    else:
        print("未找到匹配的页码")
    return urls
    

if __name__ == '__main__':
    # 需要爬取的photodune页面的第一页网址
    first_page_url = "https://photodune.net/search/feet%20on%20desk#content"
    

    page_urls = get_page_urls(first_page_url)
    for u in page_urls:
        print(u)