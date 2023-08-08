from datamanager import DataManager

if __name__ == '__main__':
    csv_path = "../../data/clean_data/cleaned_btc_2023.csv"
    output_csv = "../../data/test_data/TWC/cleaned_btc_weekly.csv"
    date_col = 'timestamp'
    max_holding = 10

    RS = DataManager(csv_path, date_col)
    df = RS.change_resolution("10080min")

    df.to_csv(output_csv, index=True)



