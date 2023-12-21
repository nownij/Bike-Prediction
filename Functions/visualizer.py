# visualizer.py
import matplotlib.pyplot as plt

def show_df_list(period, df_list):
    dateList, dayList = zip(*period)

    for i, df in enumerate(df_list):
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plotting 'Use' on the primary y-axis
        line1 = ax1.plot(df['HHMM'], df['Use'], linestyle='-', color='b', label='Use')[0]

        # Adding 'temp' to the secondary y-axis
        ax2 = ax1.twinx()
        line2 = ax2.plot(df['HHMM'], df['temp'], linestyle='-', color='r', label='temp')[0]

        # Set labels and title
        ax1.set_xlabel('HHMM')
        ax1.set_ylabel('Bike Use', color='b', fontsize=10)
        ax2.set_ylabel('Temperature', color='r', fontsize=10)
        plt.title(f'{dateList[i]} ({dayList[i]}) HHMM : Use')

        # Set y-axis limits and grid for 'Use'
        ax1.set_ylim(0, 100)
        ax1.grid(True)

        # Set y-axis limits for 'temp'
        ax2.set_ylim(-20, 40)

        # Display legend
        lines = [line1, line2]
        labels = [line.get_label() for line in lines]
        ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.7, 1))

        # Annotate max 'Use' value with a box
        max_value = df['Use'].max()
        max_index = df['Use'].idxmax()
        max_x = df.loc[max_index, 'HHMM']
        ax1.text(max_x, max_value, f'Max Use: ({max_x}, {max_value})', verticalalignment='bottom',
                 horizontalalignment='left', fontsize=9, color='blue')

        #plt.show()

        #plt.savefig(f'Data/graph/plot_{dateList[i]}.png')
        #print(f"File saved : plot_{dateList[i]}.png")
def show_df(period, df):
    dateList, dayList = zip(*period)

    fig, ax1 = plt.subplots()

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

    if 'Sat' not in dayList and 'Sun' not in dayList:
        day = 'Weekday'
    else:
        day = 'Weekend'

    if set(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']).issubset(dayList):
        day = 'All Day'

    plt.title(f'{dateList[0]}~{dateList[-1]} (Weekend)Use & Prediction Over Time', fontsize=15)
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

    plt.show()
