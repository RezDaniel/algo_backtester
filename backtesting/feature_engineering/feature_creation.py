# features_creation.py
import pandas as pd
import datetime as dt
from logger import MyLogger
import glob


class DataManager:

    def __init__(self, csv_path, date_col):

        self.data = pd.read_csv(csv_path, parse_dates=[date_col],
                                index_col=date_col)

        # instance of MyLogger, add False as last param to disable.
        log = MyLogger('../logfile.txt', "feature_creation.py", False)

        # can use uniform to change this
        self.data['t_plus'] = self.data.open.shift(-1)

        self.data.dropna(inplace=True)

        self.df = self.data.copy()
        self.timeframe = '1min'

    @staticmethod
    def concatenate_csv_files(file_pattern, output_filename):
        """
        Concatenate multiple CSV files into a single DataFrame and save to a
        new CSV file.

        :param file_pattern: File pattern to match the CSV files (e.g.,
        'BTCUSDT-1m-2020-*.csv').
        :param output_filename: Filename to save the concatenated data.
        :return: DataFrame containing the concatenated data.
        """
        # Get a list of all CSV files that match the pattern and sort them
        # based on dates
        csv_files = sorted(glob.glob(file_pattern))

        concatenated_data = pd.DataFrame()

        for file in csv_files:
            data = pd.read_csv(file)
            concatenated_data = pd.concat([concatenated_data, data])

        concatenated_data.to_csv(output_filename, index=False)

        return concatenated_data

    def change_resolution(self, new_timeframe):

        resample_dict = {'volume': 'sum', 'open': 'first',
                         'low': 'min', 'high': 'max',
                         'close': 'last',
                         't_plus': 'last'}

        self.df = self.data.resample(new_timeframe).agg(resample_dict)

        self.timeframe = new_timeframe

    def set_sigtime(self, hours=0, mins=0):
        """
        :param hours: int of the hour bar you want a signal on, defaults to 0
        :param mins: int of the minutes you want a signal on, defaults to 0
        """
        self.df['sigtime'] = self.df.index  # creates a column sigtime
        self.df['sigtime'] = (self.df.index.time == dt.time(hours, mins))\
            .astype(int)

    def generate_orders(self, lookback, buffer, filename):

        self.df['sig_long'] = self.df['high'].rolling(lookback).max()
        self.df['sig_short'] = self.df['low'].rolling(lookback).min()

        signal_df = pd.DataFrame(index=self.df.index,
                                 columns=['long_ord', 'short_ord']).fillna(0)
        long_ord_price, short_ord_price = 0, 0
        long_sig_flag, short_sig_flag = 0, 0

        for row in self.df.itertuples():
            if row.sigtime == 0 and short_sig_flag == long_sig_flag == 0:
                signal_df.loc[row.Index] = [0, 0]
            elif row.sigtime == 1:
                long_ord_price, short_ord_price = row.sig_long + buffer, \
                                                  row.sig_short - buffer
                signal_df.loc[row.Index] = [long_ord_price, short_ord_price]
                long_sig_flag = short_sig_flag = 1
            elif row.sigtime == 0 and (short_sig_flag or long_sig_flag):
                signal_df.loc[row.Index, ['short_ord', 'long_ord']] = [
                    short_ord_price, long_ord_price]

        # Merge the two dataframes and asign to datamanager df

        merged_df = self.df.merge(signal_df, how='left', left_index=True,
                                  right_index=True)
        merged_df[['short_ord', 'long_ord']] = merged_df[
            ['short_ord', 'long_ord']].ffill().bfill()
        merged_df.to_csv(filename)
