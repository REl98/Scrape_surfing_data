import os
from General_functions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import os
import time
import pandas as pd
import numpy as np


def scrape_wind_direction(browser):
    """
    Function scripe wind direction data from the website
    and it return an html code
    """
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    soup2 = soup.select('tr[id*="tabid_2_0_SMER"]')
    df = pd.DataFrame([str(p) for p in soup2], dtype=object)
    df.to_csv('file1.csv')
    with open('file1.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        vData = []
        for i, line in enumerate(f):
            if i == 2:  # Read only the second line in file1.csv that contain the wind direction
                vData.append(line.strip())
            elif i > 2:
                break
    return vData


def extract_wind_direction(vData):
    """
    Function that receive the data in html format
    and extract the wind directions from it and store it in a list
    """
    splitdata = vData[0].split("span")
    splitdata2 = []
    for e in splitdata:
        if "title" in e:
            splitdata2.append(e[8:19])
        else:
            pass
    return splitdata2


def Retrieving_data(vData, browser):
    """
    Function that make sure we scrape data from the website ,
    if the first try did not success , it will try untill we scrape the data
    after each try , it will sleep 5 seconds and then try again .
    """
    while (len(vData) <= 0):
        print("Retrieving Data within 5s, be patient !")
        time.sleep(5)
        vData = scrape_wind_direction(browser)
    splitData = extract_wind_direction(vData)
    splitData = [e.replace('"', "").strip() for e in splitData]
    return splitData


def initialize_parameters(container):
    """
    Function that receive data in html format
    and we extract wind speed, wind gusts, date and temperature
    we return wind speed, wind gusts, date and temperature
    """
    dateAndTime = None
    winSpeed = None
    winGusts = None
    Temp = None
    for e in container:
        try:
            dateAndTime = e.find_element(By.CSS_SELECTOR, '#tabid_2_0_dates').text
            winSpeed = np.asarray(e.find_element(By.CSS_SELECTOR, '#tabid_2_0_WINDSPD').text)
            winGusts = np.asarray(e.find_element(By.CSS_SELECTOR, '#tabid_2_0_GUST').text)
            Temp = np.asarray(e.find_element(By.CSS_SELECTOR, '#tabid_2_0_TMPE').text)
        except:
            pass
    res = [dateAndTime, winSpeed, winGusts, Temp]
    return res


def extract_day_month_hour(dateAndTime):
    """
    Function that receive data of date extract
    dats, date and hours
    :param dateAndTime:
    :return:
    """
    string_data = ["".join(str(e) for e in dateAndTime)]
    final_date = [e.replace("\n", "").split(" ") for e in string_data][0]
    days = [e[:2] for e in final_date]
    date = [str(e[2:3]).zfill(2) for e in final_date]
    hour = [e[-3:] for e in final_date]
    return days, date, hour


def create_data_frame(arr):
    """
    Function that receive a list with a mess data ,
    it will recollect the data perfectly and send it back
    """
    temp = []
    for i in range(len(arr)):
        if i + 1 < len(arr):
            if arr[i] and arr[i + 1] != '':
                temp.append(arr[i] + arr[i + 1])
            else:
                if arr[i] == '' and arr[i + 1] != '':
                    if i + 2 < len(arr):
                        if arr[i + 2] == '':
                            temp.append(arr[i + 1])
                        else:
                            i += 1
                    else:
                        temp.append(arr[i + 1])
    return temp


# web url to scrap the data from :
URL = "https://www.windguru.cz/885370"

# User-Agent --> Find Your User-Agent: https://httpbin.org/get
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"

# Connecting Edge browser --Beginning
edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver')
edge_service = Service(edge_driver_path)
edge_options = Options()
edge_options.add_experimental_option('detach', True)
edge_options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Edge(service=edge_service, options=edge_options)
browser.get(URL)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
# Connecting Edge browser --End

vData = scrape_wind_direction(browser)
# Retrieving Data and splitting ---- Beginning
wind_direction = Retrieving_data(vData, browser)
# Retrieving Data and splitting ---- End #

# Fetching the data by selecting the father element by using class name
container = wait(browser, 25).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tabulka')))

# Save Parameters
dateAndTime, winSpeed, winGusts, Temp = initialize_parameters(container)
# ----------------

# split the date for month, day and an hour
days, date, hour = extract_day_month_hour(dateAndTime)

winSpeed = winSpeed.tolist()
winSpeed = [e.strip() for e in winSpeed]
winSpeed = create_data_frame(winSpeed)

winGusts = winGusts.tolist()
winGusts = [e.strip() for e in winGusts]
winGusts = create_data_frame(winGusts)

Temp = Temp.tolist()
Temp = [e.strip() for e in Temp]
Temp = create_data_frame(Temp)

data = [days, date, hour, winSpeed,
        winGusts, Temp, wind_direction]
columns = ["Day       : ",
           "Date      : ",
           "Hour      : ", 'Wind speed: ',
           'Wind gusts: ', 'Temp (°C) : ',
           'Wind Direction:']

df = pd.DataFrame(data, index=columns)
df.to_csv(f'{os.path.join(os.getcwd())}/out.csv', sep='\t', header=False, encoding='utf-8')

winSpeed = np.asarray(winSpeed)
winGusts = np.asarray(winGusts)
Temp = np.asarray(Temp)

idx = get_index(str(extract_time())[:2]+'h', hour)
sms = (write_sms(winSpeed, winGusts, Temp, wind_direction, idx))