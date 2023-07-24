from datetime import datetime as dt
from backtest_engine import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from logger import MyLogger

#logging.disable(logging.CRITICAL)  # uncomment to disable all loggers

# instance of MyLogger, add False as last param to disable.
log = MyLogger('../data/results/logfile.log', "BTCMC3.py", True)


class BTCMC3(BackTestSA):
    def __init__(self, csv_path, date_col):
        super().__init__(csv_path, date_col)

    def generate_signals(self):
        df = self.dmgt.df

        df['longs'] = (df.open >= df.long_ord) * 1
        df['shorts'] = (df.open <= df.short_ord) * -1
        df['entry'] = df.shorts + df.longs
        df.dropna(inplace=True)

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.sigtime == 1:
                self.entry_count = 0
                log.logger.info("    sigtime")
            if row.entry == 1 and row.long_ord != 0:
                # Populating class variables if long entry
                if not self.open_pos and self.entry_count < 1:
                    self.stop_price = row.short_ord
                    self.target_price = (row.long_ord + (
                                row.long_ord - row.short_ord)) * self.long_mult
                    self.open_long(row.t_plus)
                else:
                    self.add_zeros()
            elif row.entry == -1 and row.short_ord != 0:
                # Populating class variables if short entry
                if not self.open_pos and self.entry_count < 1:
                    self.stop_price = row.long_ord
                    self.target_price = (row.short_ord - (
                                row.long_ord - row.short_ord)) * self.short_mult
                    self.open_short(row.t_plus)
                else:
                    self.add_zeros()
            elif self.open_pos:
                self.monitor_open_positions(row.close, row.Index)
            else:
                self.add_zeros()  # if entry == 0 add zeros()
        self.add_trade_cols()

    def show_performance(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        plt.title(f"Strategy results for {self.dmgt.timeframe} timeframe")
        plt.show()


if __name__ == '__main__':
    csv_path = "../data/test_data/BTCMC/final_test/orders_ny.csv"
    date_col = 'timestamp'

    mc = BTCMC3(csv_path, date_col)
    mc.run_backtest()
    mc.show_performance()
    # print to terminal how many trades executed
    print(abs(mc.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    mc.save_backtest("btc")
