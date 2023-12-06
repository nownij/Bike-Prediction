import pandas as pd

def UsageOverTime(DataFrame, interval):
    # Drop unnecessary columns
    DataFrame = DataFrame.drop(['Date', 'ST-start', 'ST-end', 'Minute[min]', 'Distance[m]'], axis=1)

    # Group by 'HHMM' and sum the 'Use' values
    resultDF = DataFrame.groupby(['HHMM'], as_index=False)['Use'].sum()

    resultDF['HHMM'] = resultDF['HHMM'].astype(str).str.zfill(4)
    resultDF['Datetime'] = pd.to_datetime(resultDF['HHMM'], format='%H%M')

    # Set 'Datetime' as the index
    resultDF.set_index('Datetime', inplace=True)

    # Set the resampling interval
    itVL = str(interval) + 'T'

    # Resample the DataFrame and sum the values within each interval
    resampledDF = resultDF.resample(itVL).sum()

    # Reset the index and convert 'Datetime' back to 'HHMM' format
    resampledDF.reset_index(inplace=True)
    resampledDF['HHMM'] = resampledDF['Datetime'].dt.strftime('%H%M').astype(int)

    # Reorder columns
    resampledDF = resampledDF[['HHMM', 'Use']]

    return resampledDF