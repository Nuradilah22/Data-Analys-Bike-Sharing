import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Dashboard Penyewaan Sepeda ✨")
st.write("Analisis pola penyewaan sepeda berdasarkan waktu dan musim.")

# load data
def load_data():
    data = pd.read_csv(r"D:\dila\submission\dashboard\all_data.csv", parse_dates=["dteday"])
    data.rename(columns={"dteday": "date"}, inplace=True)

    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    if "season_day" in data.columns:
        data["season_day"] = data["season_day"].map(season_mapping)
    
    return data 
 
data = load_data()   

# sidebar
st.sidebar.image("https://raw.githubusercontent.com/Nuradilah22/Data-Analys-Bike-Sharing/refs/heads/dilaa/sepeda.png")
st.sidebar.header("Filter Data")

selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(data["date"].dt.year.unique()))
selected_month = st.sidebar.selectbox("Pilih Bulan", range(1, 13))
selected_date = st.sidebar.date_input("Pilih Tanggal", min_value=data["date"].min(), max_value=data["date"].max())

tanggal_filter =  data[(data["date"].dt.year == selected_year) & (data["date"].dt.month == selected_month)]

# penyewaan sepeda per hari
st.subheader("Penyewaan Sepeda Per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tanggal_filter["date"], tanggal_filter["cnt_day"], marker="o", linestyle="-", alpha=0.7)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Penyewaan Sepeda per hari")
st.pyplot(fig)

# penyewaan sepeda per jam
st.subheader("Penyewaan Sepeda Per Jam")
hourly_avg = data.groupby("hr")["cnt_hour"].mean()
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(hourly_avg.index, hourly_avg.values, marker="o", linestyle="-")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Penyewaan Sepeda Per Jam")
ax.set_xticks(range(24))
st.pyplot(fig)

st.markdown(
    """*Info:*
    Dapat dilihat dari gambar di atas, waktu penyewaan sepeda pada pagi hari paling banyak pada jam 07.00 - 08.00, 
    sedangkan pada sore hari terlihat pada jam 16.00 - 18.00. Jadi, waktu yang optimal untuk menyediakan sepeda tambahan yaitu sebelum jam 07.00 pagi dan jam 16.00 sore.
    """
)

# penyewaan sepeda per musim
st.subheader("Penyewaan Sepeda per Musim")
season_avg = data.groupby("season_day")["cnt_day"].mean()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=season_avg.index, y=season_avg.values, palette="coolwarm", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Penyewaan Sepeda per Musim")
st.pyplot(fig)
