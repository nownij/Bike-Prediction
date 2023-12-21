import psycopg2
import requests
import json
import pandas as pd
import schedule
import time
import sqlalchemy
from sqlalchemy import create_engine
import param as pr
import networkx as nx
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2
authKey = '53644e646777696338335a62654768'
db_engine = create_engine(pr.local_postgresql_url)

def calculate_total_distance(path, graph):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += graph[path[i]][path[i + 1]]
    return total_distance

def traveling_salesman_fixed_destination(graph, start, end):
    # 도착지점을 제외한 도시들의 순열을 생성
    cities = list(graph.keys())
    cities.remove(end)
    all_permutations = permutations(cities)

    # 최소 거리와 최소 거리 경로 초기화
    min_distance = float('inf')
    min_path = None

    # 각 순열에 대해 출발지점과 도착지점을 포함하여 거리 계산 및 갱신
    for path in all_permutations:
        path = (start,) + path + (end,)
        distance = calculate_total_distance(path, graph)
        if distance < min_distance:
            min_distance = distance
            min_path = path

    return min_distance, min_path

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371.0
    distance = R * c
    return distance

def create_emptydf(columns):
    empty_df = pd.DataFrame(columns=columns)
    return empty_df

def getStationInfo(authKey):
    info = []

    for i in range(3):
        gen_req_url = 'http://openapi.seoul.go.kr:8088/' + authKey + '/json/bikeList/' + str(i * 1000 + 1) + '/' + str(
            (i + 1) * 1000) + '/'
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
    code_list = [code.replace('ST-', '') for code in df['Code']]  # 광진구 코드

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
    new_info_df = new_info_df[['ST_Code', 'parkCnt', 'rackCnt']]  # parkCnt : 현재 주차된 자전거 개수, rackCnt : 전체 거치대 개수

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
        new_info_df.to_csv('./Data/test/data_{}.csv'.format(timestamp_str), index=False)
        print(f'Successfully executed {execution_count} times at {pd.Timestamp.now()}')
        # 변화량 계산을 위한 임시 테이블 가져오기

        tempdf = pd.read_sql_table(table_name="temptable", con=db_engine)

        new_info_df['time'] = [timestamp_str] * len(new_info_df)
        new_info_df['parkCnt'] = new_info_df['parkCnt'].astype(int)
        new_info_df['rackCnt'] = new_info_df['rackCnt'].astype(int)
        # 변화량 계산
        if len(tempdf) == 0:
            new_info_df['delta'] = [0] * len(new_info_df)
            new_info_df['accum_delta'] = [0] * len(new_info_df)
        else:
            df_inner_join = pd.merge(new_info_df, tempdf, left_on='ST_Code', right_on='ST_Code', how='inner')
            new_info_df['delta'] = new_info_df['parkCnt'] - tempdf['parkCnt']
            new_info_df['accum_delta'] = new_info_df['delta'] + tempdf['accum_delta']

        over_st = new_info_df.loc[(new_info_df['parkCnt']/new_info_df['rackCnt']>=2) | (new_info_df['delta']>=3),'ST_Code']
        under_st = new_info_df.loc[(new_info_df['parkCnt'] / new_info_df['rackCnt'] <= 0) | (new_info_df['delta'] <= -3), 'ST_Code']
        over_st_index_list = over_st.index.tolist()
        under_st_index_list = under_st.index.tolist()
        # print(over_st)
        # print(under_st)

        # CSV 파일에서 자전거 정류장 정보 읽어오기
        df = pd.read_csv('./Data/bikestationinfo(23.06).csv')

        # 그래프 초기화
        G = nx.Graph()

        # 각 정류장을 그래프의 노드로 추가
        for index, row in df.iterrows():
            G.add_node(index, pos=(row['Latitude'], row['Longitude']))

        over_point = over_st_index_list
        start_point_over = over_point[0]
        mid_point = over_point[1:len(over_point) - 1]
        end_point_over = over_point[len(over_point) - 1]

        nodedf = pd.DataFrame(columns=over_point, index=over_point)
        for i in over_point:
            distance = {}
            for j in over_point:
                distance[j] = haversine(df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                                        df.iloc[j]['Latitude'], df.iloc[j]['Longitude'])
            nodedf[i] = distance
        min_distance_over, min_path_over = traveling_salesman_fixed_destination(nodedf, start_point_over, end_point_over)

        under_point = under_st_index_list
        start_point_under = under_point[0]
        mid_point = under_point[1:len(under_point) - 1]
        end_point_under = under_point[len(under_point) - 1]

        nodedf = pd.DataFrame(columns=under_point, index=under_point)
        for i in under_point:
            distance = {}
            for j in under_point:
                distance[j] = haversine(df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                                        df.iloc[j]['Latitude'], df.iloc[j]['Longitude'])
            nodedf[i] = distance
        min_distance_under, min_path_under = traveling_salesman_fixed_destination(nodedf, start_point_under, end_point_under)

        min_path_under_list = []
        min_path_over_list = []
        for i in min_path_under:
            min_path_under_list.append(i)
        for i in min_path_over:
            min_path_over_list.append(i)
        min_path_under_list.pop(0)
        min_path_over_list.pop(0)
        min_path_index = min_path_under_list+min_path_over_list
        min_path = []
        for i in min_path_index:
            min_path.append(new_info_df.iloc[i,0])
        min_distance = min_distance_over+min_distance_under
        print(min_path,min_distance)



        dict_var = {'time': sqlalchemy.types.VARCHAR(length=12),
                    'ST_Code': sqlalchemy.types.VARCHAR(length=8),
                    'parkCnt' : sqlalchemy.types.INT,
                    'rackCnt': sqlalchemy.types.INT,
                    'delta': sqlalchemy.types.INT,
                    'accum_delta': sqlalchemy.types.INT,
                    }


        new_info_df.to_sql('temptable', con=db_engine, index=False, if_exists='replace', dtype=dict_var)
        new_info_df.to_sql('seoulbike', con=db_engine, index=False, if_exists='append')

    except Exception as e:
        print(f'Error during execution {execution_count}: {e}')


if __name__ == "__main__":
    # Initialize execution_count
    execution_count = 0
    crawl_and_save()
    # 10분 간격으로 크롤링 작업을 스케줄
    schedule.every(1).minutes.do(crawl_and_save)

    while execution_count < 500:
        schedule.run_pending()
        time.sleep(1)
