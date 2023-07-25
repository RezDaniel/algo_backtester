# add_sigtime.py
from datamanager import DataManager


def main():
    csv_path = '../../data/test_data/build_data.csv'
    date_col = 'timestamp'
    output_csv = \
        '../../data/test_data/SRS141/build/sigtime_ny.csv'

    dmgt = DataManager(csv_path, date_col)

    # Update sigtime, check_both=False just checks 'time_london' column.
    dmgt.update_sigtime_column(output_csv, check_both=False)


if __name__ == "__main__":
    main()
