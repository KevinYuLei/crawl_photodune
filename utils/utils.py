import time
import json
import re
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sleep_random_time(min_seconds: float, max_seconds: float):
    """
    _在指定的最小和最大秒数范围内，暂停程序执行一段随机时间。_

    Args:
        min_seconds (float): 最小睡眠时间（秒）。
        max_seconds (float): 最大睡眠时间（秒）。

    Examples:
        >>> sleep_random_time(1, 3)
        # 程序将暂停1到3秒之间的随机时间。
    """
    # 生成一个在 min_seconds 和 max_seconds 之间的随机时间
    sleep_time = random.uniform(min_seconds, max_seconds)

    # 打印生成的睡眠时间（可选）
    # print(f"Sleeping for {sleep_time:.2f} seconds")

    # 让程序暂停指定的时间
    time.sleep(sleep_time)


def create_chrome_driver():
    """
    _创建并返回配置过的Chrome浏览器驱动程序对象。_

    该方法通过设置浏览器选项，隐藏自动化控制提示并禁用某些特征检测，以使浏览器更像由人类操作。

    Returns:
        webdriver.Chrome: 配置好的Chrome浏览器驱动程序对象。

    Examples:
        >>> driver = create_chrome_driver()
        >>> driver.get('https://www.example.com')
    """
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
    return driver


def scroll_to_bottom(driver: webdriver.Chrome):
    """
    _滚动页面到底部，直到页面内容加载完毕。_

    通过模拟滚动操作，逐步加载动态内容，直到无法继续滚动为止。

    Args:
        driver (webdriver.Chrome): Chrome浏览器的Selenium驱动对象。

    Examples:
        >>> driver = create_chrome_driver()
        >>> driver.get('https://www.example.com')
        >>> scroll_to_bottom(driver)
    """
    # 获取页面目前总高度
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 通过模拟滚动操作，逐步加载页面内容，直到内容加载完毕
    while True:
        driver.execute_script(f"window.scrollTo(0, {last_height})")
        time.sleep(1)

        # 获取当前滚动后的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 如果当前页面高度等于document.body.scrollHeight，说明到达页面底部，退出循环
        if abs(new_height - last_height) < 10:  # 允许10像素的误差范围
            break
        else:
            last_height = new_height


def urlset2dict(srcset_filepath: str, start_index: int = 0, output_filepath: str = 'image_urls.json'):
    """
    _从srcset文件中解析图片的URL及对应大小，并以JSON格式保存。_

    Args:
        srcset_filepath (str): 存放srcset信息的txt文件路径。
        start_index (int): 生成图片序号的起始值。
        output_filepath (str): 输出的JSON文件路径。

    Returns:
        None: 将解析后的结果保存为JSON文件。

    Examples:
        >>> urlset2dict('srcset.txt', 0, 'image_urls.json')
    """
    # 打开并读取txt文件
    with open(srcset_filepath, 'r', encoding='utf-8') as file:
        srcsets = file.readlines()

    # 用于存储所有解析后的图片信息
    all_images = {}
    current_index = start_index

    # 定义正则表达式来解析每一条srcset
    pattern = r'(https?://[^\s]+)\s(\d+)w'

    # 逐行解析srcset
    for srcset in srcsets:
        # 查找所有符合正则的URL和图片大小
        matches = re.findall(pattern, srcset.strip())

        # # 如果找到匹配项，则将数据按 image_number 存储，构建图片数据并添加到列表
        if matches:
            image_data = {}
            for url, size in matches:
                image_data[f'{size}w'] = url

            # 以图片序号为键存储size和url的字典
            all_images[current_index] = image_data
            current_index += 1  # 每次递增图片序号
    # 将结果保存为JSON文件
    with open(output_filepath, 'w+', encoding='utf-8') as f:
        json.dump(all_images, f, indent=4, ensure_ascii=False)

    print(f"总计: {current_index}条数据, 已保存到 {output_filepath}")


def get_urls_by_size(json_path, size, save_path):
    # 读取json文件
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 存储 image_number 对应的 size url
    result = {}

    # 遍历每个 image_number, 获取对应size下的url
    with open(save_path, 'w', encoding='utf-8') as file:
        for image_number, sizes in data.items():
            # 如果该 image_number 下有对应的 size
            if size in sizes:
                result[image_number] = sizes[size]  # sizes[size] 为 url
                file.write(sizes[size]+'\n')
    print(f"已将图片尺寸为: {size} 的url提取至: {os.path.basename(save_path)}!")
    return result


if __name__ == '__main__':
    # srcset_filepath = r'D:\DesktopShortcut\Project\MyUtils\crawl_photodune\runs\image_urls_srcsets.txt'
    # output_filepath = r'D:\DesktopShortcut\Project\MyUtils\crawl_photodune\runs\image_data.json'

    json_path = r'D:\DesktopShortcut\Project\MyUtils\crawl_photodune\runs\exp0\image_urls.json'
    size = '1600w'
    save_filename = 'image_urls_'+size+'.txt'
    save_path = os.path.join(os.path.dirname(json_path), save_filename)
    get_urls_by_size(json_path, size, save_path)
