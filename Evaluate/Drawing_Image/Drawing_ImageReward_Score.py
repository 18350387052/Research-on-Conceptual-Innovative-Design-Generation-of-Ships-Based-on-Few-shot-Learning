import os
import torch
import ImageReward as RM  # 导入ImageReward库，用于评估图像-文本匹配度
import pandas as pd



def evaluate_images_with_ImageReward(image_paths: str,output_filename: str,file_type: int):
    # 定义文本提示词，描述了期望生成的图像内容
    prompt = "This is a high-resolution photo of a tugboat sailing across calm turquoise waters. The vessel is predominantly white with green and red accents, and has a sturdy rectangular hull. The green deck is equipped with various equipment, including large black rubber fenders along the waterline, which may be used for collision protection. The tugboat's superstructure includes a bridge with windows, radar equipment, and a red and white antenna mast. The bridge is operated by a crew member, but he is not visible in the photo. The water is calm, with gentle ripples indicating movement. There is no sky in the image, and the focus is entirely on the ship and its surroundings."

    # 设置图像文件所在的目录路径
    img_prefix_dir = "E:/2025-09-08/5.2/Class/2-1_R8A4_LoRA_v0.1"

    # 检查文件夹是否存在
    if not os.path.exists(img_prefix_dir):
        print(f"Error: {img_prefix_dir} does not exist!")
        return


    # 支持的图像格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')

    img_list = list()
    filename_globle = list()
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(img_prefix_dir):
        # 检查文件是否为图像
        if filename.lower().endswith(supported_formats):
            filename_globle.append(filename)
            img_list.append(os.path.join(img_prefix_dir, filename))


    # 加载预训练的ImageReward模型（v1.0版本）
    model = RM.load("ImageReward-v1.0")

    # 使用torch.no_grad()禁用梯度计算，提高推理速度并节省内存
    with torch.no_grad():
        # 对所有图像进行排序和打分
        # ranking: 图像质量排名（从好到差的索引列表）
        # rewards: 每张图像对应的奖励分数列表
        ranking, rewards = model.inference_rank(prompt, img_list)

        # 打印评估结果
        print("\nPreference predictions:\n")
        print(f"ranking = {ranking}")  # 输出排名结果
        print(f"rewards = {rewards}")  # 输出奖励分数

        # 遍历每张图像，单独计算并显示其分数
        Score = list()
        for index in range(len(img_list)):
            # 计算单张图像与提示词的匹配分数
            score = model.score(prompt, img_list[index])
            # 格式化输出：图像文件名右对齐16个字符，分数保留2位小数
            # print(f"{filename_globle[index]:>16s}: {score:.4f}")
            Score.append([ranking[index],file_type,filename_globle[index],f"{score:.4f}"])


        # 按照每个内容的第0个位置进行排序 正序
        Score.sort(key=lambda x:x[0], reverse=False)
        Total_Score = 0
        for score in Score:
            print(f"ranking = {score}")
            Total_Score += float(score[3])
        print(f"Ave_Score = {Total_Score / len(Score)}")

        """
                将ImageReward得分列表转换为指定格式的Excel文件

                参数:
                data_list: 原始数据列表，格式为[(序号, 文件名, HPSv2得分), ...]
                output_filename: 输出的Excel文件名
                file_type: 要添加到"类型"列的手动指定内容
                """

        # 创建DataFrame并添加新列
        df = pd.DataFrame(Score, columns=['序号', '类型', '文件名', 'ImageReward得分'])

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
        "E:/2025-09-08/5.2/Class/2-1_ImageReward_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-2_ImageReward_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-3_ImageReward_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-4_ImageReward_Score.xlsx",
        "E:/2025-09-08/5.2/Class/2-5_ImageReward_Score.xlsx",
    ]

    # "类型"
    file_types = [1, 2, 3, 4, 5]

    for index in range(len(image_paths)):
        evaluate_images_with_ImageReward(image_paths[index], output_filenames[index], file_types[index])

if __name__ == "__main__":
    main()