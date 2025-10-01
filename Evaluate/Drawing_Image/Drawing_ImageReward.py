import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 彻底解决中文显示问题 - 方法一：全局设置字体
plt.rcParams['font.family'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 使用支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


def read_and_process_data(file_paths, comprehensive_file_path=None):
    """
    读取多个Excel文件并合并为一个DataFrame，可选读取综合得分文件

    Parameters:
    file_paths (list): 本地Excel文件路径列表
    comprehensive_file_path (str): 综合得分Excel文件路径（可选）

    Returns:
    pd.DataFrame: 合并后的数据
    pd.DataFrame: 综合得分数据（如果提供了路径）
    """
    # 读取所有Excel文件
    dfs = [pd.read_excel(file) for file in file_paths]
    # 合并数据
    combined_df = pd.concat(dfs, ignore_index=True)

    # 如果提供了综合得分文件路径，读取它
    comprehensive_df = None
    if comprehensive_file_path:
        comprehensive_df = pd.read_excel(comprehensive_file_path)

    return combined_df, comprehensive_df


def calculate_mean_scores(df, comprehensive_df=None):
    """
    按类型分组计算每种得分的平均值

    Parameters:
    df (pd.DataFrame): 合并后的数据
    comprehensive_df (pd.DataFrame): 综合得分数据（可选）

    Returns:
    pd.DataFrame: 包含分组平均值的DataFrame
    pd.Series: 综合得分的平均值（如果提供了数据）
    """
    # 原有得分列
    score_columns = ['FID得分', 'HPSv2得分', 'ImageReward得分']
    # 按类型分组并计算平均值
    grouped_means = df.groupby('类型')[score_columns].mean()

    # 如果有综合得分数据，也计算其平均值
    comprehensive_means = None
    if comprehensive_df is not None:
        comprehensive_means = comprehensive_df.groupby('类型')['综合得分'].mean()

    return grouped_means, comprehensive_means


def create_custom_bar_line_chart(means, comprehensive_means, hex_colors, line_color,
                                 x_labels, legend_labels, line_legend_label, y_range=None):
    """
    创建自定义柱状图和折线图的组合

    Parameters:
    means (pd.DataFrame): 包含平均值的DataFrame
    comprehensive_means (pd.Series): 综合得分平均值
    hex_colors (list): 三种得分的HEX颜色代码列表
    line_color (str): 折线图的HEX颜色代码
    x_labels (list): 横轴标签列表
    legend_labels (list): 柱状图图例标签列表
    line_legend_label (str): 折线图图例标签
    y_range (tuple): 纵轴范围(可选)
    """
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=(12, 8))

    # 设置每组柱子的位置和宽度
    n_types = len(means.index)  # 类型数量
    n_scores = len(means.columns)  # 得分种类数量
    total_width = 0.8  # 每组柱子的总宽度
    bar_width = total_width / n_scores  # 单个柱子的宽度

    # 生成每组柱子的x轴位置
    x_pos = np.arange(n_types)

    # 绘制每种得分的柱子
    for i, score_column in enumerate(means.columns):
        # 计算当前得分柱子的x坐标
        x_offset = i * bar_width - total_width / 2 + bar_width / 2
        bars = ax.bar(x_pos + x_offset,
                      means[score_column],
                      width=bar_width,
                      color=hex_colors[i],
                      label=legend_labels[i] if legend_labels else score_column,
                      alpha=0.8)  # 添加透明度以便更好地看到折线

    # 如果有综合得分，绘制折线图
    if comprehensive_means is not None:
        # 绘制折线
        line = ax.plot(x_pos, comprehensive_means.values,
                       color=line_color,
                       marker='o',
                       markersize=8,
                       linewidth=2.5,
                       label=line_legend_label,
                       zorder=10)  # 确保折线在柱状图上方

        # # 在每个数据点上显示数值（可选）
        # for i, value in enumerate(comprehensive_means.values):
        #     ax.text(x_pos[i], value, f'{value:.2f}',
        #             ha='center', va='bottom', fontsize=16, fontweight='bold')

    # 设置横轴标签
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels, fontsize=12)

    # 设置纵轴范围
    if y_range:
        ax.set_ylim(y_range)
    else:
        # 自动计算合适的纵轴范围
        all_values = [means.min().min(), means.max().max()]
        if comprehensive_means is not None:
            all_values.extend([comprehensive_means.min(), comprehensive_means.max()])
        data_min = min(all_values)
        data_max = max(all_values)
        margin = (data_max - data_min) * 0.15  # 增加15%的边距
        ax.set_ylim(max(0, data_min - margin), data_max + margin)

    # 添加标签和标题（可选）
    # ax.set_xlabel('参数配置', fontsize=14)
    # ax.set_ylabel('平均得分', fontsize=14)
    # ax.set_title('不同参数配置下的得分比较', fontsize=16)

    # 添加图例 - 增加字体大小设置
    ax.legend(fontsize=13, loc='best', framealpha=0.9)

    # 添加网格线以便于阅读
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    # 优化布局
    plt.tight_layout()

    # 保存 & 显示
    plt.savefig('Compare_EvaluateScore_with_Comprehensive-1.png', dpi=300)
    print(f"已生成图片：Compare_EvaluateScore_with_Comprehensive-1.png")

    # 显示图形
    plt.show()


def main():
    # 1. 定义文件路径（请根据实际文件路径修改）
    file_paths = [
        'E:/2025-09-08/5.2/Class/Done/2-0_FID_Score.xlsx',
        'E:/2025-09-08/5.2/Class/Done/2-1_HPSv2_Score.xlsx',
        'E:/2025-09-08/5.2/Class/Done/2-1_ImageReward_Score.xlsx'
    ]

    # 综合得分文件路径（请根据实际路径修改）
    comprehensive_file_path = 'E:/2025-09-08/5.2/Class/Done/2-2_Comprehensive_Score.xlsx'

    try:
        # 2. 读取和处理数据
        combined_data, comprehensive_data = read_and_process_data(file_paths, comprehensive_file_path)

        # 3. 计算分组平均值
        means, comprehensive_means = calculate_mean_scores(combined_data, comprehensive_data)
        print("计算得到的平均值:")
        print(means)
        if comprehensive_means is not None:
            print("\n综合得分平均值:")
            print(comprehensive_means)

        # 4. 自定义图表参数
        # 柱状图HEX颜色代码（请根据喜好修改）
        custom_colors = [
            # '#C3E2EC',  # 浅蓝色
            # '#BDEDC5',  # 浅绿色
            # '#F7C4C1'  # 浅粉色
            '#D87659',  # 浅蓝色
            '#E9C46A',  # 浅绿色
            '#299D8F'  # 浅粉色
        ]

        # 折线图颜色（请根据喜好修改）
        line_color = '#FF6B6B'  # 珊瑚红色

        # 横轴标签（请根据实际类型名称修改）
        custom_x_labels = [
            'r=8,α=4',
            'r=16,α=8',
            'r=32,α=16',
            'r=64,α=32',
            'r=128,α=64'
        ]

        # 柱状图图例标签（请根据实际得分含义修改）
        custom_legend = [
            'FID(1/10)',
            'HPSv2(5x)',
            'ImageReward(1.5x)'
        ]

        # 折线图图例标签
        line_legend_label = 'Weighted Ave_score(3x)'

        # 纵轴范围（可选，如不指定则自动计算）
        # custom_y_range = (0, 100)  # 示例范围

        # 5. 创建柱状图和折线图组合
        create_custom_bar_line_chart(means, comprehensive_means, custom_colors, line_color,
                                     custom_x_labels, custom_legend, line_legend_label)

    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        print("提示：请确保所有文件路径正确，包括综合得分文件")
    except KeyError as e:
        print(f"数据列名错误: {e}")
        print("提示：请确保Excel文件中包含'类型'和'综合得分'列")
    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()