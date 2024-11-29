import pandas as pd
from src.data.data_cleaning import clean_data

# Hàm để tải dữ liệu từ một file CSV.
def load_data(clean_file, raw_file_path):
    try:
        df = pd.read_csv(clean_file)
        print(f"Đã tải dữ liệu sạch thành công từ {clean_file}")
        return df
    except :
        df = pd.read_csv(raw_file_path)
        print(f"Đã tải dữ liệu thô thành công từ {raw_file_path}")
        cleaned_data = clean_data(df)
        print(f"Đã làm sạch dữ liệu")
        try:
            cleaned_data.to_csv(clean_file, index=False)
            print(f"Dữ liệu đã làm sạch được lưu vào file: {clean_file}")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
        return cleaned_data
