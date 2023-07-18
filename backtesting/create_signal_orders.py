from datetime import datetime as dt
from backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from logger import MyLogger


#logging.disable(logging.CRITICAL)  # uncomment to disable all loggers

# instance of MyLogger, add False as last param to disable.
log = MyLogger('../logfile.txt', "SRS141.py")


class SRS(BackTestSA):
    def __init__(self, csv_path, date_col, max_holding, lookback):
        super().__init__(csv_path, date_col, max_holding)

        # lookbacks
        self.lookback = lookback  # 60min

    def generate_orders(self):
        df = self.dmgt.df

        df['sig_long'] = df.high.rolling(self.lookback).max()
        df['sig_short'] = df.low.rolling(self.lookback).min()

        signal_df = pd.DataFrame(index=df.index,
                                 columns=['long_ord', 'short_ord']).fillna(0)
        long_ord_price, short_ord_price = 0, 0
        long_sig_flag, short_sig_flag = 0, 0

        for row in self.dmgt.df.itertuples():
            if row.sigtime == 0 and short_sig_flag == long_sig_flag == 0:
                signal_df.loc[row.Index] = [0, 0]
            elif row.sigtime == 1:
                long_ord_price, short_ord_price = row.sig_long + 2, \
                                                  row.sig_short - 2
                signal_df.loc[row.Index] = [long_ord_price, short_ord_price]
                long_sig_flag = short_sig_flag = 1
            elif row.sigtime == 0 and (short_sig_flag or long_sig_flag):
                signal_df.loc[row.Index, ['short_ord', 'long_ord']] = [
                    short_ord_price, long_ord_price]

        # Merge the two dataframes and asign to datamanager df
        merged_df = self.dmgt.df.join(signal_df, how='outer')
        merged_df[['short_ord', 'long_ord']] = merged_df[
            ['short_ord', 'long_ord']].ffill().bfill()
        self.dmgt.df = merged_df

    def generate_signals(self):
        df = self.dmgt.df

        df['longs'] = (df.high > df.low) * 1
        df['shorts'] = (df.low < df.high) * -1
        df['entry'] = df.shorts + df.longs
        df.dropna(inplace=True)

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1:
                # adding logic for dynamic barriers
                if not self.open_pos:
                    self.open_long(row.t_plus)
                else:
                    self.target_price = self.target_price * self.ub_mult
                    self.max_holding = self.max_holding + int(
                        (self.max_holding_limit / 3))
                    self.add_zeros()
            elif row.entry == -1:
                # adding logic for dynamic barriers
                if not self.open_pos:
                    self.open_short(row.t_plus)
                else:
                    self.target_price = self.target_price * self.lb_mult
                    self.max_holding = self.max_holding + int(
                        (self.max_holding_limit / 3))
                    self.add_zeros()
            elif self.open_pos:
                self.monitor_open_positions(row.close, row.Index)
            else:
                self.add_zeros()

        self.add_trade_cols()

    def show_performance(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()


if __name__ == '__main__':
    csv_path = "data/clean_data/btc_jan2023.csv"
    #csv_path = "data/clean_data/btc_jan2023_with_sigbar_orders.csv"
    date_col = 'timestamp'
    max_holding = 1000000000000
    lookback = 60 * 24

    srs = SRS(csv_path, date_col, max_holding, lookback)

    srs.dmgt.change_resolution("1min")

    srs.dmgt.set_sigtime(0, 1)
    srs.dmgt.generate_orders()  # After run change csv_path

    #srs.run_backtest()
    #srs.show_performance()
    # 1049 trades with fixed stops and targets 981
    #print(abs(srs.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    #srs.save_backtest("btc")
