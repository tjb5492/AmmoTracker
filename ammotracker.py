from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time
from multiprocessing import Process
import smtplib
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')

# Email Variables
gmail_email = ''
gmail_password = ''
to_email =''

# Ammo URLS
brownells_9mm_magtech_url = r"https://www.brownells.com/ammunition/handgun-ammo/9mm-luger-115gr-full-metal-case-50-box-" \
                           r"sku105201571-95196-95626.aspx?"
simmons_9mm_blazer_url = r'https://www.simmonssportinggoods.com/blazer-brass-ammunition-9mm-luger-115-grain-full-metal-jacket-50-per-box/'
simmons_9mm_blazer_124_url = r'https://www.simmonssportinggoods.com/blazer-brass-ammunition-9mm-luger-124-grain-full-metal-jacket-50-per-box/'
federal_9mm_url = r'https://www.federalpremium.com/handgun/american-eagle/american-eagle-handgun/11-AE9AP.html'

# Chrome variables
cpath = r''
driver = webdriver.Chrome(cpath,options=options)

def send_email(site,url):

   with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
       smtp.ehlo()
       smtp.starttls()
       smtp.ehlo()

       smtp.login(gmail_email,gmail_password)
       subject = 'Ammo In Stock'
       body = 'Ammo is in stock at ....' + str(site) + '\nURL = ' + url

       msg = f'Subject: {subject}\n\n{body}'
       smtp.sendmail(gmail_email, to_email, msg)


def brownells():
    driver.get(brownells_9mm_magtech_url)
    while True:
        try:
           time.sleep(5)
           driver.find_element(By.XPATH, "//div[contains(.,'Alert Me When Available')]")
           print('9mm out of stock at Brownells')
           driver.refresh()
        except NoSuchElementException:
            print('9mm Brownells...Item in Stock!')
            print('Getting the web address')
            web_address = driver.current_url
            send_email('Brownells',web_address)
            print('Email SENT!!!')


def federal():
    driver.get(federal_9mm_url)
    while True:
        try:
           time.sleep(5)
           driver.find_element(By.XPATH, "//div[contains(.,'Currently Unavailable')]")
           print('9mm out of stock at Federal')
           driver.refresh()
        except NoSuchElementException:
            print('9mm Federal...Item in Stock!')
            print('Getting the web address')
            web_address = driver.current_url
            send_email('Federal',web_address)
            print('Email SENT!!!')

def simmons():

    while True:
        try:
           time.sleep(5)
           driver.get(simmons_9mm_blazer_url)
           driver.find_element(By.XPATH, "//div[contains(.,'Sorry but this item is currently unavailable.')]")
           print('9mm out of stock at Simmons')
        except NoSuchElementException:
            print('9mm Simmons...Item in Stock!')
            print('Getting the web address')
            web_address = driver.current_url
            send_email('Simmons',web_address)
            print('Email SENT!!!')
        try:
            driver.get(simmons_9mm_blazer_124_url)
            driver.find_element(By.XPATH, "//div[contains(.,'Sorry but this item is currently unavailable.')]")
            print('9mm out of stock at Simmons')
        except NoSuchElementException:
            print('9mm Simmons...Item in Stock!')
            print('Getting the web address')
            web_address = driver.current_url
            send_email('Simmons', web_address)
            print('Email SENT!!!')





if __name__ == '__main__':
    p1 = Process(target =simmons)
    p1.start()
    p2 = Process(target = brownells)
    p2.start()
    p3 = Process(target=federal)
    p3.start()
