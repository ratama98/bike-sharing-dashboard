import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load cleaned dataset
df_hour = pd.read_csv('hour_clean.csv')
df_day = pd.read_csv('day_clean.csv')

df_hour.sort_values(by="date", inplace=True)
df_hour.reset_index(inplace=True)

df_day.sort_values(by="date", inplace=True)
df_day.reset_index(inplace=True)

df_day["date"] = pd.to_datetime(df_day["date"])
df_hour["date"] = pd.to_datetime(df_day["date"])

# Filter data
min_date = df_day["date"].min()
max_date = df_day["date"].max()

st.title('Bike Sharing Rental Analysis Dashboard')

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df_day = df_day[(df_day["date"] >= str(start_date)) & 
                (df_day["date"] <= str(end_date))]
df_hour = df_hour[(df_hour["date"] >= str(start_date)) & 
                (df_hour["date"] <= str(end_date))]

# PERTANYAAN 1
df_hour['date'] = pd.to_datetime(df_hour['date'])
df_hour['hour'] = pd.to_datetime(df_hour['hour'], format='%H').dt.hour
hourly_rental_counts = df_hour.groupby('hour')['count'].mean()

st.write("## Hourly Rental Trend")
fig1, ax1 = plt.subplots(figsize=(10, 6))
hourly_rental_counts.plot(kind='line', marker='o', color='b', ax=ax1)
ax1.set_title('Hourly Rental Trend')
ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Total Rental Count')
ax1.grid(True)
ax1.set_xticks(range(24))
st.pyplot(fig1)

# PERTANYAAN 2
average_rental_count = df_day.groupby('holiday')['count'].mean()

st.write("## Average Daily Rental Count: Holiday vs Non-Holiday")
fig2, ax2 = plt.subplots(figsize=(8, 6))
average_rental_count.plot(kind='bar', color=['skyblue', 'orange'], ax=ax2)
ax2.set_title('Average Daily Rental Count: Holiday vs Non-Holiday')
ax2.set_ylabel('Average Daily Rental Count')
ax2.set_xticks([0, 1])
ax2.set_xticklabels(['Non-Holiday', 'Holiday'], rotation=0)
ax2.grid(axis='y')
st.pyplot(fig2)

# PERTANYAAN 3
user_type_rental_count = df_day.groupby('weekday')[['casual', 'registered']].mean().reset_index()

st.write("## Average Daily Rental Count by User Type and Day of the Week")
fig3, ax3 = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = user_type_rental_count['weekday']
ax3.bar(index, user_type_rental_count['casual'], bar_width, label='Casual Users', color='skyblue')
ax3.bar(index + bar_width, user_type_rental_count['registered'], bar_width, label='Registered Users', color='orange')
ax3.set_xlabel('Day of the Week')
ax3.set_ylabel('Average Daily Rental Count')
ax3.set_title('Average Daily Rental Count by User Type and Day of the Week')
ax3.set_xticks(index + bar_width / 2)
ax3.set_xticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
ax3.legend()
st.pyplot(fig3)