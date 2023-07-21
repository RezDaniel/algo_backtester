from feature_engineering import data_wrangling as ds
from feature_engineering.feature_creation import DataManager as dmgt
from feature_engineering import feature_selection

start_date = '2019-01-01 00:00:00'
end_date = '2019-01-31 23:59:59'
sliced_df = ds.slice_data('data/clean_data/cleaned_btc',
                          start_date, end_date)

