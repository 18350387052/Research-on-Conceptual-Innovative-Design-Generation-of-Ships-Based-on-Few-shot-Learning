import pandas as pd
import numpy as np
from pathlib import Path


def read_excel_file(file_path):
    """
    读取Excel文件

    参数:
        file_path: Excel文件路径

    返回:
        DataFrame: 包含学生成绩数据的DataFrame
    """
    try:
        df = pd.read_excel(file_path)
        print(f"成功读取文件: {file_path}")
        print(f"数据行数: {len(df)}")
        return df
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None


def calculate_student_scores(df):
    """
    计算每个学生的总成绩

    参数:
        df: 包含学生成绩数据的DataFrame

    返回:
        DataFrame: 包含学号、姓名、总成绩的DataFrame
    """
    # 确保列名正确（假设列名为中文）
    expected_columns = ['学号', '姓名', '课程名称', '课程性质', '单课程成绩', '单课程学分']

    # 如果列名不匹配，尝试使用索引
    if not all(col in df.columns for col in expected_columns):
        print("警告：列名不完全匹配，尝试使用列索引")
        df.columns = expected_columns[:len(df.columns)]

    results = []

    # 按学号分组处理
    grouped = df.groupby('学号')

    for student_id, student_data in grouped:
        # 获取学生姓名（取第一条记录的姓名）
        student_name = student_data['姓名'].iloc[0]

        # 分离学位课和非学位课
        degree_courses = student_data[student_data['课程性质'] == 0]
        non_degree_courses = student_data[student_data['课程性质'] == 1]

        # 计算学位课加权平均分
        if len(degree_courses) > 0:
            degree_weighted_sum = (degree_courses['单课程成绩'] * degree_courses['单课程学分']).sum()
            degree_credit_sum = degree_courses['单课程学分'].sum()
            degree_avg = degree_weighted_sum / degree_credit_sum if degree_credit_sum > 0 else 0
        else:
            degree_avg = 0

        # 计算非学位课加权平均分
        if len(non_degree_courses) > 0:
            non_degree_weighted_sum = (non_degree_courses['单课程成绩'] * non_degree_courses['单课程学分']).sum()
            non_degree_credit_sum = non_degree_courses['单课程学分'].sum()
            non_degree_avg = non_degree_weighted_sum / non_degree_credit_sum if non_degree_credit_sum > 0 else 0
        else:
            non_degree_avg = 0

        # 计算总成绩
        total_score = degree_avg * 0.7 + non_degree_avg * 0.3

        # 添加到结果列表
        results.append({
            '学号': student_id,
            '姓名': student_name,
            '总成绩': round(total_score, 2)
        })

        # 打印详细信息（可选）
        print(f"学号: {student_id}, 姓名: {student_name}")
        print(f"  学位课平均分: {degree_avg:.2f} (课程数: {len(degree_courses)})")
        print(f"  非学位课平均分: {non_degree_avg:.2f} (课程数: {len(non_degree_courses)})")
        print(f"  总成绩: {total_score:.2f}")
        print("-" * 50)

    return pd.DataFrame(results)


def save_results(results_df, output_path):
    """
    保存结果到Excel文件

    参数:
        results_df: 包含计算结果的DataFrame
        output_path: 输出文件路径
    """
    try:
        results_df.to_excel(output_path, index=False)
        print(f"\n结果已保存到: {output_path}")
        print(f"共处理 {len(results_df)} 名学生的成绩")
    except Exception as e:
        print(f"保存文件失败: {e}")


def main():
    """
    主函数
    """
    # 设置输入和输出文件路径
    input_file = "D:/Users/cyc/2024RGclass_score.xlsx"  # 请修改为实际的输入文件名
    output_file = "D:/Users/cyc/2024RG学生总成绩.xlsx"  # 输出文件名

    print("=" * 60)
    print("学生成绩计算程序")
    print("=" * 60)

    # 读取Excel文件
    df = read_excel_file(input_file)

    if df is not None:
        print("\n开始计算学生总成绩...")
        print("=" * 60)

        # 计算每个学生的总成绩
        results = calculate_student_scores(df)

        # 保存结果
        save_results(results, output_file)

        # 显示统计信息
        print("\n统计信息:")
        print(f"最高分: {results['总成绩'].max():.2f}")
        print(f"最低分: {results['总成绩'].min():.2f}")
        print(f"平均分: {results['总成绩'].mean():.2f}")
        print(f"中位数: {results['总成绩'].median():.2f}")
    else:
        print("程序终止：无法读取输入文件")


# 交互式运行选项
def interactive_mode():
    """
    交互式模式，允许用户输入文件路径
    """
    print("=" * 60)
    print("学生成绩计算程序 - 交互模式")
    print("=" * 60)

    # 获取输入文件路径
    input_file = input("请输入成绩表文件路径（包含.xlsx后缀）: ").strip()
    if not input_file:
        input_file = "学生成绩表.xlsx"
        print(f"使用默认文件名: {input_file}")

    # 获取输出文件路径
    output_file = input("请输入输出文件路径（包含.xlsx后缀，直接回车使用默认）: ").strip()
    if not output_file:
        output_file = "学生总成绩.xlsx"
        print(f"使用默认输出文件名: {output_file}")

    # 读取和处理文件
    df = read_excel_file(input_file)

    if df is not None:
        print("\n开始计算学生总成绩...")
        print("=" * 60)

        results = calculate_student_scores(df)
        save_results(results, output_file)

        # 显示统计信息
        print("\n统计信息:")
        print(f"最高分: {results['总成绩'].max():.2f}")
        print(f"最低分: {results['总成绩'].min():.2f}")
        print(f"平均分: {results['总成绩'].mean():.2f}")
        print(f"中位数: {results['总成绩'].median():.2f}")

        # 询问是否显示详细结果
        show_details = input("\n是否显示所有学生的成绩？(y/n): ").strip().lower()
        if show_details == 'y':
            print("\n所有学生成绩：")
            print(results.to_string(index=False))
    else:
        print("程序终止：无法读取输入文件")


if __name__ == "__main__":
    # 选择运行模式
    print("请选择运行模式：")
    print("1. 默认模式（使用预设文件名）")
    print("2. 交互模式（手动输入文件路径）")

    choice = input("请输入选择 (1 或 2): ").strip()

    if choice == "2":
        interactive_mode()
    else:
        main()