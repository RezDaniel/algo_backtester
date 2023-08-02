import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from backtest_engine import BackTestSA


class MovingAverageStrategy(BackTestSA):

    def __init__(self, csv_path, date_col):
        super().__init__(csv_path, date_col)

    def generate_signals(self):

        df = self.dmgt.df

        df['ma_20'] = df.close.rolling(20).mean()
        df['ma_50'] = df.close.rolling(50).mean()

        df['ma_diff'] = df.ma_20 - df.ma_50

        df['longs'] = ((df.ma_diff > 0) & (df.ma_diff.shift(1) < 0))*1
        df['shorts'] = ((df.ma_diff < 0) & (df.ma_diff.shift(1) > 0)) * -1

        df['entry'] = df.longs + df.shorts

    def show_performance(self):
        rets = np.array(self.returns_series)

        cum_rets = rets.cumsum()

        plt.plot(cum_rets)
        plt.show()


if __name__ == '__main__':
    csv_path = '../data/test_data/RipVanWinkle/cleaned_btc_4hr.csv'
    date_col = 'timestamp'

    m = MovingAverageStrategy(csv_path, date_col)

    m.run_backtest()
    m.show_performance()
    # print to terminal how many trades executed
    print(abs(m.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    m.save_backtest("btc")