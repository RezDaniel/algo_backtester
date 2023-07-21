# feature_selection.py
from feature_creation import DataManager


def generate_sigbar_orders(csv_path, date_col, output_filename):
    # Create an instance of the DataManager class and load the data from the CSV
    dmgt = DataManager(csv_path, date_col)

    dmgt.set_sigtime(8, 0)  # Set the signal time to 8:00 AM (08:00 hours)

    # Generate orders using the specified lookback period for sigtime in min.
    lookback = 60
    dmgt.generate_orders(lookback, output_filename)
























