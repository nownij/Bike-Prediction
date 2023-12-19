import time
from Functions import dataProcessor as DtPR
from Functions import visualizer as VZ
def settings():
    DtPR.set_display_option()
    dateRange = DtPR.chooseDate()

    return dateRange
def mainSystem(dateRange):
    wkdayList, wkendList = DtPR.weekdays_weekends(dateRange)
    dateList, dayList = zip(*wkdayList)
    start_time = time.time()
    # ----- Main System ---------------------------------------- #
    original_df_list = DtPR.readCSV(dateList)
    filtered_df_list = DtPR.filtering(original_df_list)
    sumByuse_df_list = DtPR.sumByUse(filtered_df_list)

    # VZ.show_df(dateList, sumByuse_df_list)
    # ---------------------------------------------------------- #
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program Run Time >> {elapsed_time:.4f} sec")

if __name__ == "__main__":
    dateRange = settings()
    mainSystem(dateRange)