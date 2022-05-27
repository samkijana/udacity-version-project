import pandas as pd
import numpy as np
import datetime as dt
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Expects:
             Prompts user to provide city, month and day to use for data analysis.
    Returns: (str)
             city name
             month name or "all" for no filter
             day name or "all" for no filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    month_list = ["january", "february", "march", "april", "may", "june"]
    day_list = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    filter_list = ["all", "month", "day"]

    while True:
        city = input("Would you like to see bikeshare data for Chicago, New York, or Washington?: ").lower().strip()

        if city == "" or city not in (CITY_DATA):
            print(f"City entered {city} is not in either Chicago, New York or Washington.")
            continue
        else:
            print(city.title())
            break

    while True:
        data_filter = input(
            "Would you like to filter the data by month, day, or not at all? Type all for no filter. ").lower().strip()
        if data_filter == "" or data_filter not in filter_list:
            print(f"Filter entered {data_filter} is not either month, day or all. ")
            continue
        else:
            print(data_filter.title())
            break

    if data_filter == "all":
        day = "all"
        month = "all"

    if data_filter == "month":
        day = "all"

    if data_filter == "day":
        month = "all"

    if data_filter == "month":
        while True:
            month = input("Which month - January, February, March, April, May, or June? ").lower().strip()
            if month == "" or month not in month_list:
                print(f"Month entered {month} is not either January, February, March, April, May or June.")
                continue
            else:
                print(month.title())
                break

    if data_filter == "day":
        while True:
            day = input(
                "Which day - Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday? ").lower().strip()
            if day == "" or day not in day_list:
                print(
                    f"Day entered {day} is not either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday.")
                continue
            else:
                print(day.title())
                break

    return city, month, day

def load_data(city, month, day):
    """
    Expects:
             city, month and day args
    Returns:
             df - Pandas DataFrame containing city data filtered by month and day
    """
    print(f"Loading data for filter(s) selected.")
    try:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Month Name'] = df['Start Time'].dt.strftime("%B")
        df['Day Name'] = df['Start Time'].dt.strftime('%A')
        df['City'] = city.title()

        if month != "all":
            df = df[df['Month Name'] == month.capitalize()]

        if day != "all":
            df = df[df['Day Name'] == day.capitalize()]
    except Exception as e:
        print(f"Error: {e}")

    return df

def time_stats(df):
    """
    Expects:
             df - Pandas DataFrame containing city data filtered by month and day
    Returns:
             Statistics on the most frequent times of travel
    """
    start_time = time.time()
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Month Name'] = df['Start Time'].dt.strftime("%B")
        df['Day Name'] = df['Start Time'].dt.strftime('%A')
        df['Start Hour'] = df['Start Time'].dt.hour

        print(f"Retrieving statistic for frequent month.")
        common_month = df['Month Name'].mode()[0]
        print(f"Most frequent Month is {common_month}.")
        print(f"This took %s seconds." % (time.time() - start_time))

        print(f"Retrieving statistic for frequent day of the week.")
        common_day = df['Day Name'].mode()[0]
        print(f"Most frequent Day of Week is {common_day}.")
        print(f"This took %s seconds." % (time.time() - start_time))

        print(f"Retrieving statistic for frequent start hour.")
        common_hour = df['Start Hour'].mode()[0]
        print(f"Most frequent Start Hour is {common_hour}.")
        print(f"This took %s seconds." % (time.time() - start_time))
    except Exception as e:
        print(f"Error: {e}")

def station_stats(df):
    """
    Expects:
             df - Pandas DataFrame containing city data filtered by month and day
    Returns:
             Statistics on the most popular stations and trip
    """
    start_time = time.time()
    try:
        print(f"Retrieving statistic for popular start station.")
        common_start_station = df['Start Station'].mode()[0]
        print(f"Popular Start Station is {common_start_station}.")
        print("This took %s seconds." % (time.time() - start_time))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"Retrieving statistic for popular end station.")
        common_end_station = df['End Station'].mode()[0]
        print(f"Popular End Station is {common_end_station}.")
        print("This took %s seconds." % (time.time() - start_time))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"Retrieving statistic for popular start station and end station trip.")
        freq_start, freq_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
        freq_combination = (df[(df['Start Station'] == freq_start) & (df['End Station'] == freq_end)])
        freq_count = len(freq_combination)
        print(f"Popular Start Station: {freq_start} and End Station: {freq_end}.\nNumber of Occurrences: {freq_count}.")
        print("This took %s seconds." % (time.time() - start_time))
    except Exception as e:
        print(f"Error: {e}")

def trip_duration_stats(df):
    """
    Expects:
             df - Pandas DataFrame containing city data filtered by month and day
    Returns:
             Statistics on the total and average trip duration
    """
    start_time = time.time()
    try:
        travel_time = {}
        travel_count = len(df)

        print(f"Retrieving statistics for total travel time and mean travel time.")
        total_travel_time = df.groupby(['City'])['Trip Duration'].sum()
        for city_total, time_total in total_travel_time.items():
            travel_time["Total Travel Time"] = time_total
        total_time = travel_time["Total Travel Time"]

        mean_travel_time = df.groupby(['City'])['Trip Duration'].mean()
        for city_mean, time_mean in mean_travel_time.items():
            travel_time["Mean Travel Time"] = time_mean
        mean_time = travel_time["Mean Travel Time"]

        print(f"Total Travel Time: {total_time}, Mean Travel Time: {mean_time:.2f}, Count: {travel_count}.")
        print("This took %s seconds." % (time.time() - start_time))
    except Exception as e:
        print(f"Error: {e}")

def user_stats(df):
    """
    Expects:
             df - Pandas DataFrame containing city data filtered by month and day
    Returns:
             Statistics on bikeshare users
    """
    start_time = time.time()
    try:
        print(f"Retrieving statistics for user types.")
        if "User Type" in df.columns:
            df = df.dropna(subset=["User Type"])
            print(df["User Type"].value_counts().to_frame())
            print("This took %s seconds." % (time.time() - start_time))
        else:
            print(f"No User Type data!")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"Retrieving statistics for gender.")
        if "Gender" in df.columns:
            df = df.dropna(subset=["Gender"])
            print(df["Gender"].value_counts().to_frame())
            print("This took %s seconds." % (time.time() - start_time))
        else:
            print("No Gender data!")
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(f"Retrieving statistics for birth year.")
        if "Birth Year" in df.columns:
            df = df.dropna(subset=["Birth Year"])
            min_year = df["Birth Year"].min()
            max_year = df["Birth Year"].max()
            mode_year = df["Birth Year"].mode()[0]
            print(f"Earliest Year: {int(min_year)}, Recent Year: {int(max_year)}, Common Year: {int(mode_year)}.")
            print("This took %s seconds." % (time.time() - start_time))
        else:
            print("No Birth Year data!")
    except Exception as e:
        print(f"Error: {e}")

def print_rows(df):
    """
    Expects:
             df - Pandas DataFrame containing city data filtered by month and day
             Prompts user if they want to review raw data
    Returns:
             Prints 10 rows of data at a time
    """
    start_time = time.time()
    try:
        index_start = 0
        index_end = 9
        counter = 10

        while True:
            if index_start == 0 and index_end == 9:
                print_rows = input("Would you like to review rows? Type Yes or No. ").lower().strip()
            else:
                print_rows = input("Would you like to review 5 more rows of data? Type Yes or No. ").lower().strip()
            if print_rows == "" or print_rows not in ("yes", "no"):
                print(f"Input entered {print_rows} is not either Yes or No.")
                continue
            if print_rows == "yes":
                print(df.loc[df.index[index_start]:df.index[index_end]])
                index_start += counter
                index_end += counter
            if print_rows == "no":
                break
    except Exception as e:
        print(f"Error: {e}")
    print("\nThis took %s seconds." % (time.time() - start_time))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()