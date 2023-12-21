# dataProcessor.py
from datetime import datetime, timedelta
import os
import pandas as pd

# Date Setting System
def setOptions():
    # Set display options to show all rows and columns in DataFrames
    pd.reset_option('display.max_rows', None)
    pd.reset_option('display.max_columns', None)
    # Disable the Warning(Not Recommended)
    pd.set_option('mode.chained_assignment', None)
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False
def weekdays_weekends(dateRange):
    weekdays = [date for date, day in dateRange if day not in ['Sat', 'Sun']]
    weekends = [date for date, day in dateRange if day in ['Sat', 'Sun']]
    holidays = [('20230101', 'Mon'),
                ('20230123', 'Mon'),
                ('20230124', 'Tue'),
                ('20230301', 'Wed'),
                ('20230505', 'Fri'),
                ('20230529', 'Mon'),
                ('20230606', 'Tue'),
                ('20230815', 'Tue'),
                ('20230928', 'Thu'),
                ('20230929', 'Fri'),
                ('20231003', 'Tue'),
                ('20231009', 'Mon')]  # You can add more holidays

    holiday_dates = [date for date, _ in holidays]

    wkdayList = [date_info for date_info in dateRange if date_info[0] in weekdays and date_info[0] not in holiday_dates]
    wkendList = [date_info for date_info in dateRange if date_info[0] in (weekends + holiday_dates)]

    return wkdayList, wkendList
def chooseDate():
    while True:
        start_date_str = input("Start date (YYYYMMDD) >> ")
        end_date_str   = input("End date   (YYYYMMDD) >> ")

        try:
            start_date = datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.strptime(end_date_str, '%Y%m%d')

            if start_date > end_date:
                raise ValueError("End date should be equal to or after the start date.")

            dateRange = [(current_date.strftime('%Y%m%d'), current_date.strftime('%a')) for current_date in
                         (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1))]

            wkdayList, wkendList = weekdays_weekends(dateRange)

            while True:
                holiday_var = input("Filter : ALL [0] / Weekdays [1] / Holidays [2] >> ")
                if holiday_var == '0':
                    return dateRange
                elif holiday_var == '1':
                    return wkdayList
                elif holiday_var == '2':
                    return wkendList
                else:
                    print("Select again.")

        except ValueError as e:
            print(f"Invalid Input : {e}. Please Enter Valid Dates.")

# Bike Data Collection System
def tpss_readCsv(period):
    dateList, dayList = zip(*period)

    original_df_list = []

    for date in dateList:
        year_month = date[:6]
        csv_file_path = f"./Data/tpss_bcycl_od_statnhm_{year_month}/tpss_bcycl_od_statnhm_{date}.csv"

        if os.path.exists(csv_file_path):
            try:
                # reading with utf-8 encoding
                original_df_list.append(pd.read_csv(csv_file_path, encoding='utf-8'))
            except UnicodeDecodeError:
                # reading with cp949 encoding
                original_df_list.append(pd.read_csv(csv_file_path, encoding='cp949'))
        else:
            print("There is no file name of : ", csv_file_path)

    return original_df_list
def tpss_dataProcessing(df_list):
    selected_columns = ['기준_날짜', '기준_시간대', '시작_대여소_ID', '종료_대여소_ID', '전체_건수', '전체_이용_분', '전체_이용_거리']
    new_column_names = ['Date', 'HHMM', 'ST-start', 'ST-end', 'Use', 'Minute[min]', 'Distance[m]']
    target_info_file_path = "./Data/bikeStationInfo(23.06).csv"

    target_info = pd.read_csv(target_info_file_path)

    filtered_df_list = []

    for df in df_list:
        df = df[selected_columns]
        df.rename(columns=dict(zip(selected_columns, new_column_names)), inplace=True)

        df = df[~((df['ST-start'] == df['ST-end']) & (df['Minute[min]'] < 3))]
        df = df[df['ST-end'] != 'CENTER']
        df = df[df['Minute[min]'] != 0]

        df = df[df['ST-start'].isin(target_info['Code']) | df['ST-end'].isin(target_info['Code'])]
        df = df.reset_index(drop=True)

        filtered_df_list.append(df)

    # Function : Sum By Use
    sumByuse_df_list = sum_by_use(filtered_df_list)

    return sumByuse_df_list
def sum_by_use(df_list):
    sumByuse_df_list = []

    for df in df_list:
        df['HHMM'] = pd.to_numeric(df['HHMM'])
        full_range = [i for i in range(0, 2400, 5) if i % 100 < 60]
        df = pd.DataFrame({'HHMM': full_range}).merge(df, on='HHMM', how='left').fillna(0)

        df['HHMM'] = df['HHMM'].astype(str).str.zfill(4)
        df = df.groupby('HHMM')['Use'].sum().reset_index().astype(int)

        sumByuse_df_list.append(df)

    return sumByuse_df_list
def concat_df(df_list):
    df = pd.concat(df_list, ignore_index=True)
    res_df = df.groupby('HHMM').agg({'Use': 'mean', 'temp': 'mean'}).round(2).reset_index()

    return res_df

# Temperature Data Collection System
def temp_readCsv(period):
    original_temp_df = pd.read_csv("./Data/temp.csv", encoding='utf-8')

    dateList, dayList = zip(*period)
    dateList = [int(date) for date in dateList]  # str -> int

    temperature_df_list = []

    temp_df = original_temp_df[original_temp_df['Date'].isin(dateList)]
    temp_df = temp_df.reset_index(drop=True)

    unique_dates = temp_df['Date'].unique()

    for date in unique_dates:
        temp = temp_df[temp_df['Date'] == date].set_index('Date').transpose().rename(columns={date: 'temp'})
        temperature_df_list.append(temp)

    return temperature_df_list
def temp_dataProcessing(df_list):
    result_temp_df_list = []

    for df in df_list:
        df = df.loc[df.index.repeat(12)].reset_index(drop=True)
        df['HHMM'] = [i for i in range(0, 2400, 5) if i % 100 < 60]
        df = df[['HHMM', 'temp']]
        result_temp_df_list.append(df)

    return result_temp_df_list

# Merge Bike Data & Temperature Data
def mergeDataframes(tpss_df_list, temp_df_list):
    result_df_list = []

    for df1, df2 in zip(tpss_df_list, temp_df_list):
        df = pd.merge(df1, df2, on='HHMM')
        result_df_list.append(df)

    return result_df_list