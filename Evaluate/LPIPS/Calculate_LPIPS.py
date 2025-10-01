import os

import torch
import lpips
from PIL import Image
import torchvision.transforms as transforms
import numpy as np

def interpret_lpips_score(lpips_value):
    """
    解释LPIPS分数
    """
    if lpips_value < 0.01:
        return "几乎完全相同"
    elif lpips_value < 0.05:
        return "非常相似，差异很小"
    elif lpips_value < 0.1:
        return "相似，有轻微差异"
    elif lpips_value < 0.2:
        return "有明显差异"
    elif lpips_value < 0.5:
        return "差异较大"
    else:
        return "差异很大，几乎完全不同"

class LPIPSEvaluator:
    def __init__(self, net='alex', device=None):
        """
        初始化LPIPS评估器

        Args:
            net: 网络类型 ('alex', 'vgg', 'squeeze')
            device: 计算设备
        """
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loss_fn = lpips.LPIPS(net=net).to(self.device)

        # 定义预处理 图像预处理
        self.transform = transforms.Compose([
            transforms.Resize((400, 600)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])


    def preprocess_image(self, image_path):
        """
        预处理图像，确保是RGB格式

        Args:
            image_path: 图像路径或PIL Image对象

        Returns:
            预处理后的tensor
        """
        # 加载图像
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = image_path

        # 处理RGBA图像
        if image.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', image.size, (255, 255, 255))
            # 使用alpha通道作为mask进行粘贴
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # 转换为tensor
        img_tensor = self.transform(image)

        # LPIPS需要归一化到[-1, 1]
        img_tensor = 2 * img_tensor - 1

        # 添加batch维度
        img_tensor = img_tensor.unsqueeze(0).to(self.device)

        return img_tensor

    def calculate_lpips(self, img1_path, img2_path):
        """
        计算两张图像的LPIPS距离

        Args:
            img1_path: 第一张图像路径
            img2_path: 第二张图像路径

        Returns:
            LPIPS距离值
        """
        # 预处理图像
        img1_tensor = self.preprocess_image(img1_path)
        img2_tensor = self.preprocess_image(img2_path)

        # 计算LPIPS
        with torch.no_grad():
            distance = self.loss_fn(img1_tensor, img2_tensor)

        return distance.item()

def main():
    # 使用示例

    evaluator = LPIPSEvaluator(net='alex')
    # distance = evaluator.calculate_lpips(image_path01, image_path02)
    # print(f"LPIPS距离: {distance:.4f}")

    # 比较目标的原图像
    image_origin = "E:/2025-09-08/5.3/3-1_Fullmodel/Fullmodel-generate-0043.png"

    # 加载本地图像地址
    image_paths = "E:/2025-09-08/5.3/3-7_LowResolute/"
    # 设置图像文件所在的目录路径


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

    resule_score = list()
    for index in range(len(img_list)):
        # 分别与第0张进行比较 计算感知相似度得分
        distance = evaluator.calculate_lpips(image_origin, img_list[index])
        resule_score.append([0,filename_globle[index], distance,interpret_lpips_score(distance)])

    Score = 0
    resule_score = sorted(resule_score, key=lambda x: x[2], reverse=False)
    for index in range(len(resule_score)):
        resule_score[index][0] = index + 1
        Score += resule_score[index][2]

    for result in resule_score:
        print(f"rank =  {result}")
    Ave_Score = Score / len(resule_score)
    print(f"Ave_Score = {Ave_Score}")

if __name__ == '__main__':
    main()