"""
Name:       Bryan Calabrese
CS230:      Section 5
Data:       Uber Fares
URL:        Link to your web application online

Description:

This program is designed to show data from Uber trips throughout New York City from 2009 to 2015.
It first shows the Uber Logo as well as important metrics that are valuable to the company's data collection.
It plots out fare amount data to show whether the number of passengers matter, as well as how much the duration of the ride matters.
It also maps out dropoff and pickup locations based off of the amount of passengers a user selects.

"""
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

with open('requirements.txt') as f:
    lines = f.readlines()
st.image('/Users/bryancalabrese/OneDrive - Bentley University/Spring 2022/CS 230/Project/pngwing.com.png') # Used a logo instead of a title
st.sidebar.image('/Users/bryancalabrese/OneDrive - Bentley University/Spring 2022/CS 230/Project/Uber_logo.svg.png')

df_uber = pd.read_csv('/Users/bryancalabrese/OneDrive - Bentley University/Spring 2022/CS 230/Project/uber_8000_sample.csv')
df = pd.DataFrame(df_uber)
sdf = df_uber.loc[:,"key":"passenger_count"]
sdf = sdf.dropna()
sdf = sdf.drop(sdf[sdf.fare_amount<0].index)
sdf.set_index("key", inplace=True)


def sidebarheader(part):
    st.sidebar.header("Part " + part)
    return

# Metric
metrics_header = '<p style="font-family:KrungThep; color:Black; font-size: 50px;">Average Metrics </p>'
st.markdown(metrics_header, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Average Fare", "$11.42")
col2.metric("Average Number of Passengers", "1.7")
col3.metric("Average Duration of Trip", "00:29:50")

# Part 1
sidebarheader(part="I")
st.title("Part I")
st.header("Uber Fares Per Passenger")

fare_amt = st.sidebar.slider("Please select a trip total fare amount:",5,196)
s1 = sdf[sdf.fare_amount <= fare_amt][['fare_amount', 'passenger_count']]

#st.dataframe(s1)
dfaverage = s1.groupby("passenger_count").mean()

chart = st.sidebar.selectbox("Select a chart", ["","Bar Chart", "Line Plot"])

passengers = [0,1,2,3,4,5,6]
fig, ax = plt.subplots()

if chart == "Bar Chart":
    fig1 = plt.figure(figsize=(12,8))
    ax1 = fig1.add_axes([.5,.5,.5,.5])
    ax1.bar(passengers, dfaverage["fare_amount"], color = 'red')
    ax1.set_xlabel("Passengers")
    ax1.set_ylabel("Fare Amount")
    ax1.set_title("Fare per Passenger")
    st.pyplot(fig1)
elif chart == "Line Plot":
    fig1 = plt.figure(figsize=(12,8))
    ax1 = fig1.add_axes([.5,.5,.5,.5])
    ax1.plot(passengers, dfaverage["fare_amount"], color = 'orange')
    ax1.set_xlabel("Passengers")
    ax1.set_ylabel("Fare Amount")
    ax1.set_title("Fare per Passenger")
    st.pyplot(fig1)
else:
    st.write("Please select a chart: ")

# Part 2
sidebarheader(part="II")
st.title("Part II")
st.header("Uber Fares versus Trip Duration")

fare_amt2 = st.sidebar.number_input("Please select how much you are willing to spend:",2.5,200.0)
s5 = sdf[sdf.fare_amount <= fare_amt2][['fare_amount']]
time_fare = s5.groupby(s5.index).mean()
#st.write(time_fare.index)

fig2 = plt.figure(figsize=(12,8))
ax2 = fig2.add_axes([1,1,1,1])
ax2.scatter(time_fare.index, time_fare["fare_amount"], color = 'green')
ax2.set_xlabel("Trip Duration")
ax2.set_ylabel("Fare Amount")
ax2.set_title("Fare Amount effect on Trip Duration")
ax2.set_xticks([time_fare.index.min(), time_fare.index.max()])
st.pyplot(fig2)

# Part 3
sidebarheader(part="III")
st.title("Part III")

passengers2 = st.sidebar.radio("Please select how many passengers:", passengers)

s3 = sdf[sdf["passenger_count"]==passengers2]
#st.write(s3)

st.header("Pickup Locations")

view_state = pdk.ViewState(
    latitude=sdf["pickup_latitude"].median(),
    longitude=sdf["pickup_longitude"].median(),
    zoom=11,
    pitch=0)

# Create a map layer with the given coordinates
layer1 = pdk.Layer(type = 'ScatterplotLayer',
                  data=s3,
                  get_position='[pickup_longitude, pickup_latitude]',
                  get_radius=40,
                  get_color=[25,0,255],
                  pickable=True,
                   )

map = pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-streets-v11',
        initial_view_state=view_state,
        layers=[layer1],
    )

st.pydeck_chart(map)

st.header("Dropoff Locations")
view_state2 = pdk.ViewState(
    latitude=sdf["dropoff_latitude"].median(),
    longitude=sdf["dropoff_longitude"].median(),
    zoom=11,
    pitch=0)

# Create a map layer with the given coordinates
layer2 = pdk.Layer(type = 'ScatterplotLayer', # layer type
                  data=s3, # data source
                  get_position='[dropoff_longitude, dropoff_latitude]',
                  get_radius=40,
                  get_color=[600,0,255],
                  pickable=True,
                   )

map2 = pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-streets-v11',
        initial_view_state=view_state2,
        layers=[layer2],
    )

st.pydeck_chart(map2)
st.write('' # provide map and logo separation
         ''
         ''
         ''
         ''
         ''
         '')
st.image('/Users/bryancalabrese/OneDrive - Bentley University/Spring 2022/CS 230/Project/Uber_logo.svg.png')
