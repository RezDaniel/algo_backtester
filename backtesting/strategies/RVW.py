import matplotlib.pyplot as plt
from backtest_engine import BackTestSA


class RVW(BackTestSA):

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
        df.dropna(inplace=True)

    def run_backtest(self):
        self.generate_signals()
        for row in self.dmgt.df.itertuples():
            # If there's an entry signal and no open position, open a position
            if row.entry != 0 and not self.open_pos:
                self.open_long(
                    row.t_plus) if row.entry == 1 else self.open_short(
                    row.t_plus)
            # If there's an entry signal and an open position in the opposite
            # direction, close the position
            elif row.entry * self.direction == -1 and self.open_pos:
                current_position_direction = self.direction
                self.close_position(row.close)
                self.reverse_position(row.t_plus, current_position_direction)
            # In all other cases, add zeros
            else:
                self.add_zeros()
        self.add_trade_cols()

    def show_performance(self):
        plt.style.use('ggplot')
        self.dmgt.df.returns.cumsum().plot()
        strat_name = self.__class__.__name__
        tf = self.dmgt.timeframe
        plt.title(f"Strategy results: {strat_name} {tf}")
        plt.show()


if __name__ == '__main__':
    csv_path = '../data/test_data/RipVanWinkle/cleaned_btc_2021.csv'
    date_col = 'timestamp'

    rvw = RVW(csv_path, date_col)

    rvw.run_backtest()
    rvw.show_performance()
    # print to terminal how many trades executed
    print(abs(rvw.dmgt.df.direction).sum())

    # Uncomment if you wish to save the backtest to the folder
    rvw.save_backtest("btc_2021")
