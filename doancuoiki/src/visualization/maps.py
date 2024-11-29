import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Bản đồ nhiệt AQI trung bình theo quốc gia
def generate_aqi_map(cleaned_df):
    pollute_country = cleaned_df.groupby("Country")["AQI Value"].mean().reset_index()
    fig = px.choropleth(
        pollute_country,
        locations="Country",
        locationmode="country names",
        color="AQI Value",
        hover_name="Country",
        color_continuous_scale="Turbo",
        title="Chỉ số chất lượng không khí trung bình theo quốc gia"
    )
    fig.show()
    
# Vẽ heatmap cho các thành phố sạch nhất và ô nhiễm nhất
def plot_aqi_heatmap(city_aqi_df, title, ascending=True):
    # Sắp xếp dữ liệu
    city_aqi_df = city_aqi_df.sort_values(by="AQI Value", ascending=ascending)
    
    # Đảm bảo thứ tự thành phố trên trục y
    heatmap_data = city_aqi_df.pivot_table(index="City", values="AQI Value")
    heatmap_data = heatmap_data.reindex(index=city_aqi_df["City"])  # Sắp xếp theo thứ tự dữ liệu đầu vào

    # Vẽ heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        cbar=True,
        linewidths=0.5,
        linecolor="white"
    )
    plt.title(title)
    plt.xlabel("Chỉ số AQI")
    plt.ylabel("Thành phố")
    plt.tight_layout()
    plt.show()