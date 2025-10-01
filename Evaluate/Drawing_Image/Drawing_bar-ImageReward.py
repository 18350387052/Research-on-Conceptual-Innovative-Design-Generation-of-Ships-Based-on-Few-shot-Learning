import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 彻底解决中文显示问题 - 方法一：全局设置字体
plt.rcParams['font.family'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 使用支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


def read_and_process_data(file_paths):
    """
    读取多个Excel文件并合并为一个DataFrame

    Parameters:
    file_paths (list): 本地Excel文件路径列表

    Returns:
    pd.DataFrame: 合并后的数据
    """
    # 读取所有Excel文件
    dfs = [pd.read_excel(file) for file in file_paths]
    # 合并数据
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df


def read_comprehensive_score(file_path):
    """
    读取综合得分Excel文件

    Parameters:
    file_path (str): 综合得分文件路径

    Returns:
    pd.DataFrame: 综合得分数据
    """
    df = pd.read_excel(file_path)
    return df


def calculate_mean_scores(df):
    """
    按类型分组计算每种得分的平均值

    Parameters:
    df (pd.DataFrame): 合并后的数据

    Returns:
    pd.DataFrame: 包含分组平均值的DataFrame
    """
    # 假设得分列名为'得分1', '得分2', '得分3'，请根据实际数据修改
    score_columns = ['FID得分', 'HPSv2得分', 'ImageReward得分']
    # 按类型分组并计算平均值
    grouped_means = df.groupby('类型')[score_columns].mean()

    return grouped_means


def calculate_comprehensive_mean(df):
    """
    按类型分组计算综合得分的平均值

    Parameters:
    df (pd.DataFrame): 综合得分数据

    Returns:
    pd.Series: 分组后的综合得分平均值
    """
    # 按类型分组并计算综合得分的平均值
    comprehensive_mean = df.groupby('类型')['综合得分'].mean()
    return comprehensive_mean


def create_bar_chart_with_line(means, comprehensive_scores, hex_colors, line_color,
                               x_labels, legend_labels, y_range=None):
    """
    创建带有综合得分折线图的柱状图

    Parameters:
    means (pd.DataFrame): 包含平均值的DataFrame
    comprehensive_scores (pd.Series): 综合得分平均值
    hex_colors (list): 三种得分的HEX颜色代码列表
    line_color (str): 折线图的HEX颜色代码
    x_labels (list): 横轴标签列表
    legend_labels (list): 图例标签列表
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
                      alpha=0.8)  # 稍微调整透明度以便看清折线

    # 绘制综合得分折线图
    line = ax.plot(x_pos, comprehensive_scores,
                   color=line_color,
                   marker='o',
                   markersize=8,
                   linewidth=2.5,
                   label='综合得分',
                   zorder=5)  # 确保折线在柱子上方

    # 在折线图的每个点上显示数值（可选）
    for i, value in enumerate(comprehensive_scores):
        ax.text(i, value, f'{value:.2f}',
                ha='center', va='bottom', fontsize=10)

    # 设置横轴标签
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels)

    # 设置纵轴范围
    if y_range:
        ax.set_ylim(y_range)
    else:
        # 自动计算合适的纵轴范围
        all_values = list(means.values.flatten()) + list(comprehensive_scores.values)
        data_min = min(all_values)
        data_max = max(all_values)
        margin = (data_max - data_min) * 0.1  # 增加10%的边距
        ax.set_ylim(max(0, data_min - margin), data_max + margin)

    # 添加标签和标题（根据需要取消注释）
    # ax.set_xlabel('类型')
    # ax.set_ylabel('平均得分')
    # ax.set_title('不同类型得分平均值比较（含综合得分）')

    # 添加图例
    ax.legend(fontsize=16)

    # 添加网格线以便于阅读
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # 优化布局
    plt.tight_layout()

    # 保存 & 显示
    plt.savefig('Compare_EvaluateScore_with_Comprehensive-1.png', dpi=300)
    print(f"已生成图片：Compare_EvaluateScore_with_Comprehensive-1.png")

    # 显示图形
    plt.show()


def main():
    # 1. 定义文件路径（请根据实际文件路径修改）
    score_file_paths = [
        'E:/2025-09-08/5.2/Class/Done/2-0_FID_Score.xlsx',
        'E:/2025-09-08/5.2/Class/Done/2-1_HPSv2_Score.xlsx',
        'E:/2025-09-08/5.2/Class/Done/2-1_ImageReward_Score.xlsx'
    ]

    # 综合得分文件路径（请根据实际路径修改）
    comprehensive_file_path = 'E:/2025-09-08/5.2/Class/Done/2-2_Comprehensive_Score.xlsx'

    try:
        # 2. 读取和处理原有得分数据
        combined_data = read_and_process_data(score_file_paths)

        # 3. 读取综合得分数据
        comprehensive_data = read_comprehensive_score(comprehensive_file_path)

        # 4. 计算分组平均值
        means = calculate_mean_scores(combined_data)
        print("计算得到的平均值:")
        print(means)

        # 5. 计算综合得分平均值
        comprehensive_means = calculate_comprehensive_mean(comprehensive_data)
        print("\n综合得分平均值:")
        print(comprehensive_means)

        # 6. 自定义图表参数
        # 柱状图HEX颜色代码
        bar_colors = [
            '#C3E2EC',  # 浅蓝色
            '#BDEDC5',  # 浅绿色
            '#F7C4C1'  # 浅粉色
        ]

        # 折线图颜色（可自定义）
        line_color = '#FF6B6B'  # 红色，您可以修改为任何喜欢的颜色
        # 其他可选颜色示例：
        # line_color = '#4ECDC4'  # 青色
        # line_color = '#45B7D1'  # 天蓝色
        # line_color = '#96CEB4'  # 绿色
        # line_color = '#9B59B6'  # 紫色

        # 横轴标签
        custom_x_labels = [
            'r=8,α=4',
            'r=16,α=8',
            'r=32,α=16',
            'r=64,α=32',
            'r=128,α=64'
        ]

        # 图例标签
        custom_legend = [
            'FID(1/10)',
            'HPSv2(5x)',
            'ImageReward(1.5x)'
        ]

        # 纵轴范围（可选，如不指定则自动计算）
        # custom_y_range = (0, 100)  # 示例范围

        # 7. 创建带折线图的柱状图
        create_bar_chart_with_line(
            means,
            comprehensive_means,
            bar_colors,
            line_color,
            custom_x_labels,
            custom_legend
        )

    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        print("请检查文件路径是否正确")
    except KeyError as e:
        print(f"数据列名错误: {e}")
        print("请检查Excel文件中的列名是否正确")
    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()