#%%
# Import the required modules for web scrapping and SQL connection

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import pprint
import pyodbc
import datetime

# Read the csv file which has the state details to be scrapped from redbus application

states_df = pd.read_csv("government_states.csv", index_col=False)

# Connection to SQL Server

con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
"Server=(localdb)\Local;"
"Database=Test;"
"Trusted_Connection=yes;")
cursor = con.cursor()

def getPageCount():
    """
    This menthod returns the number of pages in the selected route.
    """
    try:
        all_pageList = driver.find_elements(By.XPATH,"//div[contains(@class,'DC_117_pageTabs')]")
        element = driver.find_element(By.XPATH,"//div[@class = 'DC_117_pageTabs ']")
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except NoSuchElementException:
            return 0
    return len(all_pageList)

def get_page_data(ind):
    """
    This method fetches the route details and the corresponding route link

    """

    time.sleep(5)
    element = driver.find_element(By.XPATH, f"//div[contains(text(), {ind})]")
    driver.execute_script("arguments[0].click();", element)
    routes = driver.find_elements(By.XPATH, "//a[@class='route']")
       
    for route in routes:
        global bus_routes
        bus_routes.append([route.text, route.get_attribute("href")])


def getBusRouteDetails(state_link):
    """
    Method for calling page count and page data fetch request
    """
    driver.get(state_link)
    time.sleep(5)
    no_of_pages = getPageCount()

    print(f"Number of pages:{no_of_pages}")

    if(no_of_pages > 0):
        for ind in range(1, no_of_pages+1):
            data = get_page_data(ind)

def getBusDetails(bus_routes):
    """
    This method fetches all bus information for the routes passed

    """
    for route in bus_routes:
        print(route[0])
        print(route[1])
        print("Routing to bus_routes")
        driver.get(route[1])
        # driver.get("https://www.redbus.in/bus-tickets/hyderabad-to-vijayawada")
        time.sleep(10)
        try:
            driver.find_element(By.XPATH, "//div[contains(text(), 'View Buses')]").click()
        except NoSuchElementException:
             pass
        try:
            element_1 = driver.find_element(By.XPATH, f"//div[contains(text(), 'View Buses')]")
            driver.execute_script("arguments[0].click();", element_1)
        except NoSuchElementException:
             pass

        reached_page_end = False
        max_scroll = 50
        while not reached_page_end and max_scroll > 0:
            #print(max_scroll)
            html = driver.find_element(By.TAG_NAME, "html")
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.PAGE_DOWN)
            last_height = driver.execute_script("return document.body.scrollHeight") + 100
            new_height = driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                    reached_page_end = True
            else:
                    last_height = new_height
            max_scroll = max_scroll - 1
        all_buses = driver.find_elements(By.XPATH, "//li[@class='row-sec clearfix']")
        itration = 0
        print(f"No of Buses:{len(all_buses)}")
        for bus in all_buses:
            bus_details = {}
            itration = itration + 1
            #time.sleep(5)
            bus_details["route"] = route[0]
            bus_details["route_link"] = route[1]
            bus_name = bus.find_element(By.XPATH, ".//div[@class='travels lh-24 f-bold d-color']")
            bus_details["busname"] = bus_name.text
            bus_type = bus.find_element(By.XPATH, ".//div[@class='bus-type f-12 m-top-16 l-color evBus']")
            bus_details["bustype"] = bus_type.text
            bus_dptime = bus.find_element(By.XPATH, ".//div[@class='dp-time f-19 d-color f-bold']")
            bus_details["departing_time"] = bus_dptime.text
            bus_duration = bus.find_element(By.XPATH, ".//div[@class='dur l-color lh-24']")
            bus_details["duration"] = bus_duration.text
            bus_reachingtime = bus.find_element(By.XPATH, ".//div[@class='bp-time f-19 d-color disp-Inline']")
            bus_details["reaching_time"] = bus_reachingtime.text
            time.sleep(5)
            try:
                bus_price = bus.find_element(By.XPATH, ".//span[@class='f-bold f-19']")
                bus_details["price"] = bus_price.text          
            except NoSuchElementException:
                bus_price = bus.find_element(By.XPATH, ".//span[@class='f-19 f-bold']")
                bus_details["price"] = bus_price.text
            try:
                bus_seatavailablity = bus.find_element(By.XPATH, ".//div[@class='seat-left m-top-30']")
                bus_details["seats_available"] = bus_seatavailablity.text.split(' ')[0]          
            except NoSuchElementException:
                bus_seatavailablity = bus.find_element(By.XPATH, ".//div[@class='seat-left m-top-16']")
                bus_details["seats_available"] = bus_seatavailablity.text.split(' ')[0]
            try:
                bus_rating = bus.find_element(By.XPATH, ".//div[@class='rating-sec lh-24']")
                bus_details["star_rating"] = bus_rating.text
            except NoSuchElementException:
                bus_details["star_rating"] = 0.0

            global bus_list
            bus_list.append(bus_details)
            print(f"Completed for {itration}/{len(all_buses)} : {bus_name.text}")  

def truncate_table(table_name):
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    con.commit()

def save_route_data(redbus_data):
    print("Save Part")
    truncate_table('bus_routes')
    bus_list_df = pd.DataFrame(redbus_data)

    for index, row in bus_list_df.iterrows():

        row.departing_time = datetime.datetime.combine(datetime.date.today(),
                            datetime.time(int(row.departing_time.split(':')[0]), int(row.departing_time.split(':')[1])))
   
        row.reaching_time = datetime.datetime.combine(datetime.date.today(),
                            datetime.time(int(row.reaching_time.split(':')[0]), int(row.reaching_time.split(':')[1])))
   
        cursor.execute(
            """
            INSERT INTO bus_routes (
            route_name,
            route_link,
            busname,
            bustype,
            departing_time,
            duration,
            reaching_time,
            star_rating,
            price,
            seats_available
            )
            VALUES
            (?,?,?,?,?,?,?,?,?,?)
            """
            ,row.route
            ,row.route_link
            ,row.busname
            ,row.bustype
            ,row.departing_time
            ,row.duration
            ,row.reaching_time
            ,row.star_rating
            ,row.price
            ,row.seats_available
        )


# Home page
   
driver = webdriver.Chrome()
driver.get("https://www.redbus.in/")
driver.maximize_window()
time.sleep(5)
body = driver.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.PAGE_DOWN)
body.send_keys(Keys.PAGE_DOWN)
time.sleep(5)

bus_routes = []
bus_list = []

# Front page navigation

for ind in states_df.index:
    state = states_df['StateCode'][ind]
    print(f"Running for {state}")
    state_link = f"https://www.redbus.in/online-booking/{state}/?utm_source=rtchometile"
    print(state_link)
    getBusRouteDetails(state_link)
    time.sleep(2)
    getBusDetails(bus_routes)


save_route_data(bus_list)
#
# # Create table script

#%%
# cursor.execute(
#             """
#                CREATE TABLE bus_routes_temp
#                (
#                id int IDENTITY(1,1) PRIMARY KEY,
#                route_name nvarchar(500),
#                route_link nvarchar(500),
#                busname nvarchar(100),
#                bustype nvarchar(100),
#                departing_time DATETIME,
#                duration nvarchar(100),
#                reaching_time DATETIME,
#                star_rating float,
#                price decimal,
#                seats_available int
#                )
#                """
# )
# #%%
# con.commit

# %%
