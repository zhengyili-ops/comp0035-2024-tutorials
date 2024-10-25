import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def draw_and_save_histogram(df, columns=None):
    """绘制数据框的直方图并保存为.png文件，仅对指定的列绘图."""
    if columns is None or len(columns) == 0:  # 检查是否指定了列
        print("未指定列或指定的列为空，无法绘制直方图。")
        return

    # 选择指定的列
    numeric_cols = df[columns]

    if not numeric_cols.empty:
        axes = numeric_cols.hist(bins=10, figsize=(10, 6))

        for ax in axes.flatten():
            ax.set_xlabel('number value')
            ax.set_ylabel('frequency')
            ax.set_title(ax.get_title())

        plt.tight_layout()

        # 保存直方图
        save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)

        fig_fp = save_dir.joinpath('histogram_with_labels.png')
        plt.savefig(fig_fp)
        print(f'直方图已保存至 {fig_fp}')
        plt.show()  # 显示图像
    else:
        print("没有数值列可以绘制直方图.")


def draw_and_save_histogram_by_event_type(df, event_type, columns=None):
    """绘制并保存指定列的直方图，按事件类型过滤 ('summer' 或 'winter')."""
    filtered_df = df[df['type'] == event_type]

    if columns is None or len(columns) == 0:
        print(f"未指定列或指定的列为空，无法绘制 {event_type} 事件的直方图。")
        return

    numeric_cols = filtered_df[columns]

    if not numeric_cols.empty:
        axes = numeric_cols.hist(bins=10, figsize=(10, 6))

        for ax in axes.flatten():
            ax.set_xlabel('number value')
            ax.set_ylabel('frequency')
            ax.set_title(f"{event_type.capitalize()} Event: {ax.get_title()}")

        plt.tight_layout()

        # 保存直方图
        save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)

        fig_fp = save_dir.joinpath(f'histogram_{event_type}_events.png')
        plt.savefig(fig_fp)
        print(f'{event_type.capitalize()}事件的直方图已保存至 {fig_fp}')
        plt.show()  # 显示图像
    else:

        print(f"没有数值列可以绘制 {event_type} 事件的直方图.")


def draw_and_save_boxplot(df, columns=None):
    """绘制数据框的箱线图并保存为.png文件，仅对指定的列绘图."""
    if columns is None or len(columns) == 0:
        print("未指定列或指定的列为空，无法绘制箱线图。")
        return

    numeric_cols = df[columns]

    if not numeric_cols.empty:
        num_cols = len(numeric_cols.columns)
        nrows = (num_cols + 1) // 2

        fig, axes = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 4 * nrows))
        axes = axes.flatten()

        for idx, col in enumerate(numeric_cols.columns):
            numeric_cols.boxplot(column=col, ax=axes[idx])
            axes[idx].set_xlabel('number value')
            axes[idx].set_ylabel('distribution')
            axes[idx].set_title(f'{col} box diagram')

        for i in range(idx + 1, len(axes)):
            fig.delaxes(axes[i])
        plt.tight_layout()

        # 保存箱线图
        save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)

        fig_fp = save_dir.joinpath('boxplot_with_labels.png')
        plt.savefig(fig_fp)
        print(f'箱线图已保存至 {fig_fp}')
        plt.show()  # 显示图像
    else:
        print("没有数值列可以绘制箱线图.")


def draw_and_save_timeseries(df, x_col,
                             y_col,
                             xlabel="Start Date",
                             ylabel="Number of Participants",
                             title="Time Series"):

    """绘制并保存时间序列图."""
    df[x_col] = pd.to_datetime(df[x_col])

    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], label=y_col)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存时间序列图
    save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
    if not save_dir.exists():
        save_dir.mkdir(parents=True, exist_ok=True)

    fig_fp = save_dir.joinpath(f'{title.lower().replace(" ", "_")}.png')
    plt.savefig(fig_fp)
    print(f'时间序列图已保存至 {fig_fp}')
    plt.show()  # 显示图像
# 确保在函数定义之前有两个空行


def draw_and_save_timeseries_by_event_type(df, event_type,
                                           x_col='start',
                                           y_col='participants',
                                           xlabel="Start Date",
                                           ylabel="Number of Participants"):

    """按事件类型绘制并保存时间序列图。"""
    # 过滤数据
    filtered_df = df[df['type'] == event_type]
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df[x_col],
             filtered_df[y_col],
             label=f'{event_type.capitalize()} Participants')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f'{event_type.capitalize()} Participants Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存时间序列图
    save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
    if not save_dir.exists():
        save_dir.mkdir(parents=True, exist_ok=True)

    fig_fp = save_dir.joinpath(f'{event_type}_participants_timeseries.png')
    plt.savefig(fig_fp)
    print(f'{event_type.capitalize()}事件的时间序列图已保存至 {fig_fp}')
    plt.show()


def annotate_anomalies(df):
    """标注时间序列中的异常点（如 1994 年冬季残奥会）。"""
    df['start'] = pd.to_datetime(df['start'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['start'], df['participants'], label='Participants')

    # 标注 1994 年冬季残奥会
    plt.annotate(
        'Winter 1994 Paralympics',
        xy=(
            '1994-01-01',
            df.loc[df['start'] == '1994-01-01', 'participants'].values[0]
        ),
        xytext=('1996-01-01', 2000),
        arrowprops=dict(facecolor='black', shrink=0.05)
    )

    plt.xlabel('Start Date')
    plt.ylabel('Number of Participants')
    plt.title('Participants Over Time with Anomalies')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

# def draw_and_save_timeseries_gender(df):
#     """绘制并保存带有男女参与者的时间序列图."""
#     df['start'] = pd.to_datetime(df['start'])

#     plt.figure(figsize=(10, 6))
#     plt.plot(df['start'],
#              df['participants_m'],
#              label='Male Participants',
#              color='blue')
# plt.plot(
#     df['start'],
#     df['participants_f'],
#     label='Female Participants',
#     color='orange'
# )

#     plt.xlabel('Start Date')
#     plt.ylabel('Number of Participants')
#     plt.title('Number of Male and Female Participants Over Time')
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     # 保存带有性别数据的时间序列图
#     save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
#     if not save_dir.exists():
#         save_dir.mkdir(parents=True, exist_ok=True)

#     fig_fp = save_dir.joinpath('timeseries_gender_plot.png')
#     plt.savefig(fig_fp)
#     print(f'带有性别参与者的时间序列图已保存至 {fig_fp}')
#     plt.show()  # 显示图像


def draw_and_save_timeseries_gender(df):
    """绘制并保存带有男女参与者的时间序列图。"""
    df['start'] = pd.to_datetime(df['start'])

    plt.figure(figsize=(10, 6))
    plt.plot(
        df['start'],
        df['participants_m'],
        label='Male Participants',
        color='blue'
    )
    plt.plot(
        df['start'],
        df['participants_f'],
        label='Female Participants',
        color='orange'
    )

    plt.xlabel('Start Date')
    plt.ylabel('Number of Participants')
    plt.title('Number of Male and Female Participants Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存带有性别数据的时间序列图
    save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
    if not save_dir.exists():
        save_dir.mkdir(parents=True, exist_ok=True)

    fig_fp = save_dir.joinpath('timeseries_gender_plot.png')
    plt.savefig(fig_fp)
    print(f'带有性别参与者的时间序列图已保存至 {fig_fp}')
    plt.show()


def draw_grouped_timeseries(df, group_col, x_col, y_col):
    """按指定列分组绘制时间序列图."""
    df[x_col] = pd.to_datetime(df[x_col])

    # 按 group_col 进行分组
    grouped = df.groupby(group_col)

    plt.figure(figsize=(10, 6))

    for name, group in grouped:
        plt.plot(group[x_col], group[y_col], label=name)  # 按组绘制

    plt.xlabel('Start Date')
    plt.ylabel('Number of Participants')
    plt.title('Participants Over Time by Event Type')
    plt.legend()  # 显示图例以区分不同事件类型
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存时间序列图
    save_dir = Path(r"C:\comp0035-2024-tutorials\src\tutorialpkg\data")
    if not save_dir.exists():
        save_dir.mkdir(parents=True, exist_ok=True)

    fig_fp = save_dir.joinpath('timeseries_grouped_plot.png')
    plt.savefig(fig_fp)
    print(f'按类型分组的时间序列图已保存至 {fig_fp}')
    plt.show()


if __name__ == '__main__':
    # 指定CSV文件的路径
    csv_file_path = Path(r"C:\comp0035-2024-tutorials\src\
                           r:tutorialpkg\data\paralympics_events_prepared.csv")

    if csv_file_path.is_file():
        df_paralympics = pd.read_csv(csv_file_path)


if __name__ == '__main__':
    # 指定CSV文件的路径
    csv_file_path = Path(r"C:\comp0035-2024-tutorials\src\
                           r:tutorialpkg\data\paralympics_events_prepared.csv")

    if csv_file_path.is_file():
        df_paralympics = pd.read_csv(csv_file_path)

        # 绘制并保存 summer 事件的直方图
        draw_and_save_histogram_by_event_type(
            df_paralympics,
            'summer',
            columns=['participants_m', 'participants_f']
        )

        # 绘制并保存 winter 事件的直方图
        draw_and_save_histogram_by_event_type(
            df_paralympics,
            'winter',
            columns=['participants_m', 'participants_f']
        )

        # 绘制并保存箱线图
        draw_and_save_boxplot(
            df_paralympics,
            columns=['participants_m', 'participants_f']
        )

        # 绘制并保存 summer 和 winter 事件的时间序列图
        draw_and_save_timeseries_by_event_type(df_paralympics, 'summer')
        draw_and_save_timeseries_by_event_type(df_paralympics, 'winter')

        # 绘制按事件类型分组的时间序列图
        draw_grouped_timeseries(
            df_paralympics,
            'type',
            'start',
            'participants'
        )
        # 绘制并保存带有性别的时间序列图
        draw_and_save_timeseries_gender(df_paralympics)

        # 显示绘制的图像
        plt.show()

    else:
        print(f"文件 {csv_file_path} 不存在，请检查路径是否正确。")
