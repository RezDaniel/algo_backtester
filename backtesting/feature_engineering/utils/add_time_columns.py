# add_time_columns.py
import pandas as pd
import pytz


def add_time_cols(df):
    """
    Convert Unix time index col to New York datetime and London datetime
    and store the result in the DataFrame.

    :param df: DataFrame with Unix timestamp as the index
    :return: DataFrame with added 'time_london' and 'time_newyork' columns
    """
    # Localize the Unix timestamp to the Bangkok timezone
    bangkok_timezone = pytz.timezone('Asia/Bangkok')
    localized_time = pd.to_datetime(df.index, unit='s').tz_localize(bangkok_timezone)

    # Convert localized Unix timestamp to New York timezone
    ny_timezone = pytz.timezone('America/New_York')
    df['time_newyork'] = localized_time.tz_convert(ny_timezone)

    # Convert localized Unix timestamp to London timezone
    ldn_timezone = pytz.timezone('Europe/London')
    df['time_london'] = localized_time.tz_convert(ldn_timezone)

    # If 'timestamp' column is not the DataFrame index, drop it
    if 'timestamp' in df.columns:
        df.drop(columns=['timestamp'], inplace=True)

    # Rearrange columns
    df = df[
        ['time_london', 'time_newyork', 'volume', 'open', 'low', 'high', 'close']]

    return df


def main():
    csv_path = '../../data/clean_data/cleaned_btc.csv'
    date_col = 'timestamp'

    data = pd.read_csv(csv_path, parse_dates=[date_col], index_col=date_col)
    data.dropna(inplace=True)

    df_with_time_cols = add_time_cols(data)

    # Save the updated DataFrame back to the CSV file
    df_with_time_cols.to_csv('../../data/clean_data/cleaned_btc_timecols.csv',
                             date_format='%m/%d/%Y %H:%M', index=True)


if __name__ == "__main__":
    main()
