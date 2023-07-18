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
    def __init__(self, csv_path, date_col, max_holding):
        super().__init__(csv_path, date_col, max_holding)

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
    csv_path = "data/clean_data/btc_jan2023_with_sigbar_orders.csv"
    date_col = 'timestamp'
    max_holding = 1000000000000

    srs = SRS(csv_path, date_col, max_holding)

    #srs.dmgt.change_resolution("1min")

    srs.run_backtest()
    srs.show_performance()
    # 1049 trades with fixed stops and targets 981
    print(abs(srs.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    srs.save_backtest("btc")
