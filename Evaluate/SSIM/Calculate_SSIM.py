import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def interpret_ssim_score(score):
    """
    解释SSIM分数的含义

    参数:
    score: SSIM分数

    返回:
    interpretation: 对分数的文字解释
    """
    if score >= 0.9:
        return "非常相似 - 图像几乎相同"
    elif score >= 0.7:
        return "高度相似 - 图像内容基本一致"
    elif score >= 0.5:
        return "中等相似 - 图像有共同特征但存在明显差异"
    elif score >= 0.3:
        return "低度相似 - 图像略有相似之处"
    elif score >= 0:
        return "几乎不相似 - 图像差异很大"
    else:
        return "负相关 - 图像可能呈现相反特性"

def calculate_ssim_for_images(original_image_path, generated_images_dir):
    """
    计算原图与生成图像集中各图像的SSIM分数

    参数:
    original_image_path: 原始图像路径
    generated_images_dir: 生成的图像所在的目录路径

    返回:
    无，结果直接打印到控制台
    """
    # 读取原始图像
    if not os.path.exists(original_image_path):
        print(f"错误：原始图像文件不存在 '{original_image_path}'")
        return

    original_img = cv2.imread(original_image_path)
    if original_img is None:
        print(f"错误：无法读取原始图像 '{original_image_path}'")
        return

    # 转换为灰度图
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # 获取生成图像目录中的所有图像文件
    if not os.path.isdir(generated_images_dir):
        print(f"错误：生成图像目录不存在 '{generated_images_dir}'")
        return

    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    generated_images = [f for f in os.listdir(generated_images_dir)
                        if f.lower().endswith(image_extensions)]

    if not generated_images:
        print(f"错误：在目录中未找到图像文件 '{generated_images_dir}'")
        return

    print(f"找到 {len(generated_images)} 张生成图像")
    print("\nSSIM评分结果:")
    print("-" * 50)

    ssim_scores = []

    # 计算每张生成图像与原图的SSIM
    for img_file in generated_images:
        img_path = os.path.join(generated_images_dir, img_file)
        gen_img = cv2.imread(img_path)

        if gen_img is None:
            print(f"警告：无法读取图像 '{img_file}'，跳过")
            continue

        # 确保生成图像尺寸与原图一致
        if gen_img.shape != original_img.shape:
            gen_img = cv2.resize(gen_img, (original_img.shape[1], original_img.shape[0]))

        # 转换为灰度图
        gen_gray = cv2.cvtColor(gen_img, cv2.COLOR_BGR2GRAY)

        # 计算SSIM
        ssim_score = ssim(original_gray, gen_gray)
        ssim_scores.append([0,img_file,float(ssim_score)])

        # print(f"{img_file}: {ssim_score:.4f}")


    ssim_scores.sort(key=lambda x: x[2], reverse=True)
    Total_score = 0
    for index in range(len(ssim_scores)):
        ssim_scores[index][0] = index + 1
        Total_score += ssim_scores[index][2]

    for ssim_score in ssim_scores:
        print(f"{ssim_score}")
    Average_score = Total_score / len(ssim_scores)
    print(f"Average_score = {Average_score} ")

    print(f'{interpret_ssim_score(Average_score)} ')


# 使用示例
if __name__ == "__main__":
    # 请替换为你的实际文件路径
    original_img_path = "E:/2025-09-08/5.3/3-5_Fullmodel/Fullmodel-generate-0123.png"  # 原始图像路径

    generated_img_dir = "E:/2025-09-08/5.3/3-2_Ourmodel/"  # 生成图像所在目录

    calculate_ssim_for_images(original_img_path, generated_img_dir)