# main.py
from Functions import dataProcessor as DtPR
from Functions import visualizer as VZ
import streamlit as st

def main():
    st.title("Bike Prediction Team #6")
    period = DtPR.chooseDate()

    if period is not None:
        pred_df = DtPR.mainSystem(period)

        VZ.show_df(period, pred_df)

# 실행 명령어 : streamlit run main.py
# 중단 명령어 : Ctrl + C
if __name__ == "__main__":
    main()