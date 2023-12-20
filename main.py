# main.py
import time
from Functions import dataProcessor as DtPR
from Functions import visualizer as VZ

def settings():
    DtPR.setOptions()
    period = DtPR.chooseDate()

    return period
def mainSystem(period):
    start_time = time.time()

    original_df_list = DtPR.read_tpss_csv(period)
    filtered_df_list = DtPR.filtering(original_df_list)
    sumByuse_df_list = DtPR.sumByUse(filtered_df_list)
    print(sumByuse_df_list)


    # VZ.show_df(period, sumByuse_df_list)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program Run Time >> {elapsed_time:.4f} sec")

if __name__ == "__main__":
    period = settings()
    #mainSystem(period)
    DtPR.read_temp_csv(period)