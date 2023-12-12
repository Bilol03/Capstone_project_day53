import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

RENT_LINK = 'https://appbrewery.github.io/Zillow-Clone/'
FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSec1ng5347qMDI865TO83vXqILnb-zHnSSC2ZqqtVjhaofxRw/viewform?usp=sf_link'

class Capstone:
    def __init__(self):
        self.response = requests.get(RENT_LINK)
        self.soup = bs(self.response.content, 'html.parser')
        
    def find_all_links(self):
        all_links = []
        links = self.soup.find_all('a', class_='property-card-link')
        for link in links:
            all_links.append(link.get('href'))
        return all_links
    
    def find_all_prices(self):
        all_prices = []
        prices = self.soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')
        for price in prices:
            if ',' in price.getText():
                all_prices.append(price.getText()[0:6])
            else:
                all_prices.append(price.getText()[0:5])
        return all_prices
    
    def get_address(self):
        all_adresses = []
        adresses = self.soup.find_all('address')
        for adress in adresses:
            all_adresses.append(adress.getText().replace('\n ', '').replace(" ", ""))
        
        return all_adresses
    
    def fill_form_auto(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(FORM_LINK)
        
        # time.sleep(5)
        
        input = browser.find_elements(By.CSS_SELECTOR, '.Xb9hP input')
        button = browser.find_elements(By.CLASS_NAME, 'l4V7wb')
        
        find_all_links = self.find_all_links()
        find_all_prices = self.find_all_prices()
        get_address = self.get_address()
        
        for i in range(0, len(find_all_links) - 1):
            time.sleep(3)
            
            input = browser.find_elements(By.CSS_SELECTOR, '.Xb9hP input')
            button = browser.find_elements(By.CLASS_NAME, 'l4V7wb')
            input[0].send_keys(find_all_links[i])
            input[1].send_keys(find_all_prices[i])
            input[2].send_keys(get_address[i])
            
            button[0].click()
            time.sleep(4)
            browser.refresh()
        

capstone = Capstone()
capstone.fill_form_auto()
