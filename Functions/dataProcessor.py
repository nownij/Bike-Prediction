# dataProcessor.py
from datetime import datetime, timedelta
import os
import pandas as pd

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
def read_tpss_csv(period):
    dateList, dayList = zip(*period)

    original_df_list = []

    for date_str in dateList:
        year_month_str = date_str[:6]
        csv_file_path = f"./Data/tpss_bcycl_od_statnhm_{year_month_str}/tpss_bcycl_od_statnhm_{date_str}.csv"

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
def read_temp_csv(period):
    dateList, dayList = zip(*period)

    dateList = [int(date) for date in dateList] # str -> int

    temp_data = pd.read_csv("./Data/temp.csv", encoding='utf-8')
    df = temp_data[temp_data['Date'].isin(dateList)]
    # 이거 이제 날짜별로 데이터프레임 만들어서, 리스트에 담고 sumByuse_df_list 인덱스 맞는걸로 기온 합쳐서 새로운 데이터프레임 형식 제작
    # 학습용으로다가~
    return df
def filtering(df_list):
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

    return filtered_df_list
def sumByUse(df_list):
    sumByuse_df_list = []

    for df in df_list:
        df['HHMM'] = pd.to_numeric(df['HHMM'])
        full_range = [i for i in range(0, 2400, 5) if i % 100 < 60]
        df = pd.DataFrame({'HHMM': full_range}).merge(df, on='HHMM', how='left').fillna(0)

        df['HHMM'] = df['HHMM'].astype(str).str.zfill(4)
        df = df.groupby('HHMM')['Use'].sum().reset_index().astype(int)

        sumByuse_df_list.append(df)

    return sumByuse_df_list
