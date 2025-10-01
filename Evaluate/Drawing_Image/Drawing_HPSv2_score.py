import os
import hpsv2
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
import pandas as pd

# 将 127.0.0.1:7890 替换为你自己的代理地址和端口
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

def convert_rgba_to_rgb(image: Image) -> Image.Image:
    """将RGBA图像转换为RGB"""
    if image.mode == 'RGBA':
        # 白色背景
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        return background
    elif image.mode != 'RGB':
        return image.convert('RGB')
    return image

def evaluate_images_with_hpsv2(image_paths: str,output_filename: str,file_type: int):
    """
    使用HPSv2评估图像

    """
    # 定义文本提示词，描述了期望生成的图像内容
    prompt = "This is a high-resolution photo of a tugboat sailing across calm turquoise waters. The vessel is predominantly white with green and red accents, and has a sturdy rectangular hull. The green deck is equipped with various equipment, including large black rubber fenders along the waterline, which may be used for collision protection. The tugboat's superstructure includes a bridge with windows, radar equipment, and a red and white antenna mast. The bridge is operated by a crew member, but he is not visible in the photo. The water is calm, with gentle ripples indicating movement. There is no sky in the image, and the focus is entirely on the ship and its surroundings."
    #
    # # 加载本地图像地址
    # image_paths = "E:/2025-09-08/5.2/Class/2-1_R8A4_LoRA_v0.1"
    # # 设置图像文件所在的目录路径
    #
    # # 输出的Excel文件名
    # output_filename = "E:/2025-09-08/5.2/Class/2-1_R8A4.xlsx"
    # # "类型"
    # file_type = 1

    # 检查文件夹是否存在
    if not os.path.exists(image_paths):
        print(f"Error: {image_paths} does not exist!")
        return

    # 支持的图像格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')

    img_list = list()
    filename_globle = list()
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(image_paths):
        # 检查文件是否为图像
        if filename.lower().endswith(supported_formats):
            filename_globle.append(filename)
            img_list.append(os.path.join(image_paths, filename))

    # 收集结果
    Results = []
    index = 0
    for filename in os.listdir(image_paths):

        # 加载图像
        image_origin = Image.open(os.path.join(image_paths, filename))
        # 转化图像为RGB
        image = convert_rgba_to_rgb(image=image_origin)

        # 计算分数
        score = hpsv2.score(image, prompt, hps_version="v2.1")
        index += 1
        Results.append([index,file_type,filename,f"{float(score[0]):.4f}"])

    # 以评分内容为依据进行排序
    # Results.sort(key=lambda x: x[2], reverse=True)
    # for index in range(len(Results)):
    #     Results[index][0] = index + 1 # 添加名次索引
    # 打印结果
    Total_Score = 0
    for result in Results:
        print(f"ranking = [{result[0]}, {result[1]}, {result[2]},{result[3]}]")
        Total_Score += float(result[3])
    print(f"Ave_Score = {Total_Score/len(Results)}")

    """
        将HPSv2得分列表转换为指定格式的Excel文件
         
        参数:
        data_list: 原始数据列表，格式为[(序号, 文件名, HPSv2得分), ...]
        output_filename: 输出的Excel文件名
        file_type: 要添加到"类型"列的手动指定内容
        """

    # 创建DataFrame并添加新列
    df = pd.DataFrame(Results, columns=['序号', '类型', '文件名', 'HPSv2得分'])

    # 保存为Excel文件
    df.to_excel(output_filename, index=False)
    print(f"文件已保存为: {output_filename}")



def main():

    # 加载本地图像地址
    # 设置图像文件所在的目录路径
    image_paths = [
        "E:/2025-09-08/5.2/Class/2-1_R8A4_LoRA_v0.1",
        "E:/2025-09-08/5.2/Class/2-2_R16A8_LoRA_v0.2",
        "E:/2025-09-08/5.2/Class/2-3_R32A16_LoRA_v0.3",
        "E:/2025-09-08/5.2/Class/2-4_R64A32_LoRA_v0.4",
        "E:/2025-09-08/5.2/Class/2-5_R128A64_LoRA_v0.5",
    ]

    # 输出的Excel文件名
    output_filenames = [
        "E:/2025-09-08/5.2/Class/2-1_HPSv2_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-2_HPSv2_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-3_HPSv2_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-4_HPSv2_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-5_HPSv2_Score.xlsx",
    ]

    # "类型"
    file_types = [1,2,3,4,5]

    for index in range(len(image_paths)):
        evaluate_images_with_hpsv2(image_paths[index], output_filenames[index],file_types[index])


if __name__ == "__main__":
    main()