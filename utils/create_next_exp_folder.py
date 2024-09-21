import os

def create_next_exp_folder(base_path):
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
