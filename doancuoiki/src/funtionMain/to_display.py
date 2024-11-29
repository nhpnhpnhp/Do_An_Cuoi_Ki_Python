def on_next_page(paginator, tree, page_label):
    data = paginator.next_page()  # Lấy dữ liệu trang tiếp theo
    update_tree(tree, data)  # Cập nhật Treeview
    update_page_label(paginator, page_label)  # Cập nhật số trang

def on_prev_page(paginator, tree, page_label):
    data = paginator.prev_page()  # Lấy dữ liệu trang trước
    update_tree(tree, data)  # Cập nhật Treeview
    update_page_label(paginator, page_label)  # Cập nhật số trang

def update_page_label(paginator, page_label):
    current_page = paginator.get_current_page()
    total_pages = paginator.get_total_pages()
    page_label.config(text=f"Trang {paginator.get_current_page()}/{paginator.total_pages}")

def update_tree(tree, dataf):
    tree.delete(*tree.get_children())
    if dataf is not None:
        tree["columns"] = list(dataf.columns)
        for col in dataf.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for idx, row in dataf.iterrows():
            tree.insert("", "end", values=list(row))
