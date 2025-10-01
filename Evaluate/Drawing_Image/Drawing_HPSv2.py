# -*- coding: utf-8 -*-
"""
HPSv2 得分散点图绘制工具
author : kimi
date   : 2025-09
"""

# -------------------- 用户配置区（按需要改） --------------------
FILE_PATH      = r"E:/2025-09-08/5.2/Class/2-1_HPSv2_Score.xlsx"         # 1. 你的 Excel 文件
SHEET_NAME     = 0                     # 0 表示第一个工作表，也可写表名
COL_ID         = "序号"                # 原始列名
COL_TYPE       = "类型"
COL_FILE       = "文件名"
COL_SCORE      = "HPSv2得分"

# 3. 5 组 HEX 颜色（按类型 1~5 对位）
HEX_COLORS = ['#FF7043', '#0077BB', '#CC3311', '#33BBEE', '#EE3377']

# 6. 图例文字（不想改就保持 None，默认用“类型1 … 类型5”）
LEGEND_LABELS = ['R=8,A=4', 'R=16,A=8', 'R=32,A=16', 'R=64,A=32', 'R=128,A=64']   # 可自定义，长度=5

# 8. 同类型散点横向拉开系数，越大越稀疏
SPREAD_FACTOR = 0.25

# 7. 类型与类型之间的中心距，越小越紧凑
CLUSTER_GAP = 0.8

# 均值折线颜色
MEAN_LINE_COLOR = "#97D1A0"

# 均值折线粗细
MEAN_LINE_WIDTH = 1.8

# 图片保存
SAVE_NAME = "HPSv2_scatter.png"
# -------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i + 2], 16) / 255 for i in (0, 2, 4))


def main():
    # 1. 读 Excel
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    df = df.rename(columns={
        COL_ID: "id",
        COL_TYPE: "type",
        COL_FILE: "file",
        COL_SCORE: "score"
    })

    # 2. 按类型分组
    type_groups = {i: grp for i, grp in df.groupby("type")}

    plt.figure(figsize=(6, 4))
    ax = plt.gca()

    colors = [hex_to_rgb(h) for h in HEX_COLORS]
    legend_text = LEGEND_LABELS if LEGEND_LABELS else [f"类型{i}" for i in range(1, 6)]

    mean_scores = []        # 用于折线
    x_centers   = []        # 类型中心横坐标

    # 3. 画散点
    for idx, (tp, grp) in enumerate(type_groups.items(), start=1):
        y = grp["score"].values
        n = len(y)
        base_x = idx * CLUSTER_GAP
        x_centers.append(base_x)
        mean_scores.append(y.mean())

        noise = (np.random.rand(n) - 0.5) * SPREAD_FACTOR
        x = base_x + noise

        ax.scatter(x, y,
                   color=colors[tp - 1],
                   s=36, edgecolors="white", linewidths=0.5)

    # 4. 画均值折线
    ax.plot(x_centers, mean_scores,
            color=MEAN_LINE_COLOR,
            linewidth=MEAN_LINE_WIDTH,
            marker="o", markersize=5,
            zorder=3, label="_nolegend_")  # 不进入图例

    # 5. 坐标轴样式
    ax.set_xticks([])
    y_min, y_max = df["score"].min(), df["score"].max()
    y_pad = 0.05 * (y_max - y_min)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True, prune=None))
    # ax.set_ylabel("HPSv2 得分")

    # 6. 图例：右下角 + 缩小
    ax.legend(legend_text,
              # title="类型",
              frameon=False,
              loc="lower right",
              fontsize=6,
              title_fontsize=7)

    # 7. 细节
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", ls="--", lw=0.5, alpha=0.4)
    plt.tight_layout()

    # 保存 & 显示
    plt.savefig(SAVE_NAME, dpi=300)
    print(f"已生成图片：{SAVE_NAME}")
    plt.show()


if __name__ == "__main__":
    main()