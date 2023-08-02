from datamanager import DataManager

# __main.py__

if __name__ == '__main__':
    csv_path = "data/clean_data/cleaned_btc.csv"
    output_csv = "data/test_data/RipVanWinkle/cleaned_btc_4hr_test.csv"
    date_col = 'timestamp'
    max_holding = 10

    RS = DataManager(csv_path, date_col)
    df = RS.change_resolution("240min")

    df.to_csv(output_csv, index=True)



