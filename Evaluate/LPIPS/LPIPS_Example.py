import torch
from torchvision import transforms
from lpips import LPIPS
from PIL import Image

# 生成图像与真实图像的相似度
# 不同任务的LPIPS参考标准
# 1. 图像压缩
# python# 图像压缩质量评估
def evaluate_compression_quality(lpips_score):
    if lpips_score < 0.05:
        return "高质量压缩"
    elif lpips_score < 0.1:
        return "良好压缩"
    elif lpips_score < 0.2:
        return "可接受压缩"
    else:
        return "压缩质量较差"
# 2. 图像超分辨率
# python# 超分辨率重建质量
def evaluate_sr_quality(lpips_score):
    if lpips_score < 0.08:
        return "优秀重建"
    elif lpips_score < 0.15:
        return "良好重建"
    elif lpips_score < 0.25:
        return "一般重建"
    else:
        return "重建质量差"
# 3. 图像生成（GAN/扩散模型）
# python# 生成图像与真实图像的相似度
def evaluate_generation_quality(lpips_score):
    if lpips_score < 0.1:
        return "生成质量极高"
    elif lpips_score < 0.2:
        return "生成质量良好"
    elif lpips_score < 0.3:
        return "生成质量一般"
    else:
        return "生成质量较差"
# 4. 图像编辑/风格迁移
# python# 编辑后与原图的差异评估
def evaluate_editing_degree(lpips_score):
    if lpips_score < 0.1:
        return "轻微编辑"
    elif lpips_score < 0.2:
        return "中度编辑"
    elif lpips_score < 0.4:
        return "显著编辑"
    else:
        return "完全改变"

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

def main():
    # 初始化LPIPS模型
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    loss_fn_alex = LPIPS(net='alex').to(device)  # 使用AlexNet作为特征提取器
    # loss_fn_vgg = LPIPS(net='vgg').to(device) # 使用VGG作为特征提取器

    # 图像预处理
    preprocess = transforms.Compose([
        transforms.Resize((400, 600)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 准备输入图像
    image_path01 = "D:/ProgramData/Experiment/resource/Tugboat_real1-025.png"
    image_path02 = "D:/ProgramData/Experiment/resource/Tugboat_real1-026.png"


    image1 = preprocess(Image.open(image_path01)).unsqueeze(0).to(device)
    image2 = preprocess(Image.open(image_path02)).unsqueeze(0).to(device)

    # 计算LPIPS得分
    with torch.no_grad():
        dist = loss_fn_alex(image1, image2)

    # 输出结果
    print('LPIPS score:\n', dist.item())

if __name__ == '__main__':
    main()