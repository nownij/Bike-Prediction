import pandas as pd

newColumns = ['Date', 'HHMM', 'ST-start', 'ST-end', 'Use', 'Minute[min]', 'Distance[m]']

def showCSV(file_path):
    data = pd.read_csv(file_path, encoding='cp949')
    data.columns = newColumns

    return data
def dataOptimization(DataFrame):
    DataFrame = selectLocation(DataFrame)
    DataFrame = sameST(DataFrame) # 대여한 곳에서 바로 자전거를 반납한 케이스 제거
    DataFrame = brokenBike(DataFrame) # 자전거가 고장나서 센터로 반납되는 케이스 제거
    DataFrame.reset_index(drop=True, inplace=True) # row 개수에 맞는 index 초기화

    return DataFrame
def selectLocation(DataFrame):
    bikeStationInfo = pd.read_csv('./bikeStationInfo(23.06).csv')
    codeList = bikeStationInfo['Code'].tolist()

    fullCase = DataFrame['ST-start'].isin(codeList) | DataFrame['ST-end'].isin(codeList)

    # other Conditions
    circular = DataFrame['ST-start'].isin(codeList) & DataFrame['ST-end'].isin(codeList)
    outflow = DataFrame['ST-start'].isin(codeList) & ~DataFrame['ST-end'].isin(codeList)
    inflow  = DataFrame['ST-end'].isin(codeList) & ~DataFrame['ST-start'].isin(codeList)

    DataFrame = DataFrame[fullCase]

    return DataFrame

    # 구, 동 선택하는 방법? 커맨드에서 받거나 시각화해서 클릭으로 설정하던가 일단 광진구 건대 쪽만 해보자

    # 광진구 내부에서만 움직이는 거
    # 광진구에서 빠져나가는거
    # 광진구로 들어오는거


    pass
def sameST(DataFrame):
    min_t = 5
    min_dst = 10

    sameST_condition = (DataFrame['ST-start'] == DataFrame['ST-end'])
    shortTime_condition = (DataFrame['Minute[min]'] <= min_t)
    shortDist_condition = (DataFrame['Distance[m]'] <= min_dst)

    # Set of Conditions
    drops = sameST_condition & shortTime_condition & shortDist_condition

    # Apply conditions and return the modified DataFrame
    return DataFrame[~drops]
def brokenBike(DataFrame):
    drops = DataFrame['ST-end'] == 'CENTER'

    # Apply conditions and return the modified DataFrame
    return DataFrame[~drops]


