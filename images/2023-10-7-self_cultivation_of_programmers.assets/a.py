import os
import re

# 图片所在文件夹路径，需替换为实际路径
folder_path = './'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 使用正则表达式匹配文件名中的 20231024
    new_filename = re.sub(r'2023\d\d\d\d', '20231007', filename)
    if new_filename != filename:
        # 构建旧文件和新文件的完整路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        # 重命名文件
        os.rename(old_file_path, new_file_path)