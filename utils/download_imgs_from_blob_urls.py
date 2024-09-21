from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import os


def download_imgs_from_blob_urls(url_file_path, save_directory):
    # 创建保存图片的目录（如果不存在）
    os.makedirs(save_directory, exist_ok=True)
    
    # 读取txt文件中的所有URL
    with open(url_file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    
    # 设置Chrome浏览器的选项，确保浏览器不会显示自动化工具控制的提示信息
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')  # 禁用GPU加速（可选）
    options.add_argument('--start-maximized')  # 启动时最大化窗口
    options.add_argument("--headless")   # 启用无头模式

    # 启动 Selenium WebDriver (Chrome)
    driver = webdriver.Chrome(options=options)

    # 通过Chrome DevTools Protocol (CDP) 禁用webdriver特征检测，使浏览器看起来像是由人操作的
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    # 用于获取blob数据，并转换为Base64编码的JavaScript
    script = """
    var blob_url = arguments[0];
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', blob_url, true);
        xhr.responseType = 'blob';
        xhr.onload = function() {
            if (xhr.status === 200) {
                var reader = new FileReader();
                reader.onloadend = function() {
                    resolve(reader.result.split(',')[1]);  // 返回 base64 数据
                };
                reader.readAsDataURL(xhr.response);  // 将 blob 转为 base64
            } else {
                reject('Failed to fetch blob data.');
            }
        };
        xhr.send();
    });
    """
    
    # 遍历访问每个包含 blob URL 的页面
    for i, url in enumerate(urls):
        url = url.strip()   # 去掉换行符和空格
    
        # 访问包含 blob URL 的页面
        driver.get(url)

        # 获取 <img> 标签的 blob URL
        img_element = driver.find_element(By.TAG_NAME, "img")
        blob_url = img_element.get_attribute("src")

        # 执行 JavaScript 获取 blob 数据，并转换为 Base64 编码
        base64_data = driver.execute_script(script, blob_url)

        # 将 Base64 解码并保存为图像文件
        img_data = base64.b64decode(base64_data)

        image_path = os.path.join(save_directory, f'image_{i:05d}.jpg')

        with open(image_path, 'wb') as img_file:
            img_file.write(img_data)

        print(f"Image downloaded and saved to {image_path}")

    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    cwd = os.getcwd()

    url_file = 'image_urls.txt'
    url_file_path = os.path.join(cwd, 'runs', url_file)

    save_dir = os.path.join(cwd, 'downloaded_imgs')

    download_imgs_from_blob_urls(url_file_path, save_dir)
