import pandas as pd
df = pd.read_csv(r"C:\Users\THINKPAD\doancuoiki\global_air_pollution_dataset.csv")
print("Trước khi làm sạch dữ liệu ta có :", len(df), "bản ghi")

###########################Clean data##################################

#Lọc các giá trị lỗi kiểu dữ liệu ở các trường về NaN
df["AQI Value"] = pd.to_numeric(df["AQI Value"], errors='coerce', downcast="integer")
df["CO AQI Value"] = pd.to_numeric(df["CO AQI Value"], errors='coerce', downcast="integer")
df["Ozone AQI Value"] = pd.to_numeric(df["Ozone AQI Value"], errors='coerce', downcast="integer")
df["NO2 AQI Value"] = pd.to_numeric(df["NO2 AQI Value"], errors='coerce', downcast="integer")
df["PM2.5 AQI Value"] = pd.to_numeric(df["PM2.5 AQI Value"], errors='coerce', downcast="integer")

#Xóa các bản ghi với trường dữ liệu AQI Value không hợp lệ: khác khoảng [0,500]
df_cleaned = df[(df['AQI Value'] >= 0) & (df['AQI Value'] <= 500) & (df["CO AQI Value"] >= 0) 
                & (df["CO AQI Value"] <= 500) & (df['Ozone AQI Value'] >= 0) & (df['Ozone AQI Value'] <= 500)
                & (df["Ozone AQI Value"] >= 0) & (df["Ozone AQI Value"] <=500) & (df["NO2 AQI Value"] >= 0)
                & (df["NO2 AQI Value"]<= 500) & (df["PM2.5 AQI Value"]>= 0) & (df["PM2.5 AQI Value"]<=500)]

df_cleaned = df.drop_duplicates() #Xóa các bản ghi trùng lặp



df_cleaned = df.dropna() # Xóa toàn bộ các bản ghi với trường dữ liệu trống hoặc NaN, null
print("Đã xóa", len(df) - len(df_cleaned), " bản ghi lỗi")



########################Thao tác cơ bản#############################
unique_cities = df_cleaned["City"].unique()

unique_countries = df_cleaned['Country'].unique()
print("Danh sách bao gồm: ", len(unique_countries), "quốc gia với", len(unique_cities), "thành phố")
unique_category = df_cleaned['AQI Category'].unique()
print("Các mức độ miêu tả của AQI bao gồm:", unique_category)
print(df_cleaned.head()) # Hiển thị 5 bản ghi đầu