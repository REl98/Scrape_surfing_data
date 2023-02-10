# Import libraries :-
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


class ScrapeData:
    def __init__(self, url, user_agent):
        self.URL = url
        self.USER_AGENT = user_agent
        self.edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver')
        self.edge_service = Service(self.edge_driver_path)
        self.edge_options = Options()
        self.edge_options.add_experimental_option('detach', True)
        self.edge_options.add_argument(f'user-agent={self.USER_AGENT}')
        self.browser = webdriver.Edge(service=self.edge_service, options=self.edge_options)
        self.browser.get(self.URL)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.container = wait(self.browser, 25).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tabulka')))


    def scrape_wind_direction(self, browser):
        """
        Function scripe wind direction data from the website
        and it return an html code
        """
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        soup2 = soup.select('tr[id*="tabid_2_0_SMER"]')
        df = pd.DataFrame([str(p) for p in soup2], dtype=object)
        df.to_csv('Directions.csv')
        with open('Directions.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            vData = []
            for i, line in enumerate(f):
                if i == 2:  # Read only the second line in Directions.csv that contain the wind direction
                    vData.append(line.strip())
                elif i > 2:
                    break
        return vData


    def extract_wind_direction(self, vData):
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


    def Retrieving_data(self, vData, browser):
        """
        Function that make sure we scrape data from the website ,
        if the first try did not success , it will try untill we scrape the data
        after each try , it will sleep 5 seconds and then try again .
        """
        while (len(vData) <= 0):
            print("Retrieving Data within 5s, be patient !")
            time.sleep(5)
            vData = self.scrape_wind_direction(browser)
        splitData = self.extract_wind_direction(vData)
        splitData = [e.replace('"', "").strip() for e in splitData]
        return splitData


    def initialize_parameters(self, container):
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


    def extract_day_month_hour(self, dateAndTime):
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


    def create_data_frame(self, arr):
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


    def initiate_scrape(self):
        vData = self.scrape_wind_direction(self.browser)
        # Retrieving Data and splitting ---- Beginning
        wind_direction = self.Retrieving_data(vData, self.browser)
        # Retrieving Data and splitting ---- End #
        dateAndTime, winSpeed, winGusts, Temp = self.initialize_parameters(self.container)
        days, date, hour = self.extract_day_month_hour(dateAndTime)
        winSpeed = winSpeed.tolist()
        winSpeed = [e.strip() for e in winSpeed]
        winSpeed = self.create_data_frame(winSpeed)

        winGusts = winGusts.tolist()
        winGusts = [e.strip() for e in winGusts]
        winGusts = self.create_data_frame(winGusts)

        Temp = Temp.tolist()
        Temp = [e.strip() for e in Temp]
        Temp = self.create_data_frame(Temp)

        data = [days, date, hour, winSpeed,
                winGusts, Temp, wind_direction]
        columns = ["Day       : ",
                   "Date      : ",
                   "Hour      : ", 'Wind speed: ',
                   'Wind gusts: ', 'Temp (°C) : ',
                   'Wind Direction:']

        df = pd.DataFrame(data, index=columns)
        df.to_csv(f'{os.path.join(os.getcwd())}/Data.csv', sep='\t', header=False, encoding='utf-8')

        winSpeed = np.asarray(winSpeed)
        winGusts = np.asarray(winGusts)
        Temp = np.asarray(Temp)
        idx = get_index(str(extract_time())[:2] + 'h', hour)
        sms = (write_sms(winSpeed, winGusts, Temp, wind_direction, idx))
        print(sms)
