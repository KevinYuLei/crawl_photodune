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

from utils import scroll_to_bottom


def get_page_urls(first_page_url):
    # 设置Chrome浏览器的选项，确保浏览器不会显示自动化工具控制的提示信息
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')  # 禁用GPU加速（可选）
    options.add_argument('--start-maximized')  # 启动时最大化窗口

    # 启动Chrome浏览器，使用上述配置
    driver = webdriver.Chrome(options=options)

    # 通过Chrome DevTools Protocol (CDP) 禁用webdriver特征检测，使浏览器看起来像是由人操作的
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    # 访问bing/images页面
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