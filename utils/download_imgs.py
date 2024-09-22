import requests
import os


def download_image(session: requests.Session, url: str, save_dir: str, image_name: str):
    """
    _下载指定 URL 的图片并保存到指定的目录下。_

    该方法通过传入的 requests 会话对象和图片 URL 下载图片，并将其保存为指定的文件名。

    Args:
        session (requests.Session): 已配置的请求会话，用于发送 HTTP 请求。
        url (str): 图片的 URL 地址。
        save_dir (str): 图片保存的目录路径。
        image_name (str): 保存图片时使用的文件名，不需要包含扩展名。

    Returns:
        None: 图片下载完成后会打印相关信息。如果下载失败，会捕获并打印异常。

    Examples:
        >>> session = requests.Session()
        >>> download_image(session, 'https://example.com/image.jpg', './images', 'image_00001')
        Image downloaded and saved as: image_00001.jpg
    """
    # 生成图片保存路径
    save_path = os.path.join(save_dir, f"{image_name}.jpg")

    try:
        # 发送请求获取图片数据
        response = session.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 将图片数据写入文件
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Image downloaded and saved as: {image_name}.jpg")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")


def load_urls_from_txt(file_path: str):
    """
    _从指定的txt文件中加载图片URL列表。_

    该方法读取txt文件中的每一行，并返回一个 URL 列表，忽略空行。

    Args:
        file_path (str): 包含图片 URL 的 txt 文件路径。

    Returns:
        list: 包含所有图片 URL 的列表。

    Examples:
        >>> urls = load_urls_from_txt('./urls.txt')
        ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
    """
    # 从txt文件中加载URL
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]  # 去除空行
    return urls


def download_images_from_txt(file_path: str, save_dir: str):
    """
    _从指定的txt文件中加载图片 URL，并将每张图片下载到指定目录。_

    该方法创建一个会话对象，加载 URL 列表，使用自定义请求头和代理配置，然后逐个下载每张图片，并按照 `image_{i}` 命名保存。

    Args:
        file_path (str): 包含图片 URL 的 txt 文件路径。
        save_dir (str): 下载图片保存的目录路径。

    Returns:
        None: 下载完成后打印每张图片的保存信息。

    Examples:
        >>> download_images_from_txt('./urls.txt', './images')
        Image downloaded and saved as: image_00000.jpg
        Image downloaded and saved as: image_00001.jpg
    """
    
    # 如果保存目录不存在，则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 加载URL列表
    urls = load_urls_from_txt(file_path)

    # 创建一个会话对象
    session = requests.Session()

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

    # 更新会话的请求头和代理配置
    session.headers.update(headers)
    session.proxies.update(proxies)

    # 遍历所有图片 URL，下载每一张图片，并按指定格式命名
    for i, url in enumerate(urls):
        image_name = f"image_{i:05d}"  # 生成填充到5位的文件名
        download_image(session, url, save_dir, image_name)


if __name__ == '__main__':
    # 示例用法
    txt_file_path = r'D:\DesktopShortcut\Project\MyUtils\crawl_photodune\runs\exp0\image_urls_1600w.txt'  # 存储URL的txt文件路径
    save_directory = r'D:\DesktopShortcut\Project\MyUtils\crawl_photodune\downloaded_imgs\exp0'  # 设置保存图片的目录

    download_images_from_txt(txt_file_path, save_directory)
