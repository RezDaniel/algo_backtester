# v2, does not reverse trade direction. If there is an opposite signal it will
# wait for one candle.

from utils.backtest_engine import BackTestSA
from utils.logger import MyLogger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

# instance of MyLogger, add False as last param to disable.
log = MyLogger('../data/results/logfile.txt', "TWCBull.py", False)


class TWC(BackTestSA):
    def __init__(self, csv_path, date_col):
        super().__init__(csv_path, date_col)

    target_close = 0

    def generate_signals(self):
        df = self.dmgt.df

        #df['timestamp'] = df.index

        df['longs'] = ((df.close > df.close.shift(1)) & (
                    df.close.shift(1) > df.close.shift(2))) * 1
        df['shorts'] = ((df.close < df.close.shift(1)) & (
                    df.close.shift(1) < df.close.shift(2))) * -1
        df['entry'] = df.shorts + df.longs

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            # log.logger.info(
            #     str(row.timestamp)
            #     + " pos : " + str(self.open_pos)
            #     + " row_close : " + str(int(row.close))
            #     + " target_close : " + str((int(self.target_close)))
            #     + " SL: " + str(int(self.stop_price)))

            if row.entry == 1 and not self.open_pos:
                # Populating class variables if long entry
                self.stop_price = row.low - 2
                self.timestamp = row.index
                self.open_long(row.t_plus)
                self.target_close = row.close
            elif row.entry == -1 and not self.open_pos:
                # Populating class variables if long entry
                self.stop_price = row.high + 2
                self.timestamp = row.index
                self.open_short(row.t_plus)
                self.target_close = row.close
            elif self.open_pos and self.direction == 1:
                # check for stop-loss breach
                if row.low <= self.stop_price:
                    self.timestamp = row.index
                    self.close_position(self.stop_price)
                # check for new target candle
                elif row.close > self.target_close:
                    self.target_close = row.close
                    self.stop_price = row.low - 2
                    self.add_zeros()
                else:
                    self.add_zeros()
            elif self.open_pos and self.direction == -1:
                # check for stop-loss breach
                if row.high >= self.stop_price:
                    self.timestamp = row.index
                    self.close_position(self.stop_price)
                # check for new target candle
                elif row.close < self.target_close:
                    self.target_close = row.close
                    self.stop_price = row.high + 2
                    self.add_zeros()
                else:
                    self.add_zeros()
            else:
                self.add_zeros()  # if entry == 0 add zeros()
        self.add_trade_cols()

    def show_performace(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()


if __name__ == '__main__':
    csv_path = "../data/test_data/TWC/cleaned_btc_1w.csv"
    date_col = 'timestamp'

    twc = TWC(csv_path, date_col)
    twc.run_backtest()
    twc.show_performace()
    # print to terminal how many trades executed
    print(abs(twc.dmgt.df.direction).sum())

    # uncomment if you wish to save the backtest to folder
    twc.save_backtest("v2_btc_2018-2023")

