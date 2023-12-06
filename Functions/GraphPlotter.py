import matplotlib.pyplot as plt

def ShowGraph(start_date, end_date, DataFrame):
    # graph Settings
    plt.figure(figsize=(12, 6))
    plt.plot(DataFrame['HHMM'], DataFrame['Use'], linestyle='solid')

    # graph title, label
    plt.title(f'2022/{start_date} ~ 2022/{end_date} Hourly Use Over Time', fontsize=16)
    plt.xlabel('HH:MM', fontsize=14)
    plt.ylabel('Use', fontsize=14)

    # show Graph
    plt.grid(True)
    plt.show()