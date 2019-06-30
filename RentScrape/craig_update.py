import re
import time
from requests import get
from bs4 import BeautifulSoup as BS
from random import randint
from time import sleep
import pandas as pd
import csv
import numpy as np

title_list = []
link_list = []
price_list = []
date_list = []
location_list = []
sqft_list = []
num_images_list = []
description_dict = {}
attr_dict = {}
attr_list = []
description_list = []
col_dict = {'title': title_list,
            'price': price_list,
            'date': date_list,
            'sqfeet': sqft_list,
            'num_images': num_images_list,
            'description': description_list,
            'attributes': attr_list}

def update_craigs(city='Provo'):
    city = city.replace(' ', '')
    url = 'https://'+ city + '.craigslist.org/search/roo?hasPic=1&availabilityMode=0&private_room=1'
    response = get(url)
    html_soup = BS(response.text, 'html.parser')
    results_total = int(html_soup.find('span', class_='totalcount').text)
    pages = np.arange(0, results_total+1, 120)
    df = pd.read_csv('craigs_roomrents_' + city + '.csv')
    latest_date = df['date'].max()
    for page in pages:
        response = get('https://'
        + city
        + '.craigslist.org/search/roo?'
        + 's='
        + str(page)
        + '&hasPic=1'
        + '&availabilityMode=0'
        + '&private_room=1')
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests,response.status_code))
        page_soup = BS(response.text, 'html.parser')
        dates = html_soup.find_all('time', class_='result-date')
        for d in dates:
            date_list.append(d['datetime'])
        # only keep dates greater than latest_date
        new_date_list = [i for i in date_list if i > latest_date]
        if len(new_date_list) == 0:
            print('No craigslist updates in page ' + str(page))
            if page != pages[-1]:
                continue
            elif page == pages[-1]:
                break
        elif len(new_date_list) > 0:
                # only get stuff that matches the dates greater than latest_date
