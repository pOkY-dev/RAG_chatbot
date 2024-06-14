import pandas as pd

def load_data(file_path):
    rental_data = pd.read_excel(file_path)
    print(rental_data.head())
    print(rental_data.columns)
    return rental_data

if __name__ == "__main__":
    file_path = 'data/merged_data_test_task.xlsx'
    load_data(file_path)