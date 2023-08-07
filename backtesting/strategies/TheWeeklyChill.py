from utils.backtest_engine import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time


class TWC(BackTestSA):
    def __init__(self, csv_path, date_col):
        super().__init__(csv_path, date_col)

    target_close = 0
    target_high = 0
    target_low = 0

    def update_target_vars(self, high, low, close):
        self.target_high = high
        self.target_low = low
        self.target_close = close

    def generate_signals(self):
        df = self.dmgt.df

        df['longs'] = ((df.close > df.close.shift(1)) & (
                    df.low.shift(1) > df.low.shift(2))) * 1
        df['shorts'] = ((df.close < df.close.shift(1)) & (
                    df.close.shift(1) < df.close.shift(2))) * -1
        df['entry'] = df.shorts + df.longs
        df.dropna(inplace=True)

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1 and self.direction == 0 and not self.open_pos:
                # Populating class variables if long entry
                self.stop_price = row.low - 2
                self.timestamp = row.index
                self.open_long(row.t_plus)
                self.update_target_vars(row.high, row.low, row.close)
            elif row.entry == -1 and self.direction == 0 and not self.open_pos:
                # Populating class variables if long entry
                self.stop_price = row.high + 2
                self.timestamp = row.index
                self.open_short(row.t_plus)
                self.update_target_vars(row.high, row.low, row.close)
            elif self.open_pos:
                if row.close > self.target_close and self.direction == 1:
                    self.update_target_vars(row.high, row.low, row.close)
                    self.stop_price = row.low
                elif row.close < self.target_close and self.direction == -1:
                    self.update_target_vars(row.high, row.low, row.close)
                    self.stop_price = row.high
                self.monitor_open_positions(row.close, row.index)
            else:
                self.add_zeros()  # if entry == 0 add zeros()
        self.add_trade_cols()

    def monitor_open_positions(self, price, timestamp):
        # check for long stop-loss breach
        if price <= self.stop_price and self.direction == 1:
            self.timestamp = timestamp
            self.close_position(price)
        # check for short stop-loss breach
        elif price >= self.stop_price and self.direction == -1:
            self.timestamp = timestamp
            self.close_position(price)
        # if all above conditions not true, append a zero to returns column
        else:
            self.add_zeros()

    def show_performace(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()


if __name__ == '__main__':
    csv_path = "../data/clean_data/cleaned_btc_2018.csv"
    date_col = 'timestamp'

    twc = TWC(csv_path, date_col)
    twc.dmgt.change_resolution("10080min")
    twc.run_backtest()
    twc.show_performace()
    # print to terminal how many trades executed
    print(abs(twc.dmgt.df.direction).sum())

    # uncomment if you wish to save the backtest to folder
    twc.save_backtest("v1_btc_2018")

