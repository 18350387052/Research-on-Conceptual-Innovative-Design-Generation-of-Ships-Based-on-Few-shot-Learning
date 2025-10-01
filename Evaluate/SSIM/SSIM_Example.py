import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np


def calculate_ssim(image1_path, image2_path):
    """
    计算两幅图像之间的结构相似性指数 (SSIM)

    参数:
    image1_path: 第一幅图像的路径
    image2_path: 第二幅图像的路径

    返回:
    ssim_score: 两幅图像的SSIM分数，范围[-1, 1]，值越大表示越相似
    """
    # 读取图像
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 检查图像是否成功加载
    if image1 is None:
        raise FileNotFoundError(f"图像文件未找到: {image1_path}")
    if image2 is None:
        raise FileNotFoundError(f"图像文件未找到: {image2_path}")

    # 确保图像尺寸相同
    if image1.shape != image2.shape:
        # 调整图像2的尺寸以匹配图像1
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        print("警告: 图像尺寸不一致，已调整第二幅图像的尺寸以匹配第一幅图像")

    # 转换为灰度图像
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性 (SSIM)
    ssim_score, diff = ssim(gray1, gray2, full=True)

    return ssim_score, diff


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


# 使用示例
if __name__ == "__main__":
    # 图像路径 - 请替换为你自己的图像路径
    image1_path = "E:/2025-09-08/5.3/3-1_Fullmodel/Fullmodel-generate-0123.png"

    image2_path = "E:/2025-09-08/5.3/3-7_LowResolute/LowResolute-generate-0002.png"

    try:
        # 计算SSIM
        ssim_score, diff_map = calculate_ssim(image1_path, image2_path)

        # 输出结果
        print(f"SSIM分数: {ssim_score:.4f}")
        print(f"相似度解释: {interpret_ssim_score(ssim_score)}")

        # 可视化差异图（可选）
        # 将差异图转换为0-255范围以便显示
        diff_visual = (diff_map * 255).astype("uint8")

        # 显示图像和差异图
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)



    except Exception as e:
        print(f"计算过程中发生错误: {e}")