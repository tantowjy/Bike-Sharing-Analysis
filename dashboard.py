import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# set streamlit page config and style seaborn
st.set_page_config(page_title="Bike Sharing Dashboard", layout='wide')
sns.set(style='dark')

# load data
df = pd.read_csv("dashboard/data.csv")
df['dateday'] = pd.to_datetime(df['dateday'])
df.season.replace(('dingin', 'semi', 'panas', 'gugur'),
                  ('winter', 'spring', 'summer', 'fall'),
                  inplace=True)
df.weathersit.replace(
    ('cerah/berawan', 'berawan dan berkabut', 'hujan/salju ringan', 'hujan/salju lebat'),
    ('clear/cloudy', 'cloudy and misty', 'light rain/snow', 'heavy rain/snow'),
    inplace=True)    

## SIDEBAR ------------------------------------------------
min_date = df['dateday'].min()
max_date = df['dateday'].max()

with st.sidebar:
    # Menambahkan logo
    st.image("dashboard/bike.png")

    # Mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label="Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dateday'] >= str(start_date)) & 
             (df['dateday'] <= str(end_date))]

# MAIN PAGE -------------------------------------------------
st.title("Bike Sharing Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    total_user = main_df['count'].sum()
    st.metric("Total User", value=total_user)

with col2:
    casual_user = main_df['casual'].sum()
    st.metric("Casual User", value=casual_user)

with col3:
    reg_user = main_df['registered'].sum()
    st.metric("Registered User", value=reg_user)

# chart 1
monthly_users = main_df.resample(rule='M', on='dateday').agg({
    "casual" : 'sum',
    'registered' : 'sum',
    'count' : 'sum'
})

monthly_users.index = monthly_users.index.strftime('%b-%y')
monthly_users = monthly_users.reset_index()
monthly_users.rename(columns={
    'casual': 'casual_users',
    'registered': 'registered_users',
    'count': 'total_users'
}, inplace=True)

chart_1 = px.line(monthly_users,
              x='dateday',
              y=['casual_users', 'registered_users', 'total_users'],
              color_discrete_sequence=['yellow', 'green', 'orange'],
              markers=True,
              title="Monthly Bike Sharing Users").update_layout(
                  xaxis_title='Month', 
                  yaxis_title='Total Users')

st.plotly_chart(chart_1, use_container_width=True)

# chart 2
season_analysis = main_df.iloc[:,[1,15]]
season_result = season_analysis.groupby(by='season').sum().reset_index().sort_values('count', ascending=False)

chart_2 = px.bar(season_result,
                  x='season',
                  y='count',
                  color_discrete_sequence=['skyblue', 'green', 'orange'],
                  title="Bike Sharing Users by Season").update_layout(
                      xaxis_title='Season',
                      yaxis_title='Total Users'
                  )

# chart 3
weather_analysis = main_df.iloc[:,[8,15]]
weather_result = weather_analysis.groupby(by='weathersit').sum().reset_index().sort_values('count', ascending=False)

chart_3 = px.bar(weather_result,
                  x='weathersit',
                  y='count',
                  color_discrete_sequence=['skyblue', 'green', 'orange'],
                  title="Bike Sharing Users by Weathersit").update_layout(
                      xaxis_title='Weathersit',
                      yaxis_title='Total Users'
                  )

left_col, right_col = st.columns(2)
left_col.plotly_chart(chart_2, use_container_width=True)
right_col.plotly_chart(chart_3, use_container_width=True)

# chart 4
t_min = -8
t_max = 39
main_df['temp'] = (main_df['temp'] * (t_max - t_min)) + t_min
main_df['windspeed'] = main_df['windspeed']*67

chart_4 = px.scatter(main_df, x='temp', y='count', color='season', height=600,
                 title="Clustering bike sharing users by temperature and season category",
                 labels={
                     'temp': 'Temperature (C)',
                     'count': 'Total Users'
                 })

st.plotly_chart(chart_4, use_container_width=True)

# chart 5
chart_5 = px.scatter(main_df, x='windspeed', y='count', color='season', height=600,
                     title='Clustering bike sharing users by windspeed and season category',
                     labels={
                         'windspeed': 'Wind Speed',
                         'count': 'Total Users'
                     }) 

st.plotly_chart(chart_5, use_container_width=True)