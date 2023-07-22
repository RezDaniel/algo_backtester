# __main.py__
from feature_engineering import data_wrangling


start_date = '2019-01-01 00:00:00'
end_date = '2019-01-31 23:59:59'
sliced_df = data_wrangling.slice_data(
    'data/clean_data/cleaned_btc_timecols', start_date, end_date)



