# generate_orders.py
from datamanager import DataManager


def generate_sigbar_orders(csv_path, date_col, output_csv):
    """
    Generate orders based on the signal time.

    :param csv_path: Path to the CSV file containing the data.
    :param date_col: Name of the column containing the timestamp in the CSV file.
    :param output_csv: Path to the output CSV file to save the generated orders.
    """
    # Create an instance of the DataManager class and load the data from the CSV
    dmgt = DataManager(csv_path, date_col)

    # Generate orders using the specified lookback period for sigtime in min.
    lookback = 60
    buffer = 2
    dmgt.generate_orders(lookback, buffer, output_csv)


if __name__ == "__main__":
    # Input file paths
    csv_path = "../../data/test_data/BTCMC/final_test/sigtime_ny.csv"
    date_col = "timestamp"
    output_csv = "../../data/test_data/BTCMC/final_test/orders_ny.csv"

    generate_sigbar_orders(csv_path, date_col, output_csv)























