from utils.backtest_engine import BackTestSA
from utils.logger import MyLogger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

# instance of MyLogger, add False as last param to disable.
log = MyLogger('../data/results/logfile.txt', "TWCBull.py", True)

class TWCBull(BackTestSA):
    def __init__(self, csv_path, date_col):
        super().__init__(csv_path, date_col)

    target_close = 0

    def generate_signals(self):
        df = self.dmgt.df

        df['timestamp'] = df.index

        df['longs'] = ((df.close > df.close.shift(1)) & (
                    df.low.shift(1) > df.low.shift(2))) * 1
        df['shorts'] = ((df.close < df.close.shift(1)) & (
                    df.close.shift(1) < df.close.shift(2))) * -1
        df['entry'] = df.shorts + df.longs

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1 and not self.open_pos:
                # Populating class variables if long entry
                self.stop_price = row.low - 2
                self.timestamp = row.timestamp
                self.open_long(row.t_plus)
                self.target_close = row.close
            elif self.open_pos:
                if row.close > self.target_close:
                    self.target_close = row.close
                    self.stop_price = row.low - 2
                    self.add_zeros()
                else:
                    self.monitor_open_positions(row.close, row.timestamp)
            else:
                self.add_zeros()  # if entry == 0 add zeros()
        self.add_trade_cols()

    def monitor_open_positions(self, price, timestamp):
        # check for long stop-loss breach
        if price <= self.stop_price:
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
    csv_path = "../data/test_data/TWC/cleaned_btc_weekly.csv"
    date_col = 'timestamp'

    twc = TWCBull(csv_path, date_col)
    twc.dmgt.change_resolution("1W")
    twc.run_backtest()
    twc.show_performace()
    # print to terminal how many trades executed
    print(abs(twc.dmgt.df.direction).sum())

    # uncomment if you wish to save the backtest to folder
    twc.save_backtest("v1_btc_2022")

