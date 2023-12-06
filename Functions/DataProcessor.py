import pandas as pd

def DataOptimization(DataFrame):
    # Select locations that are present in the bike station info
    DataFrame = select_location(DataFrame)

    # Remove cases where the bike is returned to the same station immediately
    DataFrame = same_station(DataFrame)

    # Remove cases where the bike is returned to the center due to a malfunction
    DataFrame = broken_bike(DataFrame)

    # Reset the index to match the number of rows in the DataFrame
    DataFrame.reset_index(drop=True, inplace=True)

    return DataFrame
def select_location(DataFrame):
    bikeStationInfo = pd.read_csv('./Data/bikeStationInfo(23.06).csv')
    codeList = bikeStationInfo['Code'].tolist()

    fullCase = DataFrame['ST-start'].isin(codeList) | DataFrame['ST-end'].isin(codeList)

    # other Conditions
    circular = DataFrame['ST-start'].isin(codeList) & DataFrame['ST-end'].isin(codeList)
    outflow = DataFrame['ST-start'].isin(codeList) & ~DataFrame['ST-end'].isin(codeList)
    inflow  = DataFrame['ST-end'].isin(codeList) & ~DataFrame['ST-start'].isin(codeList)

    DataFrame = DataFrame[fullCase]

    return DataFrame
def same_station(DataFrame):
    min_t = 5
    min_dst = 10

    sameST_condition = (DataFrame['ST-start'] == DataFrame['ST-end'])
    shortTime_condition = (DataFrame['Minute[min]'] <= min_t)
    shortDist_condition = (DataFrame['Distance[m]'] <= min_dst)

    # Set of Conditions
    drops = sameST_condition & shortTime_condition & shortDist_condition

    # Apply conditions and return the modified DataFrame
    return DataFrame[~drops]
def broken_bike(DataFrame):
    drops = DataFrame['ST-end'] == 'CENTER'

    # Apply conditions and return the modified DataFrame
    return DataFrame[~drops]