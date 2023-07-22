# __main.py__
from feature_engineering import data_wrangling as ds
from feature_engineering.feature_creation import DataManager as dmgt
from feature_engineering import feature_selection as fs

# start_date = '2019-01-01 00:00:00'
# end_date = '2019-01-31 23:59:59'
# sliced_df = ds.slice_data('data/clean_data/cleaned_btc',
#                           start_date, end_date)

csv_path = 'data/test_data/cleaned_btc_jan23.csv'
date_col = 'timestamp'
output_csv = 'data/test_data/test_sigbar_on_index.csv'
fs.generate_sigtime_orders(csv_path, date_col, output_csv)

