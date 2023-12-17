from Functions import dataProcessor, visualizer

if __name__ == "__main__":
    date_range = dataProcessor.select_date()

    original_data = dataProcessor.read_csv_files_in_date_range(date_range)
    #print(original_data)

    set_col_data = dataProcessor.set_columns(original_data)
    #print(set_col_data)

    removed_data = dataProcessor.remove_useless_data(set_col_data)
    #print(removed_data)

    target_data = dataProcessor.set_target_location(removed_data)
    #print(target_data)

    final = dataProcessor.merge_dataFrames(target_data)
    #print(final)

    visualizer.show_dataframe(date_range ,final)
