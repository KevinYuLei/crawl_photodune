import re
import os


def extract_img_urls(html_file_path, save_path):
    # 打开并读取文件内容
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 正则表达式匹配 <img> 标签中的 src 属性
    img_src_pattern = r'<img[^>]+src="(?!data:)([^">]+)"'

    # 找到所有匹配的 src 属性值
    img_sources = re.findall(img_src_pattern, content)

    # 获取文件名称
    save_file = os.path.basename(save_path)
    # 输出结果
    with open(save_path, 'w', encoding='utf-8') as file:
        for src in img_sources:
            file.write(src + '\n')
    print(f'图片URL已提取并保存到{save_file} 文件中, 共: {len(img_sources)} 条url')
        
if __name__ == '__main__':
    cwd = os.getcwd()
    html_file = 'collected_content.txt'
    file_path = os.path.join(cwd, 'runs', html_file)
    save_filename = 'image_urls.txt'
    save_path = os.path.join(cwd, 'runs', save_filename)
    extract_img_urls(file_path, save_path)