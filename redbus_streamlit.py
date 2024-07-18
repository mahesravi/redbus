# Import the required modules for web scrapping and SQL connection

import streamlit as st
import pyodbc
import pandas as pd
import datetime

# Connection to SQL Server

con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
          "Server=(localdb)\\Local;"
          "Database=Test;"
          "Trusted_Connection=yes;")
cursor = con.cursor()

df = pd.DataFrame()


def get_results(route, seat_type, ac_type, rating, startting_time):
  """
  Button click event - Search

  """
  rating_value = 1

  if (rating):
    rating_value = rating.split('&')[0]

  str_time = str(startting_time)

  bus_time = datetime.datetime.combine(datetime.date.today(), datetime.time(
    int(str_time.split(':')[0]), int(str_time.split(':')[1])))

  script = f"""
   select LEFT(route_name, CHARINDEX(' ', route_name + ' ') -1) [From],
   STUFF(route_name, 1, Len(route_name) +1- CHARINDEX(' ',Reverse(route_name)), '') [To],
	  busname as [Bus Name],
	  price as [Bus Fare],
	  star_rating as Rating,
	  bustype as [Bus Type],
	  departing_time as [Starting Time],
	  reaching_time as [Reaching Time],
	  duration as [Duration],
	  concat(str(seats_available), ' Seats available') as [Seat Avalablity]
   from bus_routes
   where route_name='{route}'
   and bustype like '%{seat_type}%'
   and bustype like '%{ac_type}%'
   and star_rating > {rating_value}
   and departing_time > '{bus_time}'
   """

  global df
  df = pd.read_sql(script, con)
  df.reset_index(drop=True)


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

logo, title = st.columns([1, 6])

with logo:
  st.image('logo_1.png', width=100)

with title:
  st.markdown(
    "<h4 style='text-align: center; color: #800000;'>Redbus - India's No. 1 Online Bus Ticket Booking Site</h4>",
    unsafe_allow_html=True)

# Adjust the width ratios as per your layout

col1, col2, col3 = st.columns([3, 3, 3])
with col1:
  route_filter = cursor.execute("Select distinct route_name from bus_routes")
  routes = [row[0] for row in cursor.fetchall()]
  route = st.selectbox(
    "Select the Route",
    index=None,
    placeholder="Choose an option",
    options=routes,
  )
with col2:
  seat_type = st.selectbox(
    "Select the Seat Type",
    index=None,
    placeholder="Choose an option",
    options=[
      'Seater',
      'Sleeper'])
with col3:
  ac_type = st.selectbox(
    "Select the AC Type",
    index=None,
    placeholder="Choose an option",
    options=[
      'AC',
      'Non-AC'])

col4, col5, col6 = st.columns([3, 3, 3])

with col4:
  rating = st.selectbox(
    "Select the Rating",
    index=None,
    placeholder="Choose an option",
    options=[
      '4 & Above',
      '3 & Above',
      '2 & Above',
      '1 & Above'])
with col5:
  startting_time = st.time_input("Starting Time")
with col6:
  price_filter = cursor.execute(f"Select price from bus_routes")
  price = [row[0] for row in cursor.fetchall()]
  min_price = min(price)
  max_price = max(price)
  price_range = st.slider(
    "Select a Price Range",
    int(min_price),
    int(max_price),
    (int(min_price / 2), int(max_price / 2)))

button_state = st.button(
  "Search",
  on_click=get_results(
    route,
    seat_type,
    ac_type,
    rating,
    startting_time))
if (button_state):
  st.dataframe(df)