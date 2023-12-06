from Functions import DataReader as DR
from Functions import DataProcessor as DP
from Functions import DataAnalyzer as DA

import pandas as pd

def MergeDataframes(filename_result):
    # List to store individual DataFrames
    dataframes = []

    # Loop through each filename_result to process and append the result to dataframes
    for i in range(len(filename_result)):
        # Assuming Rd.GetDataFromCSV, Rd.DataOptimization, and Rd.UsageOverTime functions are defined
        data = DR.GetDataFromCSV(filename_result[i])
        print(f"Get Data Complete : {filename_result[i]}")
        data_op = DP.DataOptimization(data)
        print(f"Optimization Complete : {filename_result[i]}")
        result = DA.UsageOverTime(data_op, 10)
        print(f"Resampled Data Complete : {filename_result[i]}\n\n")

        dataframes.append(result)

    # Initialize the merged DataFrame with the first DataFrame
    merged_df = dataframes[0]

    # Iterate through the remaining DataFrames for merging
    for df in dataframes[1:]:
        # Merge based on HHMM and suffixes for identifying columns
        merged_df = pd.merge(merged_df, df, on='HHMM', suffixes=('', '_y'))

        # Sum the 'Use' columns from both DataFrames
        merged_df['Use'] = merged_df[['Use', 'Use_y']].sum(axis=1)

        # Keep only the relevant columns (HHMM and the summed 'Use')
        merged_df = merged_df[['HHMM', 'Use']]

    # Return the final merged DataFrame
    return merged_df