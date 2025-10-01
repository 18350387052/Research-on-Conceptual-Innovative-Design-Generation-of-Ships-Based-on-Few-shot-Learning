import os
import torch
import ImageReward as RM  # 导入ImageReward库，用于评估图像-文本匹配度

# 配置代理服务器信息
proxies = {
    "http": "http://127.0.0.1:7897",  # 替换为你的本地代理地址和端口
    "https": "http://127.0.0.1:7897"   # 替换为你的本地代理地址和端口
}

def main():
    # 定义文本提示词，描述了期望生成的图像内容
    prompt = "This is a high-resolution photo of a tugboat sailing across calm turquoise waters. The vessel is predominantly white with green and red accents, and has a sturdy rectangular hull. The green deck is equipped with various equipment, including large black rubber fenders along the waterline, which may be used for collision protection. The tugboat's superstructure includes a bridge with windows, radar equipment, and a red and white antenna mast. The bridge is operated by a crew member, but he is not visible in the photo. The water is calm, with gentle ripples indicating movement. There is no sky in the image, and the focus is entirely on the ship and its surroundings."

    # 设置图像文件所在的目录路径
    img_prefix_dir = "E:/2025-09-08/5.3/3-1_Basemodel/"

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
            Score.append([ranking[index],filename_globle[index],f"{score:.4f}"])


        # 按照每个内容的第0个位置进行排序 正序
        Score.sort(key=lambda x:x[0], reverse=False)
        Total_Score = 0
        for score in Score:
            print(f"ranking = {score}")
            Total_Score += float(score[2])
        print(f"Ave_Score = {Total_Score / len(Score)}")

if __name__ == "__main__":
    main()