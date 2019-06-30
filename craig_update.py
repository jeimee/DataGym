import re
import time
from requests import get
from bs4 import BeautifulSoup as BS
from random import randint
from time import sleep
import pandas as pd
import csv

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
    df = pd.read_csv('craigs_roomrents.csv')
    latest_date = df['date'].max()
