from Functions import DateUtils as DU
from Functions import DateMerger as DM
from Functions import GraphPlotter as GP

import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

if __name__ == "__main__":
    start_date, end_date, filename_result = DU.DateRangeSettings()
    merged_df = DM.MergeDataframes(filename_result)
    GP.ShowGraph(start_date, end_date, merged_df)
    print(merged_df) # 2월 데이터도 이상해요