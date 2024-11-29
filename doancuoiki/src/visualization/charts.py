import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Vẽ Pie Chart thể hiện tỷ lệ các loại AQI
def plot_aqi_category_pie(country_df, chosen):
    category_distribution = country_df['AQI Category'].value_counts()
    wedges, texts = plt.pie(
        category_distribution,
        colors=["#4c78a8", "#72b7b2", "#f58518", "#e45756", "#54a24b", "#b279a2"],
        startangle=90,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    plt.legend(
        wedges,
        [f"{label} ({value:.2f}%)" for label, value in zip(
            category_distribution.index,
            (category_distribution / category_distribution.sum()) * 100
        )],
        title="Các loại AQI",
        loc="center left",
        bbox_to_anchor=(1, 0.5)  
    )
    plt.title(f"Tỷ lệ các loại AQI tại {chosen}", fontsize=14)
    plt.tight_layout()
    plt.show()

# Biểu đồ cột: So sánh AQI 3 thành phố lớn 
def plot_major_cities_aqi(city_aqi):
    city_aqi.plot(kind="bar", color="orange", edgecolor="black")
    plt.title("So sánh AQI trung bình tại các thành phố lớn")
    plt.xlabel("Thành phố")
    plt.ylabel("AQI Value")
    plt.show()

# Biểu đồ cột: So sánh AQI Việt Nam với các quốc gia ASEAN
def plot_asean_aqi_comparison(asean_aqi):
    plt.figure(figsize=(8, 6))
    asean_aqi.sort_values(ascending=False).plot(kind="bar", color="purple", edgecolor="black")
    plt.title("So sánh AQI trung bình giữa các quốc gia ASEAN")
    plt.xlabel("Quốc gia")
    plt.ylabel("AQI Value")
    plt.show()

# Biểu đồ histogram của các giá trị AQI
def plot_histograms(cleaned_df):
    plt.figure(figsize=(8, 6))
    plt.hist(cleaned_df['AQI Value'], bins=30, color='blue', edgecolor='black', label='AQI Values')
    plt.hist(cleaned_df['PM2.5 AQI Value'], bins=30, color='orange', edgecolor='black', alpha=0.6, label='PM2.5 AQI Values')
    plt.title('Biểu đồ giá trị AQI', fontsize=16)
    plt.xlabel('Cả hai giá trị AQI', fontsize=12)
    plt.ylabel('Tính thường xuyên', fontsize=12)
    plt.legend(loc='upper right')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()

# Biểu đồ hồi quy tuyến tính giữa AQI Value và PM2.5 AQI Value
def plot_linear_regression(cleaned_df):
    x = cleaned_df['AQI Value'].values.reshape(-1, 1)
    y = cleaned_df['PM2.5 AQI Value'].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    plt.figure(figsize=(8, 6))
    plt.plot(x, model.predict(x), color='red', label='Regression Line')
    sns.scatterplot(x='AQI Value', y='PM2.5 AQI Value', data=cleaned_df, label='Data Points')
    plt.title('Giá trị AQI vs Giá trị AQI PM2,5', fontsize=16)
    plt.xlabel('Giá trị AQI', fontsize=12)
    plt.ylabel('Giá trị AQI PM2.5', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()
