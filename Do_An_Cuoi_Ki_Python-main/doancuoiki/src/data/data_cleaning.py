import pandas as pd

# hàm đưa giá trị lỗi về biên 0 hoặc 500
def fix_out_of_bounds(value, min_val=0, max_val=500):
    if value < min_val:
        return min_val  
    elif value > max_val:
        return max_val 
    return value
def clean_data(df):
    # Lọc các giá trị lỗi kiểu dữ liệu giá trị ở các trường về NaN
    columns_to_convert = ["AQI Value", "CO AQI Value", "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"]
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce', downcast="integer")

    #Đưa các giá trị nằm ngoài khoảng [0;500] về giá trị biên
    for col in columns_to_convert:
        df[col] = df[col].apply(fix_out_of_bounds)
        
    # Xóa các bản ghi trùng lặp
    df_cleaned = df.drop_duplicates()
    
    # Xóa các bản ghi có cột dữ liệu trống hoặc NaN
    df_cleaned = df_cleaned.dropna()

    print("Đã xóa", len(df) - len(df_cleaned), "bản ghi lỗi")
        
    return df_cleaned
    
