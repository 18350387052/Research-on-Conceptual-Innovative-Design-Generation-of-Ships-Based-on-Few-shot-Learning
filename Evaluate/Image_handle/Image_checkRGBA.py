#!/usr/bin/env python3
"""
简化版RGBA格式图像检查器
扫描指定目录下的图像文件，找出RGBA格式的文件
"""

import os
from PIL import Image
from pathlib import Path


def check_rgba_images(directory_path):
    """
    扫描目录中的图像文件，检查并统计RGBA格式

    参数:
        directory_path: 要扫描的目录路径
    """
    # 支持的图像格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'}

    # 结果存储
    rgba_files = []
    format_stats = {}
    errors = []

    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"错误: 目录 '{directory_path}' 不存在")
        return

    if not os.path.isdir(directory_path):
        print(f"错误: '{directory_path}' 不是一个目录")
        return

    print(f"正在扫描目录: {os.path.abspath(directory_path)}")
    print("=" * 60)

    # 获取目录中的所有文件
    files = os.listdir(directory_path)
    total_images = 0

    # 检查每个文件
    for filename in files:
        file_path = os.path.join(directory_path, filename)

        # 跳过子目录
        if os.path.isdir(file_path):
            continue

        # 检查是否为图像文件
        if Path(file_path).suffix.lower() in image_extensions:
            total_images += 1

            try:
                # 打开图像并检查格式
                with Image.open(file_path) as img:
                    mode = img.mode

                    # 统计格式
                    if mode not in format_stats:
                        format_stats[mode] = []
                    format_stats[mode].append(filename)

                    # 如果是RGBA格式，添加到列表
                    if mode == 'RGBA':
                        rgba_files.append(filename)

            except Exception as e:
                errors.append((filename, str(e)))

    # 打印结果
    print(f"\n扫描完成！共发现 {total_images} 个图像文件\n")

    # RGBA文件列表
    print(f"【RGBA格式文件】 共 {len(rgba_files)} 个:")

    print("-" * 40)
    if rgba_files:
        for file in rgba_files:
            print(f"  ✓ {file}")
    else:
        print("  没有找到RGBA格式的文件")

    # 格式统计
    print(f"\n【所有格式统计】:")
    print("-" * 40)
    for mode, files in sorted(format_stats.items()):
        print(f"  {mode:8s} : {len(files):3d} 个文件")

    # 错误信息
    if errors:
        print(f"\n【无法读取的文件】 共 {len(errors)} 个:")
        print("-" * 40)
        for file, error in errors:
            print(f"  ✗ {file}")
            print(f"    原因: {error}")

    print("\n" + "=" * 60)
    return rgba_files


# 主程序
if __name__ == "__main__":
    # ========== 配置扫描路径 ==========
    # 在这里修改你要扫描的目录路径
    scan_directory = "D:/ProgramData/Experiment/resource"  # 当前目录，可以修改为你的图片目录路径
    # scan_directory = "/path/to/your/images"  # 例如
    # scan_directory = "D:/Pictures"  # Windows路径示例
    # scan_directory = "/Users/username/Pictures"  # Mac路径示例

    # 执行扫描
    rgba_files = check_rgba_images(scan_directory)

    # 可以在这里对返回的RGBA文件列表做进一步处理
    if rgba_files:
        print(f"提示: 发现 {len(rgba_files)} 个RGBA文件需要转换")