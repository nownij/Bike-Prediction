# main.py
import time
from Functions import dataProcessor as DtPR
from Functions import visualizer as VZ
from Functions import train

def settings():
    DtPR.setOptions()
    period = DtPR.chooseDate()

    return period
def mainSystem(period):
    start_time = time.time()

    ori_tpss_df_list = DtPR.tpss_readCsv(period)
    res_tpss_df_list = DtPR.tpss_dataProcessing(ori_tpss_df_list)

    ori_temp_df_list = DtPR.temp_readCsv(period)
    res_temp_df_list = DtPR.temp_dataProcessing(ori_temp_df_list)

    result_df_list = DtPR.mergeDataframes(res_tpss_df_list, res_temp_df_list)

    pre_df = train.train_and_predict(result_df_list)
    VZ.show_df(period, pre_df)

    # VZ.show_df_list(period, result_df_list)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program Run Time >> {elapsed_time:.4f} sec")

def stationAnalysis(period):
    ori_tpss_df_list = DtPR.tpss_readCsv(period)

    pass

if __name__ == "__main__":
    period = settings()
    mainSystem(period)
