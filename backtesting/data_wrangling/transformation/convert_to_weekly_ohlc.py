import pandas as pd
import numpy as np


def custom_resampler(array_like):
    if len(array_like) > 8:
        if array_like.name == 'open':
            return array_like[8:].iloc[0]
        elif array_like.name == 'high':
            return array_like[8:-1].max()
        elif array_like.name == 'low':
            return array_like[8:-1].min()
        elif array_like.name == 'close':
            return array_like[:-1].iloc[-1]
    else:
        return np.nan

def main():
    # Load the data
    df = pd.read_csv('../../data/test_data/TWC/test_data.csv')

    # Convert the 'timestamp' column to datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set 'timestamp' as the index
    df.set_index('timestamp', inplace=True)

    # Shift time by 8 hours
    df.index = df.index - pd.Timedelta(hours=8)

    # Resample to weekly frequency, using the custom resampling function
    df_resampled = df.resample('W-MON').apply(custom_resampler)

    # Shift time back by 8 hours
    df_resampled.index = df_resampled.index + pd.Timedelta(hours=8)

    # Write resampled dataframe to a new CSV file
    df_resampled.to_csv('../../data/test_data/TWC/weekly_OHLC.csv', index=True)

    print("Successfully written to weekly_OHLC.csv")


if __name__ == "__main__":
    main()
