import os
from utils.create_next_exp_folder import create_next_exp_folder
from utils.get_page_urls import get_page_urls
from utils.fetch_dynamic_content import fetch_dynamic_content
from utils.utils import urlset2dict, create_chrome_driver, get_urls_by_size
from utils.download_imgs import download_images_from_txt


if __name__ == '__main__':
    # 生成相关路径
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    imgs_dir = os.path.join(script_dir, 'downloaded_imgs')
    runs_dir = os.path.join(script_dir, 'runs')

    imgs_exp_dir = create_next_exp_folder(imgs_dir)
    runs_exp_dir = create_next_exp_folder(runs_dir)

    # 生成相关文件的路径
    urlset_filename = 'image_urls_srcsets.txt'
    urlset_path = os.path.join(runs_exp_dir, urlset_filename)

    urljson_filename = 'image_urls.json'
    urljson_path = os.path.join(runs_exp_dir, urljson_filename)

    size = '1600w'
    url_size_filename = 'image_urls_'+size+'.txt'
    url_size_path = os.path.join(runs_exp_dir, url_size_filename)
    # 创建浏览器对象
    driver = create_chrome_driver()
    
    # 需要爬取的photodune网址第一页
    # epx1 - feet on desk
    first_page_url = r'https://photodune.net/search/feet%20on%20desk#content'

    # 调用方法 获取系列页面url列表
    urls = get_page_urls(driver, first_page_url)

    # 调用方法 依次获得每个页面的img_srcset数据，并保存至txt中
    for i, url in enumerate(urls):
        fetch_dynamic_content(driver, url, urlset_path, i)

    # 调用方法 生成img_url.json
    urlset2dict(urlset_path, 0, urljson_path)
    
    # 调用方法抽取对应size的img的url
    get_urls_by_size(urljson_path, size, url_size_path)
    
    # 调用方法 下载图片
    download_images_from_txt(url_size_path, imgs_exp_dir)
