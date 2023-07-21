from feature_engineering import cleaning
from feature_engineering.feature_creation import DataManager as dmgt
from feature_engineering import feature_selection

# Concatenate raw Binance 1m tickdata csv files.
file_pattern = 'data/raw_data/binance_btcusdt_1m_Jan 2020 - July 2023\BTCUSDT-1m-2020-*.csv'
output_filename = 'data/clean_data/cleaned_btcusdt.csv'
concatenated_data = dmgt.concatenate_csv_files(file_pattern, output_filename)

