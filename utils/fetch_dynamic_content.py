import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from utils import scroll_to_bottom


def fetch_dynamic_content(url, save_file_path):
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
    count = 1
    failed_count = 0

    parent_element = driver.find_element(By.CSS_SELECTOR, element_selector)
    img_divs = parent_element.find_elements(By.XPATH, './div')

    # 获取保存路径下的文件名称
    save_filename = os.path.basename(save_file_path)
    # 将收集的HTML内容保存到txt文件中
    with open(save_file_path, 'w', encoding='utf-8') as file:
        for img_div in img_divs:
            # 写到这里
            
            
            
            li_elements = img_div.find_elements(By.XPATH, './li')
            for li_element in li_elements:
                a_element = li_element.find_element(
                    By.XPATH, "./div/div[@class='imgpt']/a")
                actions.move_to_element(a_element).click().perform()

                time.sleep(0.5)
                new_url = driver.current_url
                driver.execute_script(f"window.open('{new_url}', '_blank');")
                # 获取所有打开的标签页句柄
                tabs = driver.window_handles
                # 切换到新标签页
                driver.switch_to.window(tabs[-1])
                time.sleep(0.01)
                actions.send_keys(Keys.F5).perform()
                
                
                img_element_selector = "#mainImageWindow > div.mainImage.wide.notbkg.current.curimgonview > div > div > div > img"
                try:
                    actions.send_keys(Keys.F5).perform()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, img_element_selector))
                    )
                except (NoSuchElementException, TimeoutException) as e:
                    print(f"捕获到异常: {e}")
                    print(f"第{count}条图片数据获取失败.")
                    count += 1
                    failed_count += 1
                    
                    # 关闭当前标签页
                    driver.close()

                    # 切换回原始标签页
                    driver.switch_to.window(tabs[0])
                    actions.send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.01)
                    continue


                img_element = driver.find_element(
                    By.CSS_SELECTOR, img_element_selector)
                img_src = img_element.get_attribute("src")
                urls_list.append(img_src)

                # 关闭当前标签页
                driver.close()

                # 切换回原始标签页
                driver.switch_to.window(tabs[0])
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(0.01)
                file.write(img_src+'\n')
                print(f'已成功读取第{count}条图片数据: {img_src}')
                count += 1
        # 关闭浏览器，释放资源
        driver.quit()
        print(f"Urls内容已保存到 {save_filename} 文件中。")
        print(f"共爬取{count}条数据，其中爬取失败: {failed_count}条，存储成功：{len(urls_list)}条")


if __name__ == '__main__':
    bing_img_url = "https://cn.bing.com/images/search?q=smartphone+on+the+desk&qs=n&form=QBIR&sp=-1&lq=0&pq=smartphone%20on%20the%20desk&sc=7-22&cvid=FB071787232E4B959DF4D4F6EF0F3F1B&ghsh=0&ghacc=0&first=1&cw=1903&ch=653"

    cwd = os.getcwd()
    runs_folder = os.path.join(cwd, 'runs')

    html_filename = 'image_urls.txt'
    html_file_path = os.path.join(runs_folder, html_filename)

    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    fetch_dynamic_content(bing_img_url, html_file_path)
