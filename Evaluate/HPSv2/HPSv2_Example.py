import torch
from PIL import Image
import numpy as np
from torchvision import transforms
import os
from typing import List, Union
import hpsv2  # 确保已安装HPSv2


class HPSv2Evaluator:
    def __init__(self, device=None):
        """
        初始化HPSv2评估器

        Args:
            device: 计算设备，默认自动选择
        """
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()

        # CLIP预处理参数
        self.mean = [0.48145466, 0.4578275, 0.40821073]
        self.std = [0.26862954, 0.26130258, 0.27577711]
        self.target_size = 224

    def _load_model(self):
        """加载HPSv2模型"""
        try:
            model = hpsv2.load_model().to(self.device)
            model.eval()
            return model
        except Exception as e:
            print(f"加载HPSv2模型失败: {e}")
            raise

    def preprocess_image(self, image: Union[Image.Image, np.ndarray, torch.Tensor]) -> torch.Tensor:
        """
        预处理单张图像

        Args:
            image: PIL Image、numpy array或torch tensor

        Returns:
            预处理后的tensor [1, 3, 224, 224]
        """
        # 转换为PIL Image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        elif isinstance(image, torch.Tensor):
            if image.dim() == 4:  # batch dimension
                image = image.squeeze(0)
            if image.shape[0] == 3 or image.shape[0] == 4:  # CHW format
                image = image.permute(1, 2, 0)
            image = image.cpu().numpy()
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        # 处理RGBA图像
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # 应用预处理变换
        preprocess = transforms.Compose([
            transforms.Resize((self.target_size, self.target_size),
                              interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean, std=self.std)
        ])

        image_tensor = preprocess(image)
        return image_tensor.unsqueeze(0)  # 添加batch维度

    def evaluate_single(self, image: Union[str, Image.Image, np.ndarray, torch.Tensor]) -> float:
        """
        评估单张图像

        Args:
            image: 图像路径、PIL Image、numpy array或torch tensor

        Returns:
            HPSv2分数
        """
        # 如果是路径，加载图像
        if isinstance(image, str):
            image = Image.open(image)

        # 预处理
        image_tensor = self.preprocess_image(image).to(self.device)

        # 计算分数
        with torch.no_grad():
            score = self.model(image_tensor)

        return score.item()

    def evaluate_batch(self, images: List[Union[str, Image.Image, np.ndarray, torch.Tensor]],
                       batch_size: int = 32) -> List[float]:
        """
        批量评估图像

        Args:
            images: 图像列表
            batch_size: 批处理大小

        Returns:
            分数列表
        """
        scores = []

        for i in range(0, len(images), batch_size):
            batch_images = images[i:i + batch_size]
            batch_tensors = []

            for img in batch_images:
                try:
                    if isinstance(img, str):
                        img = Image.open(img)
                    tensor = self.preprocess_image(img)
                    batch_tensors.append(tensor)
                except Exception as e:
                    print(f"处理图像失败: {e}")
                    scores.append(float('nan'))
                    continue

            if batch_tensors:
                # 合并batch
                batch_tensor = torch.cat(batch_tensors, dim=0).to(self.device)

                # 批量推理
                with torch.no_grad():
                    batch_scores = self.model(batch_tensor)

                scores.extend(batch_scores.cpu().numpy().tolist())

        return scores


# 使用示例
def main():
    # 初始化评估器
    evaluator = HPSv2Evaluator()

    # 评估单张图像
    image_path = "generated_image.png"
    score = evaluator.evaluate_single(image_path)
    print(f"单张图像分数: {score}")

    # 批量评估
    image_paths = ["image1.png", "image2.png", "image3.png"]
    scores = evaluator.evaluate_batch(image_paths)
    print(f"批量评估分数: {scores}")
    print(f"平均分数: {np.mean(scores):.4f}")

    # 直接评估numpy数组（例如从扩散模型生成的）
    # generated_image = diffusion_model.generate(...)  # 假设这是您的生成图像
    # score = evaluator.evaluate_single(generated_image)


if __name__ == "__main__":
    main()