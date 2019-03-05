from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
delay = 5
def business_type():
""" With Selenium, accesses California recycling page for Commercial Streams by Business Group data.
Downloads 58 files for each counties """
    try:
        browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")
        try:
            for i in range(1,59):
                county = browser.find_element_by_name('CountyID')
                for option in county.find_elements_by_tag_name('option'):
                    if option.get_attribute('value')==str(i):
                        option.click()
                        break
                button = browser.find_element_by_id('SearchButton')
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "ExportToExcel")))
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")
                export = browser.find_element_by_id('ExportToExcel')
                export.click()
                time.sleep(delay)
                print("Downloaded " + str(i))
                browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")

        except NoSuchElementException:
            print("Error!")
            raise
    finally:
        print("Finish")

def residential_recycling():
""" With Selenium, accesses California recycling page for Residential Streams by Material Type data sets.
Downloads 58 files for each counties """
    try:
        browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")
        try:
            for i in range(1,59):
                county = browser.find_element_by_name('CountyID')
                for option in county.find_elements_by_tag_name('option'):
                    if option.get_attribute('value')==str(i):
                        option.click()
                        break
                types = browser.find_elements_by_name('startpage')
                for type in types:
                    if type.get_attribute('value')=="Residential":
                        type.click()
                button = browser.find_element_by_id('SearchButton')
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "ExportToExcel")))
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")
                export = browser.find_element_by_id('ExportToExcel')
                export.click()
                time.sleep(delay+2)
                print("Downloaded " + str(i))
                browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")

        except NoSuchElementException:
            print("Error!")
            raise
    finally:
        print("Finish")
def business_recycling():
""" With Selenium, accesses California recycling page for Commercial Streams by Material Type data.
Downloads 58 files for each counties """
    try:
        browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")
        try:
            for i in range(53,59):
                county = browser.find_element_by_name('CountyID')
                for option in county.find_elements_by_tag_name('option'):
                    if option.get_attribute('value')==str(i):
                        option.click()
                        break
                types = browser.find_elements_by_name('startpage')
                for type in types:
                    if type.get_attribute('value')=="CommByMatType":
                        type.click()
                button = browser.find_element_by_id('SearchButton')
                button.click()
                try:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "ExportToExcel")))
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")
                export = browser.find_element_by_id('ExportToExcel')
                export.click()
                time.sleep(delay+2)
                print("Downloaded " + str(i))
                browser.get("https://www2.calrecycle.ca.gov/WasteCharacterization/")

        except NoSuchElementException:
            print("Error!")
            raise
    finally:
        print("Finish")
