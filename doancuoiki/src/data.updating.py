import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from src.paginator import Paginator
from src.funtionMain import update_page_label, update_tree


def get_level(z):
    if( z >=0 and z <=50):
        return "Good"
    elif z > 50 and z <=100:
        return "Moderate"
    elif z > 100 and z <= 150:
        return "Unhealthy for Sensitive Groups"
    elif z > 150 and z <= 200:
        return "Unhealthy"
    elif z > 200 and z <= 300:
        return "Very Unhealthy"
    elif z > 300:
        return "Hazardous "
    
import pandas as pd

def delete_data(dataframe, file_path, country, city):
    # Lọc và xóa các dòng có country và city trùng với dữ liệu đã chọn
    updated_df = dataframe[~((dataframe['Country'] == country) & (dataframe['City'] == city))]

    # Lưu lại DataFrame đã được cập nhật vào file CSV, đảm bảo không lưu chỉ mục
    updated_df.to_csv(file_path, index=False)

    # Trả về DataFrame đã được cập nhật
    return updated_df


def add_data(df, file_path, choose_country, choose_city, aqi_value, co_aqi, ozone_aqi, no2_aqi, pm25_aqi):
    existing_row = df[(df["Country"].str.lower() == choose_country.lower()) & (df["City"].str.lower() == choose_city.lower())]

    if not existing_row.empty:
        df.loc[
            (df["Country"].str.lower() == choose_country.lower()) &
            (df["City"].str.lower() == choose_city.lower()),
            [
                "AQI Value", "AQI Category",
                "CO AQI Value", "CO AQI Category",
                "Ozone AQI Value", "Ozone AQI Category",
                "NO2 AQI Value", "NO2 AQI Category",
                "PM2.5 AQI Value", "PM2.5 AQI Category",
            ]
        ] = [
            aqi_value, get_level(aqi_value),
            co_aqi, get_level(co_aqi),
            ozone_aqi, get_level(ozone_aqi),
            no2_aqi, get_level(no2_aqi),
            pm25_aqi, get_level(pm25_aqi),
        ]
    else:
        new_row = {
            "Country": choose_country,
            "City": choose_city,
            "AQI Value": aqi_value,
            "AQI Category": get_level(aqi_value),
            "CO AQI Value": co_aqi,
            "CO AQI Category": get_level(co_aqi),
            "Ozone AQI Value": ozone_aqi,
            "Ozone AQI Category": get_level(ozone_aqi),
            "NO2 AQI Value": no2_aqi,
            "NO2 AQI Category": get_level(no2_aqi),
            "PM2.5 AQI Value": pm25_aqi,
            "PM2.5 AQI Category": get_level(pm25_aqi),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    if not isinstance(file_path, str) or not file_path.endswith(".csv"):
        raise ValueError("Đường dẫn file không hợp lệ.")

    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise IOError(f"Không thể lưu dữ liệu vào file: {e}")

    return df

def submit_new_data(df, tree, page_label, entry_country, entry_city, entry_aqi, entry_co_aqi, entry_ozone_aqi, entry_no2_aqi, entry_pm25_aqi, file_path, paginator):
    try:
        # Lấy dữ liệu từ các trường nhập liệu
        choose_country = entry_country.get()
        choose_city = entry_city.get()
        aqi_value = int(entry_aqi.get())
        co_aqi = int(entry_co_aqi.get())
        ozone_aqi = int(entry_ozone_aqi.get())
        no2_aqi = int(entry_no2_aqi.get())
        pm25_aqi = int(entry_pm25_aqi.get())

        # Kiểm tra nếu tất cả các trường bắt buộc đều đã nhập
        if not choose_country or not choose_city or not aqi_value or not co_aqi or not ozone_aqi or not no2_aqi or not pm25_aqi:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ các thông tin.")
            return

        # Cập nhật hoặc thêm dữ liệu vào DataFrame và lưu vào file CSV
        df = add_data(df, file_path, choose_country, choose_city, aqi_value, co_aqi, ozone_aqi, no2_aqi, pm25_aqi)
        # Tải lại dữ liệu từ file và cập nhật paginator
        paginator.update_data(df)  # Cập nhật paginator với dữ liệu mới
        # Cập nhật Treeview với dữ liệu mới
        update_tree(tree, paginator.get_page_data())  # Cập nhật Treeview
        update_page_label(paginator, page_label)  # Cập nhật label số trang

        # Thông báo thành công
        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm hoặc cập nhật thành công.")
    except ValueError as e:
        messagebox.showerror("Lỗi đầu vào", f"Đầu vào không hợp lệ: {e}")
    return df
