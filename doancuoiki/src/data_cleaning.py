import pandas as pd
from data_loading import load_data

def clean_data(df):
    # Lọc các giá trị lỗi kiểu dữ liệu giá trị ở các trường về NaN
    columns_to_convert = ["AQI Value", "CO AQI Value", "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"]
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce', downcast="integer")

    # Xóa các bản ghi với trường dữ liệu AQI Value không hợp lệ
    df_cleaned = df[(df['AQI Value'].between(0, 500)) &
                     (df["CO AQI Value"].between(0, 500)) &
                     (df['Ozone AQI Value'].between(0, 500)) &
                     (df["NO2 AQI Value"].between(0, 500)) &
                     (df["PM2.5 AQI Value"].between(0, 500))]

    # Xóa các bản ghi trùng lặp
    df_cleaned = df_cleaned.drop_duplicates()

    # Xóa toàn bộ các bản ghi với trường dữ liệu trống hoặc NaN
    df_cleaned = df_cleaned.dropna()

    print("Đã xóa", len(df) - len(df_cleaned), "bản ghi lỗi")
    return df_cleaned

if __name__ == "__main__":
    df = load_data(r"C:\Users\THINKPAD\doancuoiki\data\raw\global_air_pollution_dataset.csv")
    if df is not None:
        cleaned_df = clean_data(df)
