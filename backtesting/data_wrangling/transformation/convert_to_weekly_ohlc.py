import pandas as pd


def calculate_weekly_ohlc(datafile, output_file):
    # Load the data
    df = pd.read_csv(datafile)

    # Convert 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y/%m/%d %H:%M')
    df.set_index('timestamp', inplace=True)

    # Create new columns for weekly OHLC
    df['weekly_open'] = None
    df['weekly_high'] = None
    df['weekly_low'] = None
    df['weekly_close'] = None

    # Identify rows that have timestamps corresponding to Monday 00:00
    mondays = df[df.index.dayofweek == 0]  # 0 represents Monday in datetime
    mondays = mondays[mondays.index.hour == 0]
    mondays = mondays[mondays.index.minute == 0]

    # Loop through the Mondays and compute the weekly OHLC
    for monday in mondays.index:
        # Adjust to get the next Sunday 23:59
        next_sunday = (monday + pd.DateOffset(days=6)).replace(hour=23,
                                                               minute=59,
                                                               second=0)

        # Get data from the current Monday 00:00 to the next Sunday 23:59
        week_data = df.loc[monday:next_sunday]

        # Assign values to the new columns
        df.at[monday, 'weekly_open'] = week_data['open'].iloc[0]
        df.at[monday, 'weekly_high'] = week_data['high'].max()
        df.at[monday, 'weekly_low'] = week_data['low'].min()
        df.at[monday, 'weekly_close'] = week_data['close'].iloc[-1]

    # Save the updated data to the specified output file
    df.to_csv(output_file)


# Call the function
calculate_weekly_ohlc('cleaned_btc_exchange_time_2023.csv', 'cleaned_btc_1w_2023.csv')
