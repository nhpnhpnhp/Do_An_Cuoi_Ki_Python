import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.funtionMain import on_next_page, on_prev_page, update_page_label, update_tree

# Hàm sắp xếp dữ liệu theo tên quốc gia và nhập trực tiếp thứ tự sắp xếp
def sort_data(data, column_name, ascending=True):
    """
    Sắp xếp DataFrame theo cột đã chọn.
    
    :param data: DataFrame chứa dữ liệu.
    :param column_name: Tên cột để sắp xếp.
    :param ascending: True cho sắp xếp tăng dần, False cho sắp xếp giảm dần.
    :return: DataFrame đã được sắp xếp.
    """
    # Kiểm tra nếu cột tồn tại trong DataFrame
    if column_name in data.columns:
        return data.sort_values(by=column_name, ascending=ascending)
    else:
        raise ValueError(f"Cột {column_name} không tồn tại trong dữ liệu.")
    
def sumbit_sort(dfNow, column_combo, sort_order_combo,paginator,tree, page_label ):
        # Lấy cột và thứ tự sắp xếp từ các lựa chọn
        column_to_sort = column_combo.get()
        sort_order = sort_order_combo.get()
        if column_to_sort not in dfNow.columns:
            messagebox.showwarning("Cảnh báo", "Cột không hợp lệ!")
            return
        
        # Xác định thứ tự sắp xếp
        ascending = True if sort_order == "Tăng dần" else False

        try:
            # Gọi hàm sort_data_ok để sắp xếp dữ liệu
            sorted_data = sort_data(dfNow, column_to_sort, ascending)

            # Cập nhật Treeview với dữ liệu đã sắp xếp
            paginator.update_data(sorted_data)
            update_tree(tree, paginator.get_page_data())
            update_page_label(paginator, page_label)

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Lỗi khi sắp xếp dữ liệu: {e}")

# Hàm tìm kiếm theo tên quốc gia và thành phố, nhập trực tiếp thông tin
def search_data(dataf, country, city):
    # Lọc dữ liệu theo quốc gia và thành phố
    if country:
        dataf = dataf[dataf['Country'].str.contains(country, case=False)]
    if city:
        dataf = dataf[dataf['City'].str.contains(city, case=False)]
    return dataf

# Hàm lọc dữ liệu cho Combobox (các quốc gia)
def on_keyrelease(event, entry, data_list):
    # Lấy giá trị đã nhập vào
    value = entry.get().lower()
    # Lọc dữ liệu theo giá trị người dùng đã nhập
    filtered_data = [item for item in data_list if value in item.lower()]
    # Cập nhật lại giá trị gợi ý trong Combobox
    entry['values'] = filtered_data

# Hàm khi thay đổi quốc gia (update danh sách thành phố)
def on_country_change(event, entry_country_search, entry_city_search, df):
    # Lấy quốc gia được chọn
    selected_country = entry_country_search.get()
    
    # Lọc danh sách thành phố theo quốc gia được chọn
    if selected_country:
        cities = df[df['Country'] == selected_country]['City'].dropna().unique().tolist()
    else:
        cities = []
    
    # Cập nhật lại danh sách thành phố trong entry_city_search
    entry_city_search['values'] = cities
    entry_city_search.set('')  # Xóa giá trị đã chọn trong ô thành phố

# Hàm lọc thành phố theo quốc gia và tên nhập vào
def on_city_keyrelease(event, entry_city_search, selected_country, df):
    # Lấy giá trị đã nhập vào ô thành phố
    value = entry_city_search.get().lower()

    # Lọc danh sách thành phố thuộc quốc gia đã chọn và theo tên nhập vào
    if selected_country:
        cities = df[(df['Country'] == selected_country) & (df['City'].str.contains(value, case=False))]
        filtered_cities = cities['City'].tolist()
    else:
        filtered_cities = []

    # Cập nhật lại giá trị gợi ý trong Combobox thành phố
    entry_city_search['values'] = filtered_cities

def submit_search(entry_country_search,entry_city_search, df, paginator, tree, page_label):
        # Lấy giá trị nhập vào từ các ô tìm kiếm
        search_country = entry_country_search.get()
        search_city = entry_city_search.get()

        # Kiểm tra nếu không có giá trị nhập vào cho quốc gia hoặc thành phố, sẽ bỏ qua bộ lọc tương ứng
        if search_country and search_city:
            filtered_data = search_data(df, search_country, search_city)
        elif search_country:
            filtered_data = df[df['Country'].str.contains(search_country, case=False, na=False)]
        elif search_city:
            filtered_data = df[df['City'].str.contains(search_city, case=False, na=False)]
        else:
            # Nếu cả hai ô đều trống, hiển thị toàn bộ dữ liệu
            filtered_data = df

        # Cập nhật Treeview với dữ liệu tìm được
        paginator.update_data(filtered_data)
        update_tree(tree, paginator.get_page_data())
        update_page_label(paginator, page_label)