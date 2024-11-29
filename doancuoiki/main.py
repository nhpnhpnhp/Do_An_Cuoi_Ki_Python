import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from src.data import load_data, delete_data, submit_new_data, submit_search, on_keyrelease,on_country_change, on_city_keyrelease, sumbit_sort
from src.analysis import submit_country, submit_global
from src.funtionMain import on_next_page, on_prev_page, update_page_label, update_tree
from src.paginator import Paginator



def add_or_update_data_gui():

    # Cửa sổ nhập liệu thêm/cập nhật dữ liệu
    add_window = tk.Toplevel(root)
    add_window.title("Thêm / Cập nhật Dữ liệu")
    
    frame = tk.Frame(add_window, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Country").grid(row=0, column=0, padx=5, pady=5)
    entry_country = tk.Entry(frame)
    entry_country.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="City").grid(row=1, column=0, padx=5, pady=5)
    entry_city = tk.Entry(frame)
    entry_city.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="AQI Value").grid(row=2, column=0, padx=5, pady=5)
    entry_aqi = tk.Entry(frame)
    entry_aqi.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="CO AQI Value").grid(row=3, column=0, padx=5, pady=5)
    entry_co_aqi = tk.Entry(frame)
    entry_co_aqi.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame, text="Ozone AQI Value").grid(row=4, column=0, padx=5, pady=5)
    entry_ozone_aqi = tk.Entry(frame)
    entry_ozone_aqi.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame, text="NO2 AQI Value").grid(row=5, column=0, padx=5, pady=5)
    entry_no2_aqi = tk.Entry(frame)
    entry_no2_aqi.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(frame, text="PM2.5 AQI Value").grid(row=6, column=0, padx=5, pady=5)
    entry_pm25_aqi = tk.Entry(frame)
    entry_pm25_aqi.grid(row=6, column=1, padx=5, pady=5)

    def get_df():
        global df 
        df = submit_new_data(df, tree, page_label, entry_country, entry_city,entry_aqi, entry_co_aqi, entry_ozone_aqi, entry_no2_aqi, entry_pm25_aqi, a, paginator)
        

    submit_button = tk.Button(frame, text="Submit", command= get_df)
    submit_button.grid(row=8, column=0, columnspan=2, pady=10)

# Hàm xóa dữ liệu
def delete_data_gui():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Không chọn dữ liệu", "Vui lòng chọn thành phố để xóa.")
        return

    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa dữ liệu đã chọn?")
    if confirm:
        global df
        try:
            # Lặp qua các mục được chọn và xóa
            for item in selected_items:
                selected_values = tree.item(item)['values']
                selected_country = selected_values[0]
                selected_city = selected_values[1]

                # Cập nhật lại df1 sau khi xóa
                df = delete_data(df, a, selected_country, selected_city)

            # Cập nhật lại Paginator và Treeview
            paginator.update_data(df)  # Cập nhật dữ liệu cho Paginator
            update_tree(tree, paginator.get_page_data())  # Cập nhật Treeview với dữ liệu mới
            update_page_label(paginator, page_label)  # Cập nhật lại label trang

            messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa dữ liệu: {e}")


# Hàm tìm kiếm dữ liệu
def search_data_gui():

    # Tạo một frame để chứa ô tìm kiếm trên giao diện chính
    search_frame = tk.Frame(root, padx=10, pady=10)
    search_frame.pack(padx=10, pady=10)
    
       
    tk.Label(search_frame, text="Country:").pack(side="left", padx=5)
    entry_country_search = ttk.Combobox(search_frame, values=countries, state="normal")
    entry_country_search.pack(side="left", padx=5)

    tk.Label(search_frame, text="City:").pack(side="left", padx=5)
    entry_city_search = ttk.Combobox(search_frame, values=cities, state="normal")
    entry_city_search.pack(side="left", padx=5)

    # Thêm sự kiện cho việc nhập liệu vào quốc gia, MỖI KÍ TỰ ĐƯỢC NHẬP VÀO, SẼ TẠO RA MỘT LIST ĐỂ GỢI Ý CHO COUNTRY
    entry_country_search.bind('<KeyRelease>', lambda event: on_keyrelease(event, entry_country_search, countries))
    
    # Thêm sự kiện khi thay đổi quốc gia, cập nhật thành phố tương ứng, SAU KHI LỰA CHỌN SẼ CẬP NHẬT LIST THÀNH PHỐ THUỘC QUỐC GIA ĐÓ
    entry_country_search.bind('<<ComboboxSelected>>', lambda event: on_country_change(event, entry_country_search, entry_city_search, df))
    
    # Thêm sự kiện cho việc nhập liệu vào thành phố, MỖI KÍ TỰ ĐƯỢC NHẬP VÀO, SẼ TẠO RA MỘT LIST ĐỂ GỢI Ý CHO CITY
    entry_city_search.bind('<KeyRelease>', lambda event: on_city_keyrelease(event, entry_city_search, entry_country_search.get(), df))

    search_button = tk.Button(search_frame, text="Tìm kiếm", command=lambda: submit_search (entry_country_search,entry_city_search, df, paginator, tree, page_label))
    search_button.pack(side="left", padx=5)
   

# Giao diện sắp xếp
def sort_data_gui():
    dfNow = paginator.get_data()

    # Cửa sổ sắp xếp
    sort_window = tk.Toplevel(root)
    sort_window.title("Sắp xếp dữ liệu")

    frame = tk.Frame(sort_window, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Chọn cột để sắp xếp:").grid(row=0, column=0, padx=5, pady=5)
    column_combo = ttk.Combobox(frame, values=df.columns.tolist())  # Dropdown cho các cột
    column_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Chọn thứ tự:").grid(row=1, column=0, padx=5, pady=5)
    sort_order_combo = ttk.Combobox(frame, values=["Tăng dần", "Giảm dần"])  # Dropdown cho thứ tự sắp xếp
    sort_order_combo.grid(row=1, column=1, padx=5, pady=5)

    sort_button = tk.Button(frame, text="Sắp xếp", command= lambda: sumbit_sort(dfNow, column_combo, sort_order_combo,paginator,tree, page_label))
    sort_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Thêm nút đóng cửa sổ sắp xếp
    close_button = tk.Button(frame, text="Đóng", command=sort_window.destroy)
    close_button.grid(row=3, column=0, columnspan=2, pady=10)

def global_analysis():
    # Tạo cửa sổ con cho phân tích toàn cầu
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Phân tích AQI toàn cầu")
    
    # Cấu trúc giao diện
    frame = tk.Frame(analysis_window, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    # Tiêu đề của cửa sổ phân tích
    title_label = tk.Label(frame, text="Phân tích AQI toàn cầu", font=("Arial", 18))
    title_label.grid(row=0, column=0, pady=10)

    # ComboBox để chọn phân tích
    analysis_label = tk.Label(frame, text="Chọn phân tích:", font=("Arial", 14))
    analysis_label.grid(row=1, column=0, pady=10)
    analysis_combobox = ttk.Combobox(frame, values=[
        "Trực quan hóa AQI toàn cầu",
        "Giá trị AQI trung bình của các quốc gia",
        "Giá trị AQI lớn nhất",
        "Hiển thị các thành phố ở Ấn Độ có giá trị AQI bằng 500",
        "Các quốc gia có giá trị AQI nhỏ nhất",
        "Các quốc gia có giá trị AQI cao nhất",
        "Quốc gia có giá trị AQI trung bình nhỏ nhất",
    ], font=("Arial", 12), width=40)
    analysis_combobox.grid(row=1, column=1, pady=10)

    # Nút bắt đầu phân tích
    analyze_button = tk.Button(frame, text="Phân tích", command=lambda: submit_global(analysis_combobox, df, treeview), width=20, height=2, font=("Arial", 10))
    analyze_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Khu vực Treeview để hiển thị kết quả phân tích
    treeview_frame = tk.Frame(frame)
    treeview_frame.grid(row=3, column=0, columnspan=2, pady=10)

    treeview = ttk.Treeview(treeview_frame, columns=("Column1", "Column2", "Column3"), show="headings", height=10)
    treeview.pack(fill=tk.BOTH, expand=True)

    # Cấu hình các cột Treeview
    treeview.heading("Column1", text="Country")
    treeview.heading("Column2", text="City")
    treeview.heading("Column3", text="AQI Value")

    # Căn chỉnh các cột cho hợp lý
    treeview.column("Column1", anchor="w", width=200)  
    treeview.column("Column2", anchor="w", width=200)  
    treeview.column("Column3", anchor="e", width=100)  

    # Nút đóng cửa sổ phân tích
    close_button = tk.Button(frame, text="Đóng", command=analysis_window.destroy, width=30, height=2, font=("Arial", 14))
    close_button.grid(row=4, column=0, columnspan=2, pady=10)

# Hàm phân tích quốc gia
def country_analysis():
    # Tạo cửa sổ nhập quốc gia
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Phân tích AQI theo quốc gia")
    
    frame = tk.Frame(analysis_window, padx=10, pady=10)
    frame.pack()

    country_list = sorted(df['Country'].dropna().unique().tolist())
    frame.pack()

    tk.Label(frame, text="Chọn quốc gia:").grid(row=0, column=0, padx=5, pady=5)
    country_entry = ttk.Combobox(frame, values=countries, state="normal")
    country_entry.bind('<KeyRelease>', lambda event: on_keyrelease(event, country_entry, countries))

    country_entry.grid(row=0, column=1, padx=5, pady=5)

    submit_button = tk.Button(frame, text="Phân tích", command= lambda: submit_country(country_entry, paginator.get_data(), a))
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    close_button = tk.Button(frame, text="Đóng", command=analysis_window.destroy)
    close_button.grid(row=2, column=0, columnspan=2, pady=10)

def create_button(parent, text, command, side="left", padx=10, pady=10):
    button = tk.Button(parent, text=text, command=command)
    button.pack(side=side, padx=padx, pady=pady)
    return button

root = tk.Tk()
root.title("Air Manager")
root.geometry("1400x700")

raw_file_path = r"C:\Users\DELL\Downloads\DoAnCuoiKi (1)\doancuoiki\data\raw\global_air_pollution_dataset.csv"
a = r"C:\Users\DELL\Downloads\DoAnCuoiKi (1)\doancuoiki\data\cleaned\cleaned_data.csv"
df = load_data(a, raw_file_path)
paginator = Paginator(df)

countries = df['Country'].dropna().unique().tolist()
cities = df['City'].dropna().unique().tolist()

search_data_gui()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)
tree = ttk.Treeview(frame, show="headings")
tree.pack(fill="both", expand=True, pady=5)

# Nút Next và Previous
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)
# Cập nhật command cho nút "Trang trước" và "Trang sau"
# Thêm page_label vào trong hàm lambda
create_button(button_frame, "Trang trước", command=lambda: on_prev_page(paginator, tree, page_label), side="left")
create_button(button_frame, "Trang sau", command=lambda: on_next_page(paginator, tree, page_label), side="right")



# Các nút chức năng khác
create_button(root, "Phân tích toàn cầu", global_analysis)
create_button(root, "Phân tích quốc gia", country_analysis)
create_button(root, "Thêm / Sửa", add_or_update_data_gui)
create_button(root, "Xóa", delete_data_gui)
create_button(root, "Sắp xếp dữ liệu", sort_data_gui)

# Label hiển thị số trang
page_label = tk.Label(root, text="", font=("Arial", 12))
page_label.pack(pady=5)

# Hiển thị trang đầu tiên và cập nhật số trang
update_tree(tree, paginator.get_page_data())
update_page_label(paginator, page_label)

# Chạy ứng dụng
root.mainloop()

