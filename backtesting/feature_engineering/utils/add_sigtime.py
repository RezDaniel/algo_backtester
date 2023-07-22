# add_sigtime.py
from feature_engineering.feature_creation import DataManager


def main():
    csv_path = 'data/clean_data/cleaned_btc_with_timecols.csv'
    date_col = 'timestamp'

    dmgt = DataManager(csv_path, date_col)

    # Update sigtime, check_both=False just checks 'time_london' column.
    dmgt.update_sigtime_column(check_both=True)


if __name__ == "__main__":
    main()
