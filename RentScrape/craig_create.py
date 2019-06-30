import re
import time
from requests import get
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from time import sleep
import pandas as pd
import csv
import numpy as np
from warnings import warn

#browser = webdriver.Chrome()
#wait = WebDriverWait(browser, 10)

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
df = pd.DataFrame()
#fix QR issue

#def craigs_roomrents(city='Provo'):
    #Gets roomrents with private room and picture
    #Used part of https://towardsdatascience.com/web-scraping-craigslist-a-complete-tutorial-c41cea4f4981
def craigs_roomrents(city='Provo'):
    city = city.replace(' ', '')
    url = 'https://'+ city + '.craigslist.org/search/roo?hasPic=1&availabilityMode=0&private_room=1'
    response = get(url)
    html_soup = BS(response.text, 'html.parser')
    results_total = int(html_soup.find('span', class_='totalcount').text)
    pages = np.arange(0, results_total+1, 120)
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
        posts = page_soup.find_all('li', class_='result-row')
        j=1
        k=1
        for i in posts:
            #price
            price = int(i.a.text.strip().replace('$',''))
            price_list.append(price)
            #title
            title_link = i.find('a', class_='result-title hdrlnk')
            title = title_link.text
            title_list.append(title)
            #link
            link = title_link['href']
            link_list.append(link)
            date = i.find('time', class_='result-date')['datetime']
            date_list.append(date)
            loc=i.find('span', class_='result-hood')
            if loc is None:
                location = 0
                location_list.append(location)
            elif loc is not None:
                location = loc.text
                location_list.append(location)
            housing_ft = i.find('span', class_='housing')
            if housing_ft is None:
                housing_ft = 0
            elif housing_ft is not None:
                housing_ft = re.search(r'(\w+)',housing_ft.text)[0]
            sqft_list.append(housing_ft)
            print('Done ' + str(j))
            j += 1
        for link in link_list:
            response = get(link)
            link_soup = BS(response.text,'html.parser')
            num_images = len(link_soup.find_all('div', class_='slide'))
            num_images_list.append(num_images)
            description = link_soup.find('section', id='postingbody').text.strip()
            #description_list.append(description)
            description_dict[link] = description
            description_list.extend(list(description_dict.values()))
            attr = link_soup.find('p', class_='attrgroup').findNext('p').text.strip().replace('\n\n', ',')
            attr_dict[link] = attr
            attr_list.extend(list(attr_dict.values()))
            #attr_list.append(attr)
            print('individual scrape successful: ' + str(k))
            k += 1
            sleep(randint(1,4))
    # Now Create a data set
    df = pd.DataFrame(link_list)
    for key, val in col_dict.items():
        df[key] = val
    df.to_csv('craigs_roomrents.csv')
    print('Created a Craigslist dataset')

        #get the first part of list name without _list
        #Then create columns
        #save as a csv file so that you can clean this more.
        # see how you can add to the dataset withou repeating




#other places to consider rentler.com, trulia.com, byu.uloop.com/housing/
