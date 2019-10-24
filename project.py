import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! Please enter all options in lowercase letters.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # used stackoverflow for assistance, see note 1 in readme.txt
    city = ' '
    while city not in ('chicago', 'new york city', 'washington'):
        city = input('Which city would you like to explore? Please enter chicago, new york city, or washington: ')
        if city not in ('chicago', 'new york city', 'washington'):
            print("I\'m sorry, that was not one of the options. Please enter the city again.")

    # get user input for month (all, january, february, ... , june)
    month = ' '
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input('What month would you like to see? Please enter any month between january and june, or enter all to see all months: ')
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print ("I\'m sorry, that was not one of the options. Please enter a month again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ' '
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input('What day would you like to see? Please enter any day of the week or all to see all days: ')
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("I\'m sorry, that was not one of the options. Please enter a day aagain.")
    print('-'*40)
    return city, month, day

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
    #used solution from problem sets because the code was more efficient than my solution
    df = pd.read_csv(CITY_DATA[city])

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
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_list = ['January', 'February', 'March', 'April', 'May','June']
    print('Most Popular Month: ', month_list[int(popular_month)-1])
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day: ', popular_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts()
    start_station_max = start_station.max()
    start_station_list =[]
    for i in range((len(start_station.values))):
        if start_station.values[i] == start_station_max:
            start_station_list.append(start_station.index[i])
    print('Popular Start Station: ',start_station_list)

    # display most commonly used end station
    end_station = df['End Station'].value_counts()
    end_station_max = end_station.max()
    end_station_list = []
    for i in range((len(end_station.values))):
        if end_station.values[i] == end_station_max:
            end_station_list.append(end_station.index[i])
    print('Popular End Station: ', end_station_list)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + '-' + df['End Station']
    combo_values = df['combo'].value_counts()
    combo_values_max = combo_values.max()
    combo_values_list = []
    for i in range((len(combo_values.values))):
        if combo_values.values[i] == combo_values_max:
            combo_values_list.append(combo_values.index[i])
    print('Popular Station Combo: ', combo_values_list)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    #used geeksforgeeks for assistance, see note 2 in readme.txt
    start_time = time.time()
    total_time = df['Trip Duration'].sum()
    min, sec = divmod(total_time, 60)
    hour, min = divmod(min, 60)
    print('Total Trip Duration: {} hours, {} minutes, and {} seconds.'.format(int(hour),int(min),int(sec)))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    min, sec = divmod(mean_time, 60)
    hour, min = divmod(min, 60)
    print('Mean Trip Duration: {} hours, {} minutes, and {} seconds.'.format(int(hour),int(min),int(sec)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print ('{}s: {}\n{}s: {}'.format(user_counts.index[0], user_counts.values[0], user_counts.index[1], user_counts.values[1]))

    # Display counts of gender
    #accounts for some data sets missing gender and birth year data
    try:
        gender_counts = df['Gender'].value_counts()
        print ('{} users: {}\n{} users: {}'.format(gender_counts.index[0], gender_counts.values[0], gender_counts.index[1], gender_counts.values[1]))
    except KeyError:
        print('No Gender Data')
    # Display earliest, most recent, and most common year of birth
    try:
        print('Earliest Birthday Year: ',int(df['Birth Year'].min()))
        print('Most Recent Birthday Year: ',int(df['Birth Year'].max()))
        print('Most Common Birthday Year: ',int(df['Birth Year'].mode()))
    except KeyError:
        print('No Birth Year Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data in sets of five.  Allows the user to determine if they want to continue to see raw data sets or exit."""
    #used stackoverflow for assistance, see note 3 in readme.txt
    #drops data that was created during the program
    df.drop(['month','day_of_week','hour','combo'], axis=1,inplace=True)
    #set iterator to 0
    i = 0
    #prompts user for input
    x = input('Would you like to see the raw data? Please enter yes or no: ')
    #establishes repetitive loop
    while True:
        #checks user input and prompts them to enter again if incorrect data is displayed
        if x == 'yes':
            while x == 'yes':
                #used stackoverflow for assistance, see note 4 in readme.txt
                print(df.iloc[i,:])
                print(df.iloc[i+1,:])
                print(df.iloc[i+2,:])
                print(df.iloc[i+3,:])
                print(df.iloc[i+4,:])
                i += 5
                x = input('Would you like to see more data? Please enter yes or no: ')
                if x == 'yes':
                    break
                elif x == 'no':
                    return
                else:
                    print('I\'m sorry, that was not one of the options.')
                    x = input('Would you like to see more data? Please enter yes or no: ')


        elif x == 'no':
            return
        elif x != 'yes' or 'no':
            print('I\'m sorry that was not one of the options')
            x = input('Would you like to see the raw data? Please enter yes or no: ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
