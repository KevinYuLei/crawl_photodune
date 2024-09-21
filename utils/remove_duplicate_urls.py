import os


def remove_duplicate_urls(file_path):
    # 读取文件内容并存储在集合中，以自动去除重复项
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    filename = os.path.basename(file_path)
    print(f"源文件'{filename}'包含url共: {len(urls)}条.")
    # 去除多余的空格和换行符，并使用集合去重
    unique_urls = set(url.strip() for url in urls if url.strip())

    # 将去重后的URL写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        for url in unique_urls:
            file.write(url + '\n')

    print(
        f"Removed duplicates. Unique URLs have been saved back to {file_path}.")
    print(f'去重后的文件包含url共: {len(unique_urls)}条.')


if __name__ == '__main__':
    # 文件路径
    url_file_path = r'D:\DesktopShortcut\Project\MyUtils\crawl_bing_imgs\runs\image_urls.txt'  # 需要处理的URL文件路径

    # 调用函数去除重复的URL
    remove_duplicate_urls(url_file_path)
