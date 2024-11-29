class Paginator:
    def __init__(self, data, page_size=10):
        self.data = data
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = (len(data) // page_size) + (1 if len(data) % page_size > 0 else 0)

    def update_data(self, otherDF):
        self.data = otherDF
        self.current_page = 0
        self.total_pages = (len(otherDF) // self.page_size) + (1 if len(otherDF) % self.page_size > 0 else 0)
        print("co update data")

    def get_page_data(self):
        start_idx = self.current_page * self.page_size
        end_idx = min((self.current_page + 1) * self.page_size, len(self.data))
        return self.data.iloc[start_idx:end_idx]

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        return self.get_page_data()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        return self.get_page_data()

    def get_current_page(self):
        return self.current_page + 1  # Trang bắt đầu từ 1, không phải 0

    def get_total_pages(self):
        return self.total_pages
    
    def get_data(self):
        return self.data