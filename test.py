import requests
import json
import pandas as pd
import schedule
import time

authKey = '53644e646777696338335a62654768'

# Real-Time Data
def getStationInfo(authKey):
    info = []

    for i in range(3):
        gen_req_url = 'http://openapi.seoul.go.kr:8088/' + authKey + '/json/bikeList/' + str(i * 1000 + 1) + '/' + str((i + 1) * 1000) + '/'
        print(gen_req_url)
        original_data = requests.get(gen_req_url)
        processed_data = json.loads(original_data.text)
        info = info + processed_data['rentBikeStatus']['row']

    # print(f'Show Original Data : {info}')

    return info
# Removing Unessential Component
def removeComponent(info):
    for item in info:
        del item['shared']
        del item['stationLatitude']
        del item['stationLongitude']
        del item['stationId']
def locationFilter(info):
    data = pd.read_csv("Data/bikeStationInfo(23.06).csv")
    df = pd.DataFrame(data)
    code_list = [code.replace('ST-', '') for code in df['Code']] # 광진구 코드

    # 'stationName'에서 숫자 추출하여 code_list에 있는 숫자들과 교집합 구하기
    numbers_in_station_name = [int(station['stationName'].split('.')[0]) for station in info]
    intersection_set = set(map(str, numbers_in_station_name)) & set(code_list)

    # 교집합에 해당하는 딕셔너리만 남기기
    new_info = [station for station in info if station['stationName'].split('.')[0] in intersection_set]
    new_info_df = pd.DataFrame(new_info)

    # 컬럼명 변경
    new_info_df = new_info_df.rename(
        columns={'rackTotCnt': 'rackCnt', 'stationName': 'ST_Code', 'parkingBikeTotCnt': 'parkCnt'})
    # col 위치 변경
    new_info_df = new_info_df[['ST_Code', 'parkCnt', 'rackCnt']] # parkCnt : 현재 주차된 자전거 개수, rackCnt : 전체 거치대 개수

    # ST_Code 내의 정보에서 . (온점) 앞 숫자만 남기기
    new_info_df['ST_Code'] = 'ST-' + new_info_df['ST_Code'].str.extract(r'(\d+)')

    return new_info_df
def crawl_and_save():
    global execution_count
    execution_count += 1

    try:
        info = getStationInfo(authKey)
        removeComponent(info)
        new_info_df = locationFilter(info)

        # 10분 간격으로 데이터를 저장 (CSV 형식)
        timestamp_str = pd.Timestamp.now().strftime('%Y%m%d%H%M')
        new_info_df.to_csv('./Data/test/data_{}'.format(timestamp_str), index=False)

        print(f'Successfully executed {execution_count} times at {pd.Timestamp.now()}')
    except Exception as e:
        print(f'Error during execution {execution_count}: {e}')

if __name__ == "__main__":
    # Initialize execution_count
    execution_count = 0

    # 10분 간격으로 크롤링 작업을 스케줄
    schedule.every(10).minutes.do(crawl_and_save)

    while execution_count < 5:
        schedule.run_pending()
        time.sleep(1)