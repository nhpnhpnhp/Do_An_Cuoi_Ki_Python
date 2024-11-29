import seaborn as sns
import matplotlib.pyplot as plt

# Hiển thị ma trận tương quan giữa các chỉ số AQI
def display_correlation_matrix(cleaned_df):
    relevant_columns = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value']
    corr_matrix = cleaned_df[relevant_columns].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Ma trận tương quan của các yếu tố AQI")
    plt.show()
