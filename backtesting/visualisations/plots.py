# plots.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.colors as mcolors

# Set Seaborn style and context
sns.set_style('darkgrid')
sns.set_context("talk")


def save_plot(pdf_pages):
    pdf_pages.savefig()
    plt.show(block=True)
    plt.close()


# Helper function to handle common configurations
def plot_common_config(title, xlabel, ylabel, legend=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if legend:
        plt.legend(legend)
    plt.grid(True)
    plt.tight_layout()  # Prevent x-axis label from being cropped
    plt.subplots_adjust(bottom=0.2)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()


def monthly_cumulative_returns(df, pdf_pages):
    df['YearMonth'] = df['timestamp'].dt.to_period('M')
    monthly_returns = df.groupby(['YearMonth'])['returns'].sum()

    # Calculate cumulative return for each month
    cumulative_returns = monthly_returns.cumsum()

    plt.figure(figsize=(12, 6))

    # Convert PeriodIndex to string representation for plotting
    x_labels = cumulative_returns.index.strftime('%b %y')

    # Plot cumulative returns
    plt.plot(x_labels, cumulative_returns, label='Cumulative Return', color='blue', marker='o')

    plot_common_config(f'Monthly Cumulative Return (Total Trades: {len(df)})', 'Month', 'Cumulative Return', ['Cumulative Return'])
    plt.xticks(ha='center')
    save_plot(pdf_pages)
    plt.show()


def cumulative_returns_per_trade(df, pdf_pages):
    df['Cumulative Returns'] = df['returns'].cumsum()

    plt.figure(figsize=(12, 6))

    # Plot cumulative returns per trade
    plt.plot(df.index, df['Cumulative Returns'],
             label='Cumulative Returns per Trade', color='blue', marker='o')

    plot_common_config(f'Cumulative Returns per Trade (Total Trades: {len(df)})', 'Trade Number', 'Cumulative Returns', ['Cumulative Returns per Trade'])
    x_ticks = np.linspace(0, len(df), num=25, dtype=int)
    plt.xticks(x_ticks, ha='center')
    save_plot(pdf_pages)
    plt.show()


def win_loss_pie_chart(df, pdf_pages):
    win_loss_counts = df['returns'].value_counts()
    win_loss_counts.index = ['Win' if i == 1 else 'Loss' for i
                             in win_loss_counts.index]

    win_loss_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140,
                         figsize=(6, 6))
    plt.ylabel('')  # This is to remove the 'None' ylabel.
    plot_common_config('Win/Loss Proportions', '', '')
    save_plot(pdf_pages)
    plt.show()


def drawdown_lengths(df, pdf_pages):
    df['Drawdown'] = (df['returns'] == -1).astype(int)
    drawdowns = (df['Drawdown'].diff() != 0).cumsum()
    drawdowns = drawdowns[df['Drawdown'] == 1].value_counts().values

    total_trades = len(df)

    if not drawdowns.size:
        print("No drawdowns in the data.")
    else:
        bin_heights, bin_borders = \
            np.histogram(drawdowns, bins=range(1, max(drawdowns) + 2),
                         density=False)
        max_frequency = max(bin_heights)
        plt.hist(drawdowns, bins=range(1, max(drawdowns) + 2),
                 align='left', rwidth=0.8)
        plt.yticks(np.arange(0, max_frequency+1, 2))
        # Set x-axis ticks with step size 1
        plt.xticks(np.arange(1, max(drawdowns)+1, 1))
        plot_common_config(f'Histogram of Drawdown Lengths (Total Trades: {total_trades})', 'Consecutive losing trades', 'Frequency')
        save_plot(pdf_pages)
        plt.show()


def monthly_win_loss_bar(df, pdf_pages):
    df['YearMonth'] = df['timestamp'].dt.to_period('M')
    monthly_counts = df.groupby(['YearMonth', 'returns']).size().unstack(
        fill_value=0)
    monthly_counts = monthly_counts[[1, -1]]

    # Convert the index to 'Jan23' format
    monthly_counts.index = monthly_counts.index.strftime('%b %y')

    monthly_counts.plot(kind='bar', stacked=True, figsize=(12, 6),
                        color=['lightblue', 'salmon'])
    plt.xticks(ha='center')
    plot_common_config(f'Monthly Win/Loss Counts (Total Trades: {len(df)})', 'Month', 'Number of Trades')
    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(bottom=0.25)
    save_plot(pdf_pages)
    plt.show()


def win_loss_ratio(df, pdf_pages):
    df['Win'] = (df['returns'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['Cumulative Trades'] = df.index + 1
    df['Win/Loss Ratio'] = df['Cumulative Wins'] / df['Cumulative Trades']

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['timestamp'], df['Win/Loss Ratio'], color=mcolors.to_rgba(
        'blue', alpha=0.8), linewidth=2)

    # Set the date format for the x-axis to "Jan23"
    date_format = mdates.DateFormatter('%b%y')
    ax.xaxis.set_major_formatter(date_format)

    plot_common_config('Win/Loss Ratio Over Time', 'Month', 'Win/Loss Ratio')
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    plt.xticks()  # Rotate x-axis labels for better visibility
    save_plot(pdf_pages)
    plt.show()


def win_loss_heatmap(df, pdf_pages):
    df['Year'] = df['timestamp'].dt.year
    df['Month'] = df['timestamp'].dt.strftime('%b')  # Format month as 'Jan'
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec']
    df['Month'] = pd.Categorical(df['Month'], categories=months_order,
                                 ordered=True)
    heatmap_data = df.groupby(['Year', 'Month'])['returns'].sum().unstack()

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='coolwarm', center=0)
    plot_common_config('Win/Loss Heatmap by Month', '', '')
    save_plot(pdf_pages)
    plt.show()


def box_plots_by_month(df, pdf_pages):
    df['Month'] = df['timestamp'].dt.month
    df.boxplot(column='returns', by='Month', grid=False, figsize=(12, 6),
               color=dict(boxes='skyblue', whiskers='black', medians='red',
                          caps='black'))
    plt.suptitle('', fontsize=12)  # remove auto-generated title
    plot_common_config('Box Plots of Win/Loss by Month', '', '')
    save_plot(pdf_pages)
    plt.show()


def density_plots(df, pdf_pages):
    # Define losing streaks
    df['Drawdown'] = (df['returns'] == -1).astype(int)
    losing_streaks = (df['Drawdown'].diff() != 0).cumsum()
    losing_streaks = losing_streaks[df['Drawdown'] == 1].value_counts().values

    plt.figure(figsize=(12, 6))
    sns.kdeplot(losing_streaks, fill=True, color='salmon')
    plot_common_config('Density Plot of Losing Streak Lengths', 'Streak Length', '')
    save_plot(pdf_pages)
    plt.show()

    # Define winning streaks
    df['Winning'] = (df['returns'] == 1).astype(int)
    winning_streaks = (df['Winning'].diff() != 0).cumsum()
    winning_streaks = winning_streaks[df['Winning'] == 1].value_counts().values

    plt.figure(figsize=(12, 6))
    sns.kdeplot(winning_streaks, fill=True, color='skyblue')
    plot_common_config('Density Plot of Winning Streak Lengths', 'Streak Length', '')
    save_plot(pdf_pages)
    plt.show()


def cumulative_wins_3d(df, pdf_pages):
    df['Win'] = (df['returns'] == 1).astype(int)
    df['Cumulative Wins'] = df['Win'].cumsum()
    df['TradeNumber'] = range(1, len(df) + 1)
    df['DateNumerical'] = df['timestamp'].apply(lambda date: date.toordinal())

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(df['TradeNumber'], df['DateNumerical'], df['Cumulative Wins'],
            color='skyblue', linewidth=2)
    ax.set_xlabel('Trade Number')
    date_ticks = ax.get_yticks()
    ax.set_yticklabels([datetime.fromordinal(int(date_tick)).date() for
                        date_tick in date_ticks], fontsize=12)
    ax.set_ylabel('timestamp')
    ax.set_zlabel('Cumulative Wins')
    plt.title('3D Plot of Cumulative Wins Over Time')
    plt.tight_layout()  # Prevent x-axis label from being cropped
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    save_plot(pdf_pages)
    plt.show()


def win_loss_scatter_plot(df, pdf_pages):
    df['TradeNumber'] = range(1, len(df) + 1)  # add trade number for x-axis

    plt.figure(figsize=(12, 6))
    plt.scatter(df['TradeNumber'], df['returns'], c=df['returns'], cmap='bwr',
                alpha=0.5)
    plt.plot(df['TradeNumber'], df['returns'], color='black', linewidth=0.5,
             alpha=0.5)  # added line plot
    plt.yticks([0, 1])  # set yticks to just 1 or 0
    plot_common_config('Win/Loss Scatter Plot', 'Trade Number', 'returns')
    save_plot(pdf_pages)
    plt.show()


