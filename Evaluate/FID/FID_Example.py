import os
import subprocess


def calculate_fid_small_dataset(real_path, generated_path, dims=192):
    """
    针对小样本数据集的FID计算
    使用较低维度的特征，更适合小数据集

    Args:
        real_path: 真实图像文件夹路径
        generated_path: 生成图像文件夹路径
        dims: 特征维度
              - 64: 第一个最大池化层特征（最适合极小数据集）少于100张图
              - 192: 第二个最大池化层特征（推荐小数据集使用）100-500张图
              - 768: 预辅助分类器特征 500-2000
              - 2048: 标准最终池化特征（需要大数据集） 2000张以上

    Returns:
        FID分数
    """
    cmd = [
        'python', '-m', 'pytorch_fid',
        real_path,
        generated_path,
        '--dims', str(dims),
        '--device', 'cuda:0'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if "FID:" in result.stdout:
        fid_score = float(result.stdout.split("FID:  ")[0])
        return fid_score
    else:
        print("Error:", result.stderr)
        return None


def main():
    """完整的FID计算流程"""

    # 设置路径
    real_images_path = "D:/ProgramData/Experiment/resource"
    generated_images_path = "D:/ProgramData/Experiment/result"

    # 检查文件夹是否存在
    if not os.path.exists(real_images_path):
        print(f"Error: {real_images_path} does not exist!")
        return

    if not os.path.exists(generated_images_path):
        print(f"Error: {generated_images_path} does not exist!")
        return

    # 统计图像数量
    real_count = len([f for f in os.listdir(real_images_path)
                      if f.endswith(('.png', '.jpg', '.jpeg'))])
    gen_count = len([f for f in os.listdir(generated_images_path)
                     if f.endswith(('.png', '.jpg', '.jpeg'))])

    print(f"Real images: {real_count}")
    print(f"Generated images: {gen_count}")

    # 根据数据量选择合适的维度
    if min(real_count, gen_count) < 100:
        dims = 64
        print("Using dims=64 for very small dataset")
    elif min(real_count, gen_count) < 500:
        dims = 192
        print("Using dims=192 for small dataset")
    else:
        dims = 768
        print("Using dims=768 for medium dataset")

    # 计算FID
    print("\nCalculating FID score...")
    fid_score = calculate_fid_small_dataset(
        real_images_path,
        generated_images_path,
        dims=dims
    )

    if fid_score is not None:
        print(f"\n✓ FID Score: {fid_score}")
        # print(f"  (Lower is better, 0 = identical)")
    else:
        print("\n✗ Failed to calculate FID score")

# 如果直接运行此脚本
if __name__ == "__main__":
    main()