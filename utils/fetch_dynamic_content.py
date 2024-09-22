import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from utils.utils import scroll_to_bottom


def fetch_dynamic_content(driver: webdriver.Chrome, url: str, save_file_path: str, fetch_times: int = 0):
    """
    _从动态加载的网页中获取图片 URL，并将其保存到指定文件。_

    该方法使用 Selenium 访问一个动态加载图片的网页，获取指定 CSS 选择器下的图片 URL，并将这些 URL 保存到文件中。
    它通过滚动页面、刷新和等待元素加载来确保可以抓取到所有动态内容。

    Args:
        driver (webdriver.Chrome): 已初始化的 Selenium Chrome 浏览器驱动。
        url (str): 目标网页的 URL。
        save_file_path (str): 保存抓取到的图片 URL 的文件路径。
        fetch_times (int, optional): 爬取次数，用于记录当前爬取的轮数，默认为0。

    Returns:
        tuple: 
            - list: 包含抓取到的图片 URL 的列表。
            - int: 当前轮次抓取到的图片 URL 数量。

    Examples:
        >>> driver = webdriver.Chrome()
        >>> urls, count = fetch_dynamic_content(driver, 'https://www.bing.com/images', './img_urls.txt')
        第1次爬取, 共爬取20条img_url, 已成功保存到 img_urls.txt 文件中
    """
    # 访问photodune页面
    driver.get(url)

    # 定位页面中用于展示图片的动态元素的CSS选择器
    element_selector = "#content > div.search-index_content__searchResults > main > div.search-index_content__searchResultsWrapper > div"

    # 创建ActionChains对象
    actions = ActionChains(driver)

    # 短暂停顿0.5s
    time.sleep(0.5)
    # 手动刷新页面确保能获取CSS选择器
    actions.send_keys(Keys.F5).perform()
    # 短暂停顿0.5s
    time.sleep(0.5)

    # 等待页面的初始加载，直到目标元素出现在页面中
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
    )

    scroll_to_bottom(driver)

    urls_list = []
    count = 0

    parent_element = driver.find_element(By.CSS_SELECTOR, element_selector)
    img_divs = parent_element.find_elements(By.XPATH, './div')

    # 获取保存路径下的文件名称
    save_filename = os.path.basename(save_file_path)
    # 将收集的HTML内容保存到txt文件中
    with open(save_file_path, 'a+', encoding='utf-8') as file:
        for img_div in img_divs:
            img_element = img_div.find_element(By.XPATH, './div/a/img')
            img_url = str(img_element.get_attribute('srcset'))
            file.write(img_url+'\n')

            urls_list.append(img_url)
            count += 1

    print(f"第{fetch_times+1}次爬取, 共爬取{count}条img_url, 已成功保存到 {save_filename} 文件中")
    return urls_list, count


if __name__ == '__main__':
    photodune_url = "https://photodune.net/search/feet%20on%20desk#content"

    cwd = os.getcwd()
    runs_folder = os.path.join(cwd, 'runs')

    urlset_filename = 'image_urls_srcsets.txt'
    urlset_file_path = os.path.join(runs_folder, urlset_filename)

    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    urls_list, count = fetch_dynamic_content(photodune_url, urlset_file_path)
    pass
