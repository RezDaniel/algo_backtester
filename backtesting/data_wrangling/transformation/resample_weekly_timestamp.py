import pandas as pd


def weekly_timestamp():
    # Load the data
    df = pd.read_csv('data/clean_data/cleaned_btc.csv')

    # Drop all columns except 'timestamp'
    df = df[['timestamp']]

    # Convert the 'timestamp' column to datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'],
                                     format='%Y-%m-%d %H:%M:%S')

    # Set 'timestamp' as the index
    df.set_index('timestamp', inplace=True)

    # Resample to weekly frequency, keeping only the Mondays
    df_resampled = df.resample('W-MON').first()

    # Reset the index to convert the datetime back to a column
    df_resampled.reset_index(inplace=True)

    # Write resampled dataframe to a new CSV file
    df_resampled.to_csv('data/test_data/TWC/cleaned_btc_weekly.csv',
                        index=False)

    print("Successfully written to weekly_timestamps.csv")


if __name__ == "__main__":
    weekly_timestamp()
