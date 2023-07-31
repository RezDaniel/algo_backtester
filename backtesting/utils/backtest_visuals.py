# backtest_visuals.py
from matplotlib.backends.backend_pdf import PdfPages
import animations
import plots
import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d


class DataLoader:
    """
    Original CSV file needs to just have two columns, 'timestamp' and 'results'
    the timestamp column can be a datetime and the results values are int 1 for
    a win and int -1 for a losing trade.
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def load_csv(self):
        df = pd.read_csv(self.filepath)
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df

    def slice_data(self, df, start_date, end_date):
        mask = (df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)
        sliced_df = df.loc[mask].reset_index(drop=True)
        return sliced_df

    def _clean_and_reshape(self, df):
        reshaped_data = []
        for i in range(0, df.shape[1], 2):
            month = df.iloc[:, i]
            returns = df.iloc[:, i+1]
            is_valid = ~np.isnan(returns)
            month = month[is_valid]
            returns = returns[is_valid]
            if len(month) == 0 or len(returns) == 0:
                continue
            temp_df = pd.concat([month, returns], axis=1)
            temp_df.columns = ['timestamp', 'returns']
            reshaped_data.append(temp_df)
        reshaped_df = pd.concat(reshaped_data)
        reshaped_df = reshaped_df.sort_values('timestamp').reset_index(drop=True)
        return reshaped_df


if __name__ == '__main__':
    # Create an instance of DataLoader, replace with your actual file path
    loader = DataLoader(
        'backtesting/data/results/VW141/SRS141_backtest_results.csv')

    # Load the data
    df = loader.load_csv()

    # Slice the data
    start_date = '2022-09-24'  # uncomment to focus on worst drawdown periods
    end_date = '2022-12-31'
    df = loader.slice_data(df, start_date, end_date)

    # convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Call the visualisations functions
    with PdfPages('backtesting/data/results/VW141/vw141_backtest_result_plots.pdf') as pdf_pages:
        plots.cumulative_returns_per_trade(df, pdf_pages)
        plots.monthly_cumulative_returns(df, pdf_pages)
        plots.win_loss_pie_chart(df, pdf_pages)
        plots.win_loss_ratio(df, pdf_pages)
        plots.drawdown_lengths(df, pdf_pages)
        plots.win_loss_heatmap(df, pdf_pages)
        plots.density_plots(df, pdf_pages)

        #plots.cumulative_wins_3d(df, pdf_pages)
        #plots.monthly_win_loss_bar(df, pdf_pages)
        #plots.box_plots_by_month(df, pdf_pages)
        #plots.win_loss_scatter_plot(df, pdf_pages)

    # Call the animated functions
    animations.win_loss_ratio_animation(df)
    animations.cum_returns_per_trade_animation(df)

    #visualisations.win_loss_scatter_plot_animation(df)
