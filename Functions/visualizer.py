# visualizer.py
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def show_df(period, df):
    dateList, dayList = zip(*period)

    fig, ax1 = plt.subplots()
    df['HHMM'] = pd.to_numeric(df['HHMM'])
    df['Use'] = pd.to_numeric(df['Use'])

    # 왼쪽 y축 설정
    ax1.set_xlabel('HHMM')
    ax1.set_ylabel('Use / Prediction', color='black')
    ax1.plot(df['HHMM'], df['Use'], color='blue', linestyle='-', label='Use')
    ax1.plot(df['HHMM'], df['prd_Use'], color='green', linestyle='-', label='prd_Use')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim(0, 100)
    ax1.grid(True)


    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature', color='black')
    ax2.plot(df['HHMM'], df['temp'], color='red', linestyle='--', label='temp')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.set_ylim(-20, 40)

    # x축 설정
    ax1.set_xticks(range(0, 2400, 200))
    ax1.set_xticklabels(ax1.get_xticks(), rotation=45)

    plt.title(f'{dateList[0]}~{dateList[-1]} Use & Prediction Over Time', fontsize=15)
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

    #plt.plot()
    st.pyplot(fig)
