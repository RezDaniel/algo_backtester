import pandas as pd


def convert_and_save(csv_path, output_path):
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    # Convert the 'timestamp' column to the desired format
    df['timestamp'] = df['timestamp'].dt.strftime('%Y/%m/%d')

    # Save the DataFrame back to a new CSV file
    df.to_csv(output_path, index=False)


# Use the function
input_csv = 'data/test_data/TWC/cleaned_btc_1w_2018.csv'
output_csv = 'data/test_data/TWC/converted_btc_1w_2018.csv'
convert_and_save(input_csv, output_csv)
