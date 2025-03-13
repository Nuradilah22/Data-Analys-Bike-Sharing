import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Dashboard Bike Sharing ✨")
st.markdown("Analyzing bike rental trends by date and hour.")

@st.cache_data
def load_data():
    main_df = pd.read_csv("main_data.csv")
    main_df["dteday"] = pd.to_datetime(main_df["dteday"])
    return main_df

main_df = load_data()

dataset_option = st.radio("Select Dataset:", ["Daily", "Hourly"])

if dataset_option == "Daily":
    df = main_df[['dteday', 'cnt_day']] 
    st.subheader("📅 Daily Bike Rental Analysis")
else:
     df = main_df[['dteday', 'hr', 'cnt_hour']]
     st.subheader("🕒 Hourly Bike Rental Analysis")

st.markdown("# Rental Trend")

st.sidebar.header("📅 Select Date")
available_dates = main_df["dteday"].dt.strftime("%Y-%m-%d").unique()
selected_date = st.sidebar.selectbox("Select date:", available_dates)

filtered_df = main_df[main_df["dteday"] == pd.to_datetime(selected_date)]

total_rentals = filtered_df["cnt_day"].sum()  
avg_rentals = filtered_df["cnt_day"].mean()
peak_hour = filtered_df.loc[filtered_df["cnt_hour"].idxmax(), "hr"] if "hr" in filtered_df.columns else None

st.markdown("### 📈 Bike Rental Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("🔹 Total Rentals", f"{total_rentals:,} bikes")
col2.metric("📊 Daily Average", f"{avg_rentals:.0f} bikes")
col3.metric("🚀 Busiest Hour", f"{peak_hour}:00" if peak_hour is not None else "N/A")

st.markdown("### 🕒 Hourly Bike Rental Trend")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_df["hr"], y=filtered_df["cnt_hour"], marker="o", color="tab:red", ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Hour")
    ax.set_ylabel("Rental Count")
    ax.set_title(f"Bike Rental Trend on {selected_date}")
    ax.grid()
    st.pyplot(fig)
else:
    st.warning("⚠ No rental data available for this date.")

st.markdown("### 📈 Daily Bike Rental Trend")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=main_df["dteday"], y=main_df["cnt_day"], marker="o", color="tab:blue", ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Rental Count")
ax.set_title("Bike Rental Trend")
ax.grid()
st.pyplot(fig)

st.markdown("### 🔄 Comparing Bike Rentals: Workdays vs Holidays")

workday_rentals = main_df[main_df["workingday_day"] == 1].groupby("hr")["cnt_hour"].mean()  
holiday_rentals = main_df[main_df["workingday_day"] == 0].groupby("hr")["cnt_hour"].mean()  

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=workday_rentals.index, y=workday_rentals.values, marker="o", label="Workdays", ax=ax, color="tab:blue")
sns.lineplot(x=holiday_rentals.index, y=holiday_rentals.values, marker="o", label="Holidays", ax=ax, color="tab:orange")

ax.set_title("Bike Rental Comparison: Workdays vs Holidays")
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Average Rentals")
ax.legend()
ax.grid()

st.pyplot(fig)

st.markdown("### 📝 Bike Rental Data")
st.dataframe(filtered_df)
