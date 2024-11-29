import pandas as pd
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.visualization.maps import generate_aqi_map
from src.visualization.correlation import display_correlation_matrix
from src.visualization.charts import plot_histograms, plot_linear_regression

# Nhóm dữ liệu theo quốc gia và tính giá trị trung bình AQI
def analyze_air_quality(cleaned_df):
    return cleaned_df.groupby('Country')['AQI Value'].mean().reset_index()

# Tìm giá trị AQI lớn nhất và quốc gia liên quan
def find_max_aqi_value(cleaned_df):
    max_aqi_value = cleaned_df['AQI Value'].max()
    max_aqi_row = cleaned_df[cleaned_df['AQI Value'] == max_aqi_value].iloc[0]  # Chỉ lấy hàng đầu tiên
    return pd.DataFrame([max_aqi_row])  # Trả về dưới dạng DataFrame

# Tìm các thành phố có giá trị AQI cao hơn ngưỡng
def find_high_aqi_cities(cleaned_df, threshold=500):
    high_aqi_cities = cleaned_df[cleaned_df['AQI Value'] == threshold][['Country', 'City', 'AQI Value']]
    return high_aqi_cities

# Tìm và hiển thị quốc gia có AQI trung bình nhỏ nhất
def find_min_avg_aqi(cleaned_df, threshold=0):
    avg_aqi_per_country = cleaned_df.groupby('Country')['AQI Value'].mean().reset_index()
    min_avg_aqi_value = avg_aqi_per_country['AQI Value'].min()
    min_avg_aqi_countries = avg_aqi_per_country[
        avg_aqi_per_country['AQI Value'].between(min_avg_aqi_value, min_avg_aqi_value + threshold)
    ]
    return min_avg_aqi_countries

# Tìm thành phố có giá trị AQI nhỏ nhất
def find_min_aqi_value(cleaned_df):
    min_aqi_value = cleaned_df['AQI Value'].min()
    min_aqi_data = cleaned_df[cleaned_df['AQI Value'] == min_aqi_value]
    return min_aqi_data

# Hiển thị các thành phố ở Ấn Độ có giá trị AQI bằng 500
def find_high_aqi_in_india(cleaned_df):
    return cleaned_df[(cleaned_df['Country'] == 'India') & (cleaned_df['AQI Value'] == 500)]
def submit_global(analysis_combobox, df, treeview):
        try:
            selected_analysis = analysis_combobox.get()  # Lấy mục phân tích từ ComboBox

            # Khởi tạo result với giá trị mặc định
            result = pd.DataFrame(columns=["Country", "City", "AQI Value"])

            if selected_analysis == "Trực quan hóa AQI toàn cầu":
                analyze_global_aqi(df)

            elif selected_analysis == "Giá trị AQI trung bình của các quốc gia":
                result = analyze_air_quality(df)

            elif selected_analysis == "Giá trị AQI lớn nhất":
                result = find_max_aqi_value(df)

            elif selected_analysis == "Các quốc gia có giá trị AQI nhỏ nhất":
                result = find_min_aqi_value(df)
                
            elif selected_analysis == "Hiển thị các thành phố ở Ấn Độ có giá trị AQI bằng 500":
                result = find_high_aqi_in_india(df)

            elif selected_analysis == "Các quốc gia có giá trị AQI cao nhất":
                result = find_high_aqi_cities(df, threshold=500)

            elif selected_analysis == "Quốc gia có giá trị AQI trung bình nhỏ nhất":
                result = find_min_avg_aqi(df)
                
            else:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một phân tích.")
                return

            # Cập nhật Treeview với kết quả phân tích
            for row in treeview.get_children():
                treeview.delete(row)  # Xóa hết các dòng cũ trong Treeview

            # Thêm dữ liệu mới vào Treeview
            if not result.empty:
                for _, row in result.iterrows():
                    # Kiểm tra xem dữ liệu có cột "City" không, nếu không thì thêm "N/A"
                    if "City" not in result.columns:
                        treeview.insert("", tk.END, values=[row["Country"], "N/A", row["AQI Value"]])
                    else:
                        treeview.insert("", tk.END, values=list(row))
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")



# Hàm chính để thực hiện phân tích toàn cầu
def analyze_global_aqi(cleaned_df):
    
    # Trực quan hóa
    print("\n=== Trực quan hóa ===")
    print("Tạo bản đồ nhiệt AQI...")
    generate_aqi_map(cleaned_df)

    print("Hiển thị ma trận tương quan...")
    display_correlation_matrix(cleaned_df)

    print("Vẽ biểu đồ histogram...")
    plot_histograms(cleaned_df)

    print("Vẽ hồi quy tuyến tính giữa AQI và PM2.5 AQI...")
    plot_linear_regression(cleaned_df)
