#!/usr/bin/env python3
"""
简化版RGBA转RGB图像格式转换器
将指定目录中的RGBA格式图像转换为RGB格式
"""

import os
from PIL import Image
from pathlib import Path
from datetime import datetime


def convert_rgba_to_rgb(file_path, background_color=(255, 255, 255), quality=95):
    """
    将单个RGBA图像转换为RGB格式

    参数:
        file_path: 图像文件路径
        background_color: 背景颜色RGB值，用于替换透明通道
        quality: JPEG压缩质量(1-100)

    返回:
        (成功, 消息)
    """
    try:
        # 打开图像
        with Image.open(file_path) as img:
            # 检查是否为RGBA格式
            if img.mode != 'RGBA':
                return False, f"跳过 - 不是RGBA格式(当前: {img.mode})"

            # 创建备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = file_path.replace('.', f'_rgba_backup_{timestamp}.')

            # 备份原文件
            img.save(backup_path)

            # 创建RGB图像
            rgb_img = Image.new('RGB', img.size, background_color)

            # 使用alpha通道作为蒙版粘贴图像
            rgb_img.paste(img, mask=img.split()[3])

            # 保存转换后的图像（覆盖原文件）
            save_kwargs = {}
            if Path(file_path).suffix.lower() in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True

            rgb_img.save(file_path, **save_kwargs)

            return True, f"成功转换 (备份: {os.path.basename(backup_path)})"

    except Exception as e:
        return False, f"转换失败: {str(e)}"


def batch_convert_rgba(directory_path, background_color=(255, 255, 255), quality=95):
    """
    批量转换目录中的RGBA图像为RGB格式

    参数:
        directory_path: 目录路径
        background_color: 背景颜色RGB值
        quality: JPEG压缩质量
    """
    # 支持的图像格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp'}

    # 检查目录
    if not os.path.exists(directory_path):
        print(f"错误: 目录 '{directory_path}' 不存在")
        return

    if not os.path.isdir(directory_path):
        print(f"错误: '{directory_path}' 不是一个目录")
        return

    print(f"正在转换目录: {os.path.abspath(directory_path)}")
    print(f"背景颜色: RGB{background_color}")
    print(f"JPEG质量: {quality}")
    print("=" * 60)

    # 统计变量
    success_count = 0
    skip_count = 0
    fail_count = 0
    success_files = []
    skip_files = []
    fail_files = []

    # 获取目录中的所有文件
    files = os.listdir(directory_path)

    # 筛选图像文件
    image_files = []
    for filename in files:
        file_path = os.path.join(directory_path, filename)

        # 跳过子目录
        if os.path.isdir(file_path):
            continue

        # 检查是否为图像文件
        if Path(file_path).suffix.lower() in image_extensions:
            image_files.append((filename, file_path))

    print(f"\n发现 {len(image_files)} 个图像文件\n")

    # 处理每个图像文件
    for filename, file_path in image_files:
        print(f"处理: {filename} ... ", end="")

        success, message = convert_rgba_to_rgb(file_path, background_color, quality)

        if success:
            print(f"✓ {message}")
            success_count += 1
            success_files.append(filename)
        elif "跳过" in message:
            print(f"- {message}")
            skip_count += 1
            skip_files.append((filename, message))
        else:
            print(f"✗ {message}")
            fail_count += 1
            fail_files.append((filename, message))

    # 打印汇总结果
    print("\n" + "=" * 60)
    print("【转换结果汇总】\n")

    print(f"✓ 成功转换: {success_count} 个文件")
    if success_files:
        for f in success_files:
            print(f"    - {f}")

    print(f"\n- 跳过(非RGBA): {skip_count} 个文件")
    if skip_files:
        for f, reason in skip_files:
            print(f"    - {f}")

    print(f"\n✗ 转换失败: {fail_count} 个文件")
    if fail_files:
        for f, error in fail_files:
            print(f"    - {f}: {error}")

    print("\n" + "=" * 60)
    print(f"总计: 处理 {len(image_files)} 个文件")
    print(f"      成功 {success_count} | 跳过 {skip_count} | 失败 {fail_count}")

    if success_count > 0:
        print(f"\n提示: 原始RGBA文件已备份为 *_rgba_backup_时间戳.* 格式")

    return success_count, skip_count, fail_count


# 主程序
if __name__ == "__main__":
    # ========== 配置参数 ==========
    # 1. 设置要转换的目录路径
    convert_directory = "D:/ProgramData/Experiment/resource"  # 当前目录，修改为你的图片目录
    # convert_directory = "/path/to/your/images"  # 例如
    # convert_directory = "D:/Pictures"  # Windows路径示例
    # convert_directory = "/Users/username/Pictures"  # Mac路径示例

    # 2. 设置背景颜色 (用于替换透明通道)
    # 常用颜色：
    # (255, 255, 255) = 白色（默认）
    # (0, 0, 0) = 黑色
    # (128, 128, 128) = 灰色
    background = (255, 255, 255)

    # 3. 设置JPEG压缩质量 (1-100, 越高质量越好但文件越大)
    jpeg_quality = 95

    # ========== 执行转换 ==========
    batch_convert_rgba(convert_directory, background, jpeg_quality)