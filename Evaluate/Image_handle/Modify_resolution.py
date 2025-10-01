from PIL import Image
import os

def resize_image(input_path, output_path, new_width, new_height):
    # 打开图像
    with Image.open(input_path) as img:
        # 改变分辨率（resize方法会按新尺寸缩放）
        resized_img = img.resize((new_width, new_height))
        # 保存处理后的图像
        resized_img.save(output_path)

# 批量处理文件夹中的图片
input_folder = "D:\\Ships_dataset"
output_folder = "D:\\New_Ships_dataset"
new_size = (1024, 768)  # 目标分辨率（宽，高）

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有图片
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):  # 筛选图片格式
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        resize_image(input_path, output_path, new_size[0], new_size[1])