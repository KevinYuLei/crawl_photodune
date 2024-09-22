import os

def create_next_exp_folder(base_path: str):
    """
    创建下一个可用的实验文件夹，命名格式为 'exp{i}'，其中 i 从 0 开始递增。
    此方法检查指定的基本路径下是否存在名为 'exp{i}' 的文件夹。
    如果存在，i 自增，直到找到不存在的文件夹，然后创建该文件夹。

    Args:
        base_path (str): 实验文件夹所在的基础路径。

    Returns:
        str: 新创建的实验文件夹的路径。

    Examples:
        >>> create_next_exp_folder('/path/to/run')
        Created folder: /path/to/run/exp0!
        '/path/to/run/exp0'
    """
    i = 0
    # 循环检查 exp{i} 文件夹是否存在
    while True:
        folder_name = f"exp{i}"
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            # 如果不存在，则创建文件夹并退出循环
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}!")
            return folder_path
        else:
            # print((f"Existed folder: {folder_path}!"))
            pass
        i += 1

if __name__ == "__main__":
    # 设置基础路径，例如 './run'
    cwd = os.getcwd()
    base_path_1 = os.path.join(cwd, 'downloaded_imgs')
    base_path_2 = os.path.join(cwd, 'runs')
    create_next_exp_folder(base_path_1)
    create_next_exp_folder(base_path_2)
