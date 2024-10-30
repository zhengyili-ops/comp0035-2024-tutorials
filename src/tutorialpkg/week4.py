import argparse
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: Path):
    """
    Load data from a CSV or Excel file.
    :param file_path: Path to the file.
    :return: DataFrame containing the loaded data.
    """
    if file_path.suffix == '.csv':
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Loaded CSV data from {file_path}")
            print(df.columns)  # Print column names to verify
            return df
        except FileNotFoundError as e:
            logging.error(f"CSV file not found. Please check the file path. Error: {e}")
    elif file_path.suffix in ['.xls', '.xlsx']:
        try:
            df = pd.read_excel(file_path)
            logging.info(f"Loaded Excel data from {file_path}")
            print(df.columns)  # Print column names to verify
            return df
        except FileNotFoundError as e:
            logging.error(f"Excel file not found. Please check the file path. Error: {e}")
    else:
        logging.error(f"Unsupported file type: {file_path.suffix}")
    return None

def print_data_types(df):
    """
    Print the data types of the DataFrame columns.
    :param df: DataFrame containing data.
    """
    if df is not None:
        logging.info("Data types of the columns:")
        print(df.dtypes)

def print_statistics(df):
    """
    Print basic statistics of the DataFrame columns.
    :param df: DataFrame containing data.
    """
    if df is not None:
        logging.info("Statistics of the dataset:")
        print(df.describe())

def check_unique_values(df, columns):
    """
    Check if the specified columns have unique values.
    :param df: DataFrame containing data.
    :param columns: List of columns to check for uniqueness.
    """
    if df is not None:
        for column in columns:
            if column in df.columns:
                if df[column].is_unique:
                    logging.info(f"Column '{column}' has unique values.")
                else:
                    duplicate_values = df[df.duplicated([column], keep=False)][column]
                    logging.warning(f"Column '{column}' does not have unique values. Duplicates at rows: {duplicate_values.index.tolist()}")
            else:
                logging.error(f"Column '{column}' not found in the dataset.")

def check_null_values(df, columns):
    """
    Check if the specified columns have any null values.
    :param df: DataFrame containing data.
    :param columns: List of columns to check for null values.
    """
    if df is not None:
        for column in columns:
            if column in df.columns:
                null_count = df[column].isnull().sum()
                if null_count > 0:
                    null_indices = df[df[column].isnull()].index.tolist()
                    logging.warning(f"Column '{column}' has {null_count} null values at rows: {null_indices}")
                else:
                    logging.info(f"Column '{column}' has no null values.")
            else:
                logging.error(f"Column '{column}' not found in the dataset.")

def check_date_format(df, columns, date_format="%d/%m/%Y"):
    """
    Check if the specified date columns match the given format.
    :param df: DataFrame containing data.
    :param columns: List of date columns to check.
    :param date_format: Expected date format.
    """
    if df is not None:
        for column in columns:
            if column in df.columns:
                for index, value in df[column].items():
                    try:
                        datetime.strptime(value, date_format)
                    except ValueError:
                        logging.error(f"Date format error in column '{column}' at row {index}: '{value}' does not match format {date_format}")
            else:
                logging.error(f"Column '{column}' not found in the dataset.")

def check_duration(df):
    """
    Check if the 'duration' column is equal to the difference between 'end' and 'start'.
    :param df: DataFrame containing data.
    """
    if df is not None:
        if 'start' in df.columns and 'end' in df.columns and 'duration' in df.columns:
            for index, row in df.iterrows():
                try:
                    start_date = datetime.strptime(row['start'], "%d/%m/%Y")
                    end_date = datetime.strptime(row['end'], "%d/%m/%Y")
                    expected_duration = (end_date - start_date).days
                    if row['duration'] != expected_duration:
                        logging.error(f"Duration error at row {index}: Expected {expected_duration}, found {row['duration']}")
                except ValueError as e:
                    logging.error(f"Date parsing error at row {index}: {e}")
        else:
            logging.error("Columns 'start', 'end', or 'duration' not found in the dataset.")

def check_column_constraints(df):
    """
    Check column constraints like NOT NULL, UNIQUE, etc.
    :param df: DataFrame containing data.
    """
    if df is not None:
        # Example checks for constraints based on dataset
        check_unique_values(df, ['event_code', 'year', 'country', 'host'])
        check_null_values(df, ['type', 'year', 'country', 'host', 'start', 'end', 'duration', 'Code'])
        check_date_format(df, ['start', 'end'])
        check_duration(df)

def main(file_type: str):
    # Use absolute paths for the files
    if file_type == 'csv':
        datafile = Path("C:/comp0035-2024-tutorials/src/tutorialpkg/data/paralympics_events_prepared.csv")
    elif file_type == 'excel':
        datafile = Path("C:/comp0035-2024-tutorials/src/tutorialpkg/data/paralympics_events_prepared.xlsx")
    else:
        logging.error("Unsupported file type. Use 'csv' or 'excel'.")
        return

    # Load data
    df_paralympics = load_data(datafile)

    # Print data types
    print_data_types(df_paralympics)

    # Print statistics
    print_statistics(df_paralympics)

    # Check column constraints
    check_column_constraints(df_paralympics)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the datatype of the columns in the paralympics dataset.')
    parser.add_argument('--file_type', type=str, choices=['csv', 'excel'], required=True, help='Specify the file type: csv or excel')
    args = parser.parse_args()

    main(args.file_type)
