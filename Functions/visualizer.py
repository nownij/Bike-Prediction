from Functions import dataProcessor as DtPR
import matplotlib.pyplot as plt

def show_dataframe(date_range, dataframe):
    start_date = date_range[0]
    end_date = date_range[-1]

    # Create Figure and AxesSubplot
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # First subplot: Number of uses
    axs[0].plot(dataframe['HHMM'], dataframe['Use'], 'b-', label='Number of uses')
    axs[0].set_title('Number of uses')
    axs[0].set_xlabel('HH')
    axs[0].set_ylabel('Values')
    axs[0].legend()

    # Second subplot: Total usage minutes
    axs[1].plot(dataframe['HHMM'], dataframe['Minute[min]'], 'r-', label='Total usage minutes')
    axs[1].set_title('Total usage minutes')
    axs[1].set_xlabel('HH')
    axs[1].set_ylabel('Values')
    axs[1].legend()

    # Third subplot: Total usage distance
    axs[2].plot(dataframe['HHMM'], dataframe['Distance[m]'], 'g-', label='Total usage distance')
    axs[2].set_title('Total usage distance')
    axs[2].set_xlabel('HH')
    axs[2].set_ylabel('Values')
    axs[2].legend()

    # Adjust layout
    plt.tight_layout()

    # Change x-axis ticks
    for ax in axs:
        ax.set_xticks(range(0, 2400, 100))
        ax.set_xticklabels(['{:02d}'.format(h) for h in range(0, 24)])

    # Set the graph title
    plt.suptitle(f'{start_date}~{end_date}', fontsize=16)

    # Adjust height
    plt.subplots_adjust(top=0.9)

    # Show the graph
    plt.show()
def show_df(dateList, df_list):
    for i, df in enumerate(df_list):  # Use enumerate to get both index and DataFrame
        plt.figure(figsize=(10, 6))
        plt.plot(df['HHMM'], df['Use'], linestyle='-', color='b')


        plt.xlabel('HHMM')
        plt.ylabel('Use')
        plt.title(f'{dateList[i]} HHMM : Use')

        plt.ylim(0, 100)
        plt.grid(True)

        plt.savefig(f'Data/graph/plot_{i}.png')