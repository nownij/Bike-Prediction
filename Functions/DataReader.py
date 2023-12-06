import pandas as pd

newColumns = ['Date', 'HHMM', 'ST-start', 'ST-end', 'Use', 'Minute[min]', 'Distance[m]']
uselessColumns = ['구분코드', '시작대여소명', '종료대여소명']

def GetDataFromCSV(file_path):
    try:
        # Try reading with utf-8 encoding
        data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # If utf-8 fails, try reading with cp949 encoding
        data = pd.read_csv(file_path, encoding='cp949')

    # Rename columns
    data.columns = newColumns

    # Drop useless columns if they exist
    data = data.drop(columns=uselessColumns, errors='ignore') # 8월은 자료 자체가 없고, 9,10은 데이터형식이 개박살

    return data