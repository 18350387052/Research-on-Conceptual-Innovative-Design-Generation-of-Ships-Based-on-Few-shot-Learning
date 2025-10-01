from PIL import Image
import os


def horizontal_flip_image(input_path, output_path):
    """
    对图像进行水平翻转并保存

    参数:
    input_path: 原始图像路径
    output_path: 翻转后图像的保存路径
    """
    try:
        # 打开图像
        with Image.open(input_path) as img:
            # 进行水平翻转 (transpose(Image.FLIP_LEFT_RIGHT) 也可实现相同效果)
            flipped_img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

            # 保存翻转后的图像
            flipped_img.save(output_path)
            print(f"已成功生成翻转图像: {output_path}")
    except Exception as e:
        print(f"处理图像 {input_path} 时出错: {str(e)}")


def batch_flip_images(input_dir, output_dir):
    """
    批量处理文件夹中的所有图像，生成水平翻转版本

    参数:
    input_dir: 包含原始图像的文件夹路径
    output_dir: 保存翻转后图像的文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_dir, exist_ok=True)

    # 支持的图像格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_dir):
        # 检查文件是否为图像
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_dir, filename)

            # 生成输出文件名，在原文件名后添加"_flipped"标识
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_flipped{ext}"
            output_path = os.path.join(output_dir, output_filename)

            # 进行水平翻转
            horizontal_flip_image(input_path, output_path)


if __name__ == "__main__":
    # 配置路径
    # INPUT_DIRECTORY = "original_images"  # 原始图像所在文件夹
    # OUTPUT_DIRECTORY = "flipped_images"  # 翻转后图像保存文件夹




    INPUT_origin = "D:/ProgramData/Experiment/resource"
    INPUT_DIRECTORY = INPUT_origin
    OUTPUT_DIRECTORY = INPUT_origin + "flip/"
    # 执行批量翻转
    batch_flip_images(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    print(f"** 批量水平翻转处理完成!")


