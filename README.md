# redbus
Redbus Data Scraping and Filtering with Streamlit Application

The "Redbus Data Scraping and Filtering with Streamlit Application" aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry

## Dependancies

* Python 3.11
* pandas
* pyodbc
* selenium
* datetime
* streamlit

  **NOTE**: Version details for above python packages are mentioned in *requirements.txt*.

## Setup and install

 python package installation commands. 
 * pip install pandas
 * pip install selenium
 * pip install streamlit
 * pip install pyodbc

 ### Import and Connect
 
  import pandas as pd
  from selenium import webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.common.keys import Keys

# File: redbus_web_scrapping.py
This file fetches 10 state bus details into bus_routes table.

## getPageCount
This menthod returns the number of pages in the selected route

## get_page_data
This method fetches the route details and the corresponding route link

##### Parameters
* **ind** (Mandatory) - Refers the page number where the route details has to be fetched

## getBusRouteDetails
Method to get the page count and route details.

##### Parameters
* **state_link** (Mandatory) - Get the state link to get the page and route details

## getBusDetails
This method fetches all bus information for the routes passed

##### Parameters
* **bus_routes** (Mandatory) - Get all bus routes to get the bus details

# File: redbus_streamlit.py
This file has the implementation of web page for user to get the required details about buses.

## get_results
This method makes the request with SQL DB to get the required details based on user filter. It will be called when 
user makes the search request from application.

##### Parameters
* **route** (Mandatory) - User selected Route Name from streamlit application
* **seat_type** (Mandatory) - User selected bus Seat type from streamlit application
* **ac_type** (Mandatory) - User selected bus ac type from streamlit application
* **rating** (Mandatory) - User selected rating of the bus from streamlit application
* **startting_time** (Mandatory) - User selected starting time of the bus from streamlit application
* **min_selected_price** (Mandatory) - User selected minimum price for the bus from streamlit application
* **max_selected_price** (Mandatory) - User selected maximum proce for the bus from streamlit application

# File: government_states.csv
This file has 10 states from the redbus application

# Python file running:

python redbus_web_scrapping.py

# Streamlit file running:

streamlit run redbus_streamlit.py

# Output:

Statewise data will be stored in bus_routes table
 
