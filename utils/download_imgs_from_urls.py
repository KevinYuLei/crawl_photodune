import os
import re
import requests
from urllib.parse import urlparse, parse_qs

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'DNT': '1',
}

# 代理配置（根据需要替换为实际代理地址和端口）
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 从URL或Content-Disposition头中提取文件名
def get_filename_from_url(url, response):
    # 1. 尝试从 Content-Disposition 响应头中获取文件名
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split("filename=")[-1].strip('"')
        return filename

    # 2. 尝试从 URL 中获取文件名
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # 3. 检查是否有查询参数提供文件名提示
    query_params = parse_qs(parsed_url.query)
    if 'dl' in query_params:
        filename = query_params['dl'][0]

    # 使用正则表达式清理文件名中的非法字符
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

    return filename if filename else f"downloaded_image.jpg"

# 下载图片的辅助函数，并保证名称递增，且带有正确的扩展名
def download_image(url, folder_path, image_count):
    try:
        # 使用会话，带上自定义 User-Agent
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url, stream=True, proxies=proxies)

            if response.status_code == 200:
                # 生成递增的图片文件名，确保为5位数，并加上正确的扩展名
                filename_from_url = get_filename_from_url(url, response)
                if not filename_from_url.lower().endswith(('.jpg')): # ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
                    filename_from_url += '.jpg'  # 默认使用 .jpg 扩展名

                # 限制文件名长度，不超过60个字符
                base_name, ext = os.path.splitext(filename_from_url)
                base_name = f"image_{image_count:05d}_{base_name}"
                if len(base_name) + len(ext) > 60:
                    base_name = base_name[:60 - len(ext)]
                
                base_name += ext

                # 生成保存路径
                image_path = os.path.join(folder_path, base_name)

                # 检查并创建文件夹
                os.makedirs(folder_path, exist_ok=True)

                # 保存图片
                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"第{image_count:04d}条图片, 下载成功: {base_name}")
            else:
                print(f"第{image_count:04d}条图片, 下载失败: {url}, 状态码: {response.status_code}")
    except Exception as e:
        print(f"发生错误: {e}")

# 主函数
def download_imgs_from_urls(img_url_path, save_dir):
    # 检查目标文件夹是否存在，不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 读取文件并逐行处理
    with open(img_url_path, 'r') as file:
        urls = file.readlines()

    image_count = 1  # 计数器从1开始

    # 下载所有图片URL
    for url in urls:
        url = url.strip()
        download_image(url, save_dir, image_count)
        image_count += 1  # 下载成功后递增计数器

if __name__ == "__main__":
    # 替换为你的文件路径和目标文件夹路径
    img_url_path = r"D:\DesktopShortcut\Project\MyUtils\crawl_bing_imgs\runs\exp5\image_urls.txt"  # 替换为 image_urls.txt 文件路径
    save_dir = r"D:\DesktopShortcut\Project\MyUtils\crawl_bing_imgs\downloaded_imgs\exp5"  # 替换为保存图片的文件夹路径

    download_imgs_from_urls(img_url_path, save_dir)
