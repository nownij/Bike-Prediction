import time
from Functions import dataProcessor, visualizer

if __name__ == "__main__":
    # Step 1: Select Date
    date_range = dataProcessor.select_date()

    # Record Start time
    start_time = time.time()

    # Step 2: Read CSV Files
    original_data = dataProcessor.read_csv_files_in_date_range(date_range)

    # Step 3: Set Columns
    set_col_data = dataProcessor.set_columns(original_data)

    # Step 4: Remove Useless Data
    removed_data = dataProcessor.remove_useless_data(set_col_data)

    # Step 5: Set Target Location : 광진구
    target_data = dataProcessor.set_target_location(removed_data)
    #print(target_data)

    # Step 6: Merge DataFrames
    #final = dataProcessor.merge_dataframes(target_data)

    # Step 7: Visualize Data
    #visualizer.show_dataframe(date_range, final)

    # Measuring Runtime
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program Run Time >> {elapsed_time:.4f} sec")
