import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing Data", layout="wide")

st.title('California Housing Data (1990) by XiyuZhou')  

@st.cache_data
def load_data():
    data = pd.read_csv('/Users/uuuuuy/Desktop/Python/housing.csv/housing.csv')  

housing_data = load_data()

st.sidebar.header('More Filters')

if 'ocean_proximity' in housing_data.columns:
    location_types = housing_data['ocean_proximity'].unique()
    selected_locations = st.sidebar.multiselect(
        'Select Location Type:',
        options=location_types,
        default=location_types
    )
    housing_data = housing_data[housing_data['ocean_proximity'].isin(selected_locations)]

income_level = st.sidebar.radio(
    "Select Income Level:",
    ("Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (≥4.5)")
)

if income_level == "Low (≤2.5)":
    filtered_data = housing_data[housing_data['median_income'] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_data = housing_data[(housing_data['median_income'] > 2.5) & (housing_data['median_income'] < 4.5)]
else: 
    filtered_data = housing_data[housing_data['median_income'] >= 4.5]

st.subheader('Minimum Median House Price')
min_price = st.slider(
    "Select minimum median house price:",
    min_value=int(housing_data['median_house_value'].min()),
    max_value=int(housing_data['median_house_value'].max()),
    value=int(housing_data['median_house_value'].min()),
    key='price_slider'
)

price_filtered_data = filtered_data[filtered_data['median_house_value'] >= min_price]

st.subheader('Housing Data Map')
if 'latitude' in price_filtered_data.columns and 'longitude' in price_filtered_data.columns:
    st.map(price_filtered_data[['latitude', 'longitude']])
else:
    st.warning("Latitude and longitude data not found. Cannot display map.")

st.subheader('Median House Value Distribution')
fig, ax = plt.subplots()
ax.hist(price_filtered_data['median_house_value'], bins=30, edgecolor='black')
ax.set_xlabel('Median House Value')
ax.set_ylabel('Frequency')
st.pyplot(fig)

st.info("See more filters in the sidebar.")