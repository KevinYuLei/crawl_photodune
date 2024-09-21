import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_to_bottom(driver: webdriver.Chrome):
    # 获取页面目前总高度
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # 通过模拟滚动操作，逐步加载页面内容，直到内容加载完毕
    while True:
        driver.execute_script(f"window.scrollTo(0, {last_height})")
        time.sleep(1)
        
        # 获取当前滚动后的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 如果当前页面高度等于document.body.scrollHeight，说明到达页面底部，退出循环
        if abs(new_height - last_height) < 10: # 允许10像素的误差范围
            break
        else:
            last_height = new_height