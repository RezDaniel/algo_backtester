import pandas as pd
import pytz


def convert_timezone():
    # Load the data
    df = pd.read_csv('../../data/clean_data/cleaned_btc_2023.csv')

    # Convert the 'timestamp' column to datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')

    # Set 'timestamp' as the index
    df.set_index('timestamp', inplace=True)

    # Convert the index to timezone-aware datetime index (in UTC)
    df.index = df.index.tz_localize('UTC')

    # Convert the timezone to UTC-8
    df.index = df.index.tz_convert('Etc/GMT+8')

    # Write the dataframe to a new CSV file
    df.to_csv('cleaned_btc_exchange_time_2023.csv', index=True)

    print("Successfully written to test_data_exchange_time.csv")


if __name__ == "__main__":
    convert_timezone()
