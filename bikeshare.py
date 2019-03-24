import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# this filters the data
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n')
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        print("You did not make a valid selection, please try again:\n")
        city=input("Please choose one of the three cities: Chicago, New York City, or Washington:\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Choose a month from January to June, or type all to see data for all months:\n").lower()
    while month not in ["january", "february", "march", "april", "may", "june", "all"]:
        print("You did not make a valid selection, please try again:\n")
        month = input("Choose a month from January to June, or say all to see data for all months:\n").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day =input("Select a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, or all:\n").lower()
    while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "all"]:
        print("You did not make a valid selection, please try again:\n")
        day =input("Select a day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, or all:\n").lower()
    print('-'*40)

    return city, month, day

# get user input
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month of the year is', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week is', common_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour is ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['combined'] = df[['Start Station', 'End Station']].apply(lambda x: ''.join(x), axis=1)
    print('Most frequent combination of start and end station is', df['combined'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is',df['Trip Duration'].sum(), 'seconds')

    # display mean travel time
    print('Mean travel time is',df['Trip Duration'].mean(), 'seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if 'Gender' in df.columns:
    # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print('The distribution of gender is:\n', gender_types)
    else:
        print("Gender information is NOT available for this city")

    if 'Birth Year' in df.columns:
    # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year is:', int(earliest_birth_year))

        recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is:', int(recent_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year is:', int(common_birth_year))
    else:
        print("Birth year information is NOT available for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        counter = 5
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        while raw_data.lower() not in ['yes', 'no']:
            print("Invalid input. Please type 'yes' or 'no'.")
            raw_data = input('\nWould you like to see 5 lines of raw data? Type \'yes\' or \'no\'.\n')
        while raw_data.lower() == 'yes':
            print(df.head(counter))
            raw_data = input('\nWould you like to see the next 5 lines of raw data? Type \'yes\' or \'no\'.\n')
            counter += 5


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ['yes', 'no']:
            print("Invalid input. Please type 'yes' or 'no'.")
            restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
     main()
