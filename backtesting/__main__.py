from feature_engineering import cleaning
from feature_engineering import feature_creation
from feature_engineering import feature_selection

# Binance 1m tickdata csv file concatenation.
file_pattern = '\backtesting data DO NOT DELETE\Binance tick data_1m\BTCUSDT_Jan 2020 - July 2023\unzippedBTCUSDT-1m-2020-*.csv'
output_filename = 'BTCUSDT-1m-concatenated.csv'

concatenated_data = concatenate_csv_files(file_pattern, output_filename)