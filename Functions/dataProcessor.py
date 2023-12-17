# DataProcessor.py
from datetime import datetime, timedelta
import os
import pandas as pd

# Set display options to show all rows and columns in DataFrames
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def is_valid_date(date_str):
    # Check if the input string is a valid date formatted as '%Y%m%d'
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False

def select_date():
    while True:
        start_date = input("Start date (YYYYMMDD): ")
        end_date = input("End date   (YYYYMMDD): ")

        # Error condition 1: If the input is not an 8-digit string
        if not (is_valid_date(start_date) and is_valid_date(end_date)):
            print("Invalid date format. Please enter dates in the format YYYYMMDD.")
            continue

        # Error condition 2: If the end date is before the start date
        start_date_obj = datetime.strptime(start_date, '%Y%m%d')
        end_date_obj = datetime.strptime(end_date, '%Y%m%d')
        if start_date_obj > end_date_obj:
            print("End date should be equal to or after the start date. Please enter valid dates.")
            continue

        # If valid, create a date range
        date_range = []
        current_date = start_date_obj

        while current_date <= end_date_obj:
            date_range.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)

        return date_range

def read_csv_files_in_date_range(date_range):
    original_data = []

    # Read CSV files within the selected date range
    for date_str in date_range:
        year_month_str = date_str[:6]
        csv_file_path = f"Data/tpss_bcycl_od_statnhm_{year_month_str}/tpss_bcycl_od_statnhm_{date_str}.csv"

        if os.path.exists(csv_file_path):
            try:
                # Try reading with utf-8 encoding
                original_data.append(pd.read_csv(csv_file_path, encoding='utf-8'))

            except UnicodeDecodeError:
                # If utf-8 fails, try reading with cp949 encoding
                original_data.append(pd.read_csv(csv_file_path, encoding='cp949'))

        else:
            print('There is no file name of : ', csv_file_path)

    return original_data

def set_columns(data):
    selected_columns = ['기준_날짜', '기준_시간대', '시작_대여소_ID', '종료_대여소_ID', '전체_건수', '전체_이용_분', '전체_이용_거리']
    new_column_names = ['Date', 'HHMM', 'ST-start', 'ST-end', 'Use', 'Minute[min]', 'Distance[m]']

    result_data = []

    for df in data:
        df = df[selected_columns]
        df.rename(columns=dict(zip(selected_columns, new_column_names)), inplace=True)
        result_data.append(df)

    return result_data

def remove_useless_data(data):
    result_data = []
    for df in data:
        # Deletion criteria 1: Delete rows where 'ST-start' and 'ST-end' are the same, and 'Minute[min]' is less than 3
        df = df[~((df['ST-start'] == df['ST-end']) & (df['Minute[min]'] < 3))]
        # Deletion criteria 2: Delete rows where 'ST-end' is 'CENTER'
        df = df[df['ST-end'] != 'CENTER']
        # Deletion criteria 3: Delete rows where 'Minute[min]' is 0
        df = df[df['Minute[min]'] != 0]

        result_data.append(df)

    return result_data

def set_target_location(data):
    target_info_file_path = "Data/bikeStationInfo(23.06).csv"

    target_info = pd.read_csv(target_info_file_path)
    codeList = target_info['Code'].tolist()

    # For each DataFrame, delete rows where 'ST-start' and 'ST-end' do not match values in the 'Code' column of target_info
    result_data = []
    for df in data:
        df = df[df['ST-start'].isin(target_info['Code']) | df['ST-end'].isin(target_info['Code'])]
        # Reset index
        df = df.reset_index(drop=True)
        result_data.append(df)

    return result_data

def merge_dataFrames(data):
    # Initialize the DataFrame to store the final result
    final_result = pd.DataFrame(columns=['HHMM', 'Use', 'Minute[min]', 'Distance[m]'])

    # Loop to merge all DataFrames in the array
    for df in data:
        # Drop 'Date', 'ST-start', and 'ST-end' columns
        df = df.drop(['Date', 'ST-start', 'ST-end'], axis=1, errors='ignore')

        # Sum the values for columns where 'HHMM' is the same
        grouped = df.groupby('HHMM').sum().reset_index()

        # Add the result to the final result
        final_result = pd.concat([final_result, grouped])

    # Sum the values where 'HHMM' is the same in the final result
    final_result = final_result.groupby('HHMM').sum().reset_index()

    return final_result