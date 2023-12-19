# visualizer.py
import matplotlib.pyplot as plt

def show_df(period, df_list):
    dateList, dayList = zip(*period)

    for i, df in enumerate(df_list):
        plt.figure(figsize=(10, 6))
        plt.plot(df['HHMM'], df['Use'], linestyle='-', color='b')

        plt.xlabel('HHMM')
        plt.ylabel('Use')
        plt.title(f'{dateList[i]} ({dayList[i]}) HHMM : Use')

        plt.ylim(0, 100)
        plt.grid(True)

        max_value = df['Use'].max()
        max_index = df['Use'].idxmax()
        max_x = df.loc[max_index, 'HHMM']

        plt.text(max_x, max_value, f'Max: ({max_x}, {max_value})', verticalalignment='bottom',
                 horizontalalignment='left', fontsize=10, color='red')

        plt.show()

        # plt.savefig(f'Data/graph/plot_{dateList[i]}.png')
        # print(f"File saved : plot_{dateList[i]}.png")