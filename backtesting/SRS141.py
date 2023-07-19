from datetime import datetime as dt
from backtest import BackTestSA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from logger import MyLogger

#logging.disable(logging.CRITICAL)  # uncomment to disable all loggers

# instance of MyLogger, add False as last param to disable.
log = MyLogger('data/strategy_results/logfile.txt', "SRS141.py", True)


class SRS(BackTestSA):
    def __init__(self, csv_path, date_col, max_holding):
        super().__init__(csv_path, date_col, max_holding)

    def generate_signals(self):
        df = self.dmgt.df

        df['longs'] = (df.open >= df.long_ord) * 1
        df['shorts'] = (df.open <= df.short_ord) * -1
        df['entry'] = df.shorts + df.longs
        df.dropna(inplace=True)

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            if row.entry == 1 and row.long_ord != 0:
                # Populating class variables if long entry
                if not self.open_pos:
                    self.open_long(row.t_plus)
                    self.stop_price = row.short_ord
                    self.target_price = row.long_ord + (row.long_ord - row.short_ord)
                else:
                    self.add_zeros()

            elif row.entry == -1 and row.short_ord != 0:
                # Populating class variables if short entry
                if not self.open_pos:
                    self.open_short(row.t_plus)
                    self.stop_price = row.long_ord
                    self.target_price = row.short_ord - (row.long_ord - row.short_ord)
                else:
                    self.add_zeros()
            elif self.open_pos:
                self.monitor_open_positions(row.close, row.Index)
                log.logger.info(
                    "t=" + str(row.Index)
                    + " sigt=" + str(row.sigtime)
                    + "  pos=" + str(self.open_pos)
                    + "  ent=" + str(self.entry_price)
                    + "  price=" + str(row.close)
                    + "  dir:" + str(self.direction)
                    + "  TP=" + str(self.target_price)
                    + "  SL=" + str(self.stop_price))
            else:
                self.add_zeros()  # if entry == 0 add zeros()

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
    srs.run_backtest()
    srs.show_performance()
    # 1049 trades with fixed stops and targets 981
    print(abs(srs.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    srs.save_backtest("btc")
