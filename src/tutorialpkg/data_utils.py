from pathlib import Path
import pandas as pd

def prepare_data(df, columns_to_change=None):
    if columns_to_change is None:
        columns_to_change = []

    print("\nColumns in the DataFrame for preparation:")
    print(df.columns)

    for col in columns_to_change:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype('int')
            print(f"Converted column '{col}' to integers.")
        else:
            print(f"Column '{col}' not found in the DataFrame, skipping conversion.")

    # 将 'start' 和 'end' 列转换为 datetime 类型
    if 'start' in df.columns:
        df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y', errors='coerce')
    if 'end' in df.columns:
        df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y', errors='coerce')

    # 处理 'type' 列中的空格和大小写
    if 'type' in df.columns:
        df['type'] = df['type'].str.strip().str.lower()  # 去除空格并转换为小写
        print("\nProcessed 'type' column (stripped whitespace and converted to lowercase).")

    # 删除 'URL', 'disabilities_included', 'highlights' 列，并分配给新的 DataFrame
    columns_to_drop = ['URL', 'disabilities_included', 'highlights']
    df_prepared = df.drop(columns=columns_to_drop, axis=1, errors='ignore')  # 删除指定的列
    print("\nDropped columns: 'URL', 'disabilities_included', 'highlights'.")

    # 添加新列 'duration'，计算持续天数并将其插入到 'end' 列后面
    if 'start' in df.columns and 'end' in df.columns:
        df_prepared.insert(df_prepared.columns.get_loc('end') + 1, 
                           'duration', 
                           (df_prepared['end'] - df_prepared['start']).dt.days.astype(int))
        print("\nAdded new column 'duration' based on the difference between 'start' and 'end'.")

    # 保存处理后的 DataFrame 到 CSV 文件
    output_path = Path(__file__).parent.joinpath("data", "paralympics_events_prepared.csv")
    df_prepared.to_csv(output_path, index=False)
    print(f"\nSaved prepared DataFrame to '{output_path}'.")

    # 打印新的 DataFrame 的列名
    print("\nColumns after preparation:")
    print(df_prepared.columns)

    return df_prepared


# 处理缺失值函数
def handle_missing_values(df):
    print("\nHandling missing values...")

    # 删除 'Name' 列
    if 'Name' in df.columns:
        df = df.drop(columns=['Name'])
        print("Dropped 'Name' column.")

    # 删除缺失参与者数据的行（index 0, 17, 31）
    df = df.drop([0, 17, 31], errors='ignore')
    print("Dropped rows with indexes 0, 17, and 31.")

    # 重置索引
    df = df.reset_index(drop=True)
    print("Index reset.")

    return df

# 替换国家名称
def replace_country_names(df):
    replacement_names = {
        'UK': 'Great Britain',
        'USA': 'United States of America',
        'Korea': 'Republic of Korea',
        'Russia': 'Russian Federation',
        'China': "People's Republic of China"
    }
    df['country'] = df['country'].replace(replacement_names)
    print("\nReplaced country names.")
    return df

# 新增：描述 DataFrame 的函数
def describe_dataframe(df):
    print(f"DataFrame shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())
    print("\nColumn labels:")
    print(df.columns)
    print("\nColumn data types:")
    print(df.dtypes)
    print("\nDataFrame info:")
    df.info()
    print("\nStatistical summary:")
    print(df.describe())

# 合并两个 DataFrames 的函数
def merge_dataframes(events_df, npc_df):
    merged_df = events_df.merge(npc_df, how='left', left_on='country', right_on='Name')
    print("\nMerged DataFrame with NPC Codes:")
    print(merged_df[['country', 'Code', 'Name']].head())  # 仅显示合并的部分
    return merged_df

# 主程序
def main():
    pd.set_option("display.max_columns", None)

    # 读取第一个 DataFrame (CSV 文件)
    try:
        paralympics_datafile_csv = Path(__file__).parent.joinpath("data", "paralympics_events_raw.csv")
        selected_columns = ['type', 'year', 'country', 'host', 'start', 'end', 'countries', 'events', 'sports',
                            'participants_m', 'participants_f', 'participants']
        events_csv_df = pd.read_csv(paralympics_datafile_csv, usecols=selected_columns)

        # 打印 'type' 列的唯一值，查看不一致
        print("\nUnique values in 'type' column before processing:")
        print(events_csv_df['type'].unique())

        print("\nStart and End Dates (Before Processing):")
        print(events_csv_df[['start', 'end']].head())
        print("\nMissing values in 'start' column:", events_csv_df['start'].isnull().sum())
        print("Missing values in 'end' column:", events_csv_df['end'].isnull().sum())

        events_columns_to_change = ['countries', 'events', 'participants_m', 'participants_f', 'participants']
        events_csv_df = prepare_data(events_csv_df, events_columns_to_change)

        # 打印处理后的 'type' 列的唯一值
        print("\nUnique values in 'type' column after processing:")
        print(events_csv_df['type'].unique())

        print("\nStart and End Dates (After Processing):")
        print(events_csv_df[['start', 'end']].head())

        events_csv_df = handle_missing_values(events_csv_df)  # 处理缺失值
        events_csv_df = replace_country_names(events_csv_df)  # 替换国家名称

        print("Prepared CSV file content:")
        describe_dataframe(events_csv_df)

        # 保存准备好的 DataFrame 到 CSV 文件
        output_path = Path(__file__).parent.joinpath("data", "paralympics_events_prepared.csv")
        events_csv_df.to_csv(output_path, index=False)
        print(f"\nSaved prepared DataFrame to '{output_path}'.")

    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")

    # 读取第二个 DataFrame (Excel 文件)
    try:
        excel_file = Path(__file__).parent.joinpath("data", "paralympics_all_raw.xlsx")
        df_excel = pd.read_excel(excel_file, sheet_name=0)

        excel_columns_to_change = ['Rank', 'Gold', 'Silver', 'Bronze', 'Total']
        df_excel = prepare_data(df_excel, excel_columns_to_change)

        print("\nExcel file content (first sheet):")
        describe_dataframe(df_excel)

        # 保存准备好的 Excel DataFrame
        output_excel_path = Path(__file__).parent.joinpath("data", "paralympics_excel_prepared.csv")
        df_excel.to_csv(output_excel_path, index=False)
        print(f"\nSaved prepared Excel DataFrame to '{output_excel_path}'.")

    except FileNotFoundError as e:
        print(f"Excel file (first sheet) not found. Please check the file path. Error: {e}")

    # 读取 npc_codes.csv 并合并
    try:
        npc_codes_file = Path(__file__).parent.joinpath("data", "npc_codes.csv")
        npc_codes_df = pd.read_csv(npc_codes_file, usecols=['Code', 'Name'], encoding='utf-8', encoding_errors='ignore')

        merged_df = merge_dataframes(events_csv_df, npc_codes_df)

        # 打印合并后的完整 DataFrame 输出
        print("Merged DataFrame with NPC Codes:")
        print(merged_df[['country', 'Code', 'Name']])

        # 保存合并后的 DataFrame
        output_merged_path = Path(__file__).parent.joinpath("data", "paralympics_merged_prepared.csv")
        merged_df.to_csv(output_merged_path, index=False)
        print(f"\nSaved merged DataFrame to '{output_merged_path}'.")

    except FileNotFoundError as e:
        print(f"NPC codes file not found. Please check the file path. Error: {e}")
    except Exception as e:
        print(f"An error occurred while reading the NPC codes file: {e}")

# 运行主程序
if __name__ == "__main__":
    main()
