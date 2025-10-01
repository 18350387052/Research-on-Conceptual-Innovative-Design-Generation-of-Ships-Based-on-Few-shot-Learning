import os
import numpy as np
from PIL import Image

def Check_image(input_path):
    # 打开图像
    with Image.open(input_path) as img:
        img_numpy = np.array(img).astype(float)
        if np.isnan(img_numpy).any() or np.isinf(img).any():
            return False
        return True


# 批量处理文件夹中的图片
input_folder = "D:/ProgramData/Experiment/resource"


# 遍历输入文件夹中的所有图片
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):  # 筛选图片格式
        input_path = os.path.join(input_folder, filename)
        result = Check_image(input_path)
        if result == False:
            print(f"{filename} 图像包含非法值，需替换或删除")
        elif result == True:
            print(f"{filename} 图像合法")
