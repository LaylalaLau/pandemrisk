from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup

with open('geo-data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(row)

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/Users/lzy/bin/chromedriver')

url = "https://www.eventbrite.com/directory/sitemap/"
driver.get(url)

elements = driver.find_elements_by_css_selector(".panel_head2")
e_groups = [el.find_elements_by_css_selector(".g-group") for el in elements if el.find_element_by_css_selector("h2").text == "United States"]
e_links_nested = [[el.find_elements_by_css_selector(".g-cell") for el in els] for els in e_groups]
e_links = [e.find_element_by_css_selector("a").get_attribute("href") for els in e_links_nested for el in els for e in el]

print(e_links)

from numpy import NaN
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pandas as pd


def WHOData(countryName):
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'    
    response = urlopen(url)
    df = pd.read_json(url)
    df = df.transpose()
    index = pd.Series(range(len(df)))
    df = df.set_index(index)

    countryData = {'location':[],'date':[],'new_cases':[],'new_deaths':[], \
            'people_vaccinated':[],'population_density':[]}
    for d in df.loc[df['location'] == countryName]['data'][0]:
        countryData['location'].append(countryName)
        countryData['date'].append(d['date'])
        if 'new_cases' in d.keys():
            countryData['new_cases'].append(d['new_cases'])
        else:
            countryData['new_cases'].append(NaN)
        if 'new_deaths' in d.keys():
            countryData['new_deaths'].append(d['new_deaths'])
        else:
            countryData['new_deaths'].append(NaN)
        if 'people_vaccinated' in d.keys():
            countryData['people_vaccinated'].append(d['people_vaccinated'])
        else:
            countryData['people_vaccinated'].append(NaN)
        if 'population_density' in d.keys():
            countryData['population_density'].append(d['population_density'])
        else:
            countryData['population_density'].append(NaN) 
    countryData = pd.DataFrame(countryData)
    # print(countryData)

    # calculate the score
    score = 0
    df_score = countryData.copy()
    df_score = df_score.fillna(0)
    df_score['score'] = df_score.index * (df_score.new_cases + df_score.new_deaths + df_score.people_vaccinated + df_score.population_density) / 10000
    score = sum(df_score['score']) / 100000

    return countryData, score


def freshCDCData(stateName):  
    
    # make sure to install these packages before running:
    # pip install pandas
    # pip install sodapy

    #!/usr/bin/env python
    """
    from sodapy import Socrata

    # The user needs to have an app token and a Socrata account to get fresh data from the CDC website
    client = Socrata("data.cdc.gov",
                     "MyAppToken",
                     username="user@example.com",
                     password="AFakePassword")

    results = client.get("9mfq-cb36", limit=80000000000000000000000000)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    df['state'] = df['state'].astype(str)
    df.new_case = df['new_case'].astype(float)
    df.new_death = df['new_death'].astype(float)
    df.submission_date = df['submission_date'].astype(str)
    df.submission_date = df.submission_date.replace({'T00:00:00.000':''}, regex=True)
    """
     # Read data from file into dataframe
    df = pd.read_csv('United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
    
    # Clean the data and retireve based on state
    df.submission_date = df.submission_date.replace({'T00:00:00.000':''}, regex=True)
    stateData = df.loc[df['state'] == stateName][['submission_date', 'state', 'tot_cases', 'new_case', 
                                                  'tot_death', 'new_death']]
    stateData = stateData.sort_values(by=['submission_date'])
    index = pd.Series(range(len(stateData)))
    stateData = stateData.set_index(index)
    stateData['score'] = stateData.index * (stateData.new_case + abs(stateData.new_death)) / 10000
    
    score = sum(stateData['score']) / 50
    
    return stateData[['submission_date', 'state', 'tot_cases', 'new_case', 
                                                  'tot_death', 'new_death']], score
