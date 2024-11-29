import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.visualization.maps import plot_aqi_heatmap
from src.visualization.charts import  plot_aqi_category_pie, plot_asean_aqi_comparison
# Lọc dữ liệu chỉ cho this country từ tập dữ liệu ô nhiễm toàn cầu đã được làm sạch
def get_country_data(pollution_df, chosen_coutry):
    country_df = pollution_df[pollution_df["Country"] == chosen_coutry].reset_index(drop=True)
    return country_df

# 15 Thành phố sạch nhất và 15 ô nhiễm nhất
def find_top_n_cleanest_and_most_polluted_cities(country_df, n=15):
    # Thành phố sạch nhất
    cleanest_cities = country_df.groupby("City")["AQI Value"].mean().sort_values(ascending=True).head(n).reset_index()
    # Thành phố ô nhiễm nhất
    most_polluted_cities = country_df.groupby("City")["AQI Value"].mean().sort_values(ascending=False).head(n).reset_index()
    return cleanest_cities, most_polluted_cities



# So sánh AQI trung bình của các thành phố lớn
def compare_major_cities(pollution_df, country_df, chosen_country, out_file):
    major_cities = country_df[country_df["isBigCity"] == True]["City"].tolist()
    return country_df[country_df["City"].isin(major_cities)].groupby("City")["AQI Value"].mean()

# So sánh các quốc gia ASEAN
def compare_country_to_asean(pollution_df, chose_country):
    asean_countries = [
        "Viet Nam", "Thailand", "Malaysia", "Singapore", "Indonesia",
        "Philippines", "Cambodia", "Lao People's Democratic Republic", "Myanmar"
    ]

    if chose_country not in asean_countries:
        asean_countries.append(chose_country)
    asean_df = pollution_df[pollution_df["Country"].isin(asean_countries)]
    return asean_df.groupby("Country")["AQI Value"].mean()

# Hàm chính để thực hiện tất cả các bước phân tích cho một quốc gia
def analyze_country_aqi(pollution_df, chosen_country, out_file):
    country_df = get_country_data(pollution_df, chosen_country)
    print(f"Dữ liệu của {chosen_country} đã được lọc thành công.")
    print(country_df)

    # Thống kê tổng quan
    stats = country_df.describe()
    print(f"Thống kê tổng quan về các chỉ số AQI tại {chosen_country}:")
    print(stats)

    # Phân tích phân bố AQI Category
    distribution = country_df["AQI Category"].value_counts()
    print(f"\nPhân bố các loại AQI tại {chosen_country}:")
    print(distribution)
    plot_aqi_category_pie(country_df, chosen_country)

    # Vẽ heatmap cho các thành phố sạch nhất và ô nhiễm nhất
    cleanest_cities, most_polluted_cities = find_top_n_cleanest_and_most_polluted_cities(country_df, n=15)
    plot_aqi_heatmap(cleanest_cities, f"15 thành phố sạch nhất tại {chosen_country} (AQI thấp nhất)", ascending=True)
    plot_aqi_heatmap(most_polluted_cities, f"15 thành phố ô nhiễm nhất tại {chosen_country} (AQI cao nhất)", ascending=False)
    print("\n15 thành phố sạch nhất (AQI thấp nhất):")
    print(cleanest_cities)
    print("\n15 thành phố ô nhiễm nhất (AQI cao nhất):")
    print(most_polluted_cities)
    
    # So sánh với ASEAN
    asean_aqi = compare_country_to_asean(pollution_df, chosen_country)
    print(f"\nSo sánh AQI trung bình của {chosen_country} với các quốc gia ASEAN:")
    print(asean_aqi)
    plot_asean_aqi_comparison(asean_aqi)
    
def submit_country(country_entry, df, out_file):
        chosen_country = country_entry.get()

        if not chosen_country:
            messagebox.showwarning("Thông báo", "Vui lòng nhập tên quốc gia.")
            return
        
        try:
            # Gọi hàm phân tích quốc gia
            analyze_country_aqi(df, chosen_country, out_file)
            messagebox.showinfo("Hoàn tất", f"Phân tích AQI cho {chosen_country} đã hoàn thành.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi phân tích: {e}")
