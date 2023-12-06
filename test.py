def date_Range_Settings():
    # List to store the generated date range
    date_range = []

    while True:
        start_date = input("Start date for Train [MMDD] : ")
        end_date = input("End Date for Train   [MMDD] : ")
        # Check if the start_date and end_date are valid and in the correct order
        if is_valid(start_date) and is_valid(end_date) and start_date <= end_date:
            # Generate the date range
            date_range = generate_range(start_date, end_date)
            filename_list = convert_to_filename_format(date_range)
            print(filename_list)
            print(len(filename_list))

            return filename_list
        else:
            print("Invalid Date Format or Start date is not before End date. Please try again.\n")
            continue  # Go back to the beginning of the loop
def is_valid(input_date):
    # Check if the input date has a valid format
    if len(input_date) != 4:
        return False

    # Extract month and day
    month, day = int(input_date[:2]), int(input_date[2:])

    # Check if it's a valid date
    if 1 <= month <= 12 and 1 <= day <= 31:
        if (month == 2 and day <= 28) or \
                (month in {1, 3, 5, 7, 8, 10, 12} and day <= 31) or \
                (month in {4, 6, 9, 11} and day <= 30):
            return True

    # If it's an invalid date format
    return False
def generate_range(start_date, end_date):
    # List to store the generated date range
    date_range = []

    current_date = start_date
    while current_date <= end_date:
        # Append the current date to the date range list
        date_range.append(current_date)
        # Increment the date to the next day
        current_date = increment_date(current_date)
        if current_date == end_date:
            date_range.append(end_date)
            break  # Break the loop when current_date reaches end_date

    return date_range
def increment_date(date):
    # Increment the date by one day
    month, day = int(date[:2]), int(date[2:])

    # Check if it's the last day of the month
    if  (month == 2 and day == 28) or \
        (month in {1, 3, 5, 7, 8, 10, 12} and day == 31) or \
        (month in {4, 6, 9, 11} and day == 30):
        # Check if it's December 31st
        if month == 12 and day == 31:
            # Return the current date without moving to the next year
            return f"{month:02d}{day:02d}"
        else:
            # Move to the first day of the next month
            month = (month % 12) + 1
            day = 1
    else:
        # Increment the day
        day += 1

    # Convert the date to a string and return
    return f"{month:02d}{day:02d}"
def convert_to_filename_format(date_range):
    # List to store the converted date format
    filename_list = []

    for date in date_range:
        # Extract month from the date
        month = date[:2]

        # Convert date format from MMDD to YYYYMMDD (using the fixed year)
        filename_format = f"tpss_bcycl_od_statnhm_2022/tpss_bcycl_od_statnhm_2022{month}/tpss_bcycl_od_statnhm_2022{date}.csv"

        filename_list.append(filename_format)

    return filename_list


