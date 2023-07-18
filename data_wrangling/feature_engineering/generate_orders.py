# generate_orders.py
from feature_creation import DataManager


csv_path = "../../backtesting/data/clean_data/btc_jan2023.csv"
date_col = 'timestamp'
lookback = 60
output_filename = "../../backtesting/data/clean_data/btc_jan2023_with_sigbar_orders.csv"

dmgt = DataManager(csv_path, date_col)
# csv_path = "data/clean_data/btc_jan2023_with_sigbar_orders.csv"

#dmgt.change_resolution("1min")
dmgt.set_sigtime(0, 1)
dmgt.generate_orders(lookback, output_filename)





















