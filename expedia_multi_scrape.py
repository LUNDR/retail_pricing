# -*- coding: utf-8 -*-
"""
@author: lundr
"""

"""
To set up on Ubuntu:
    
sudo apt install python3 python3-dev python3-venv
sudo apt-get install python3-pip
mkdir scrape
cd scrape
python3 -m venv venv
source venv/bin/activate
pip install selenium
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get -f --yes install
sudo dpkg -i google-chrome-stable_current_amd64.deb
https://sites.google.com/a/chromium.org/chromedriver/downloads
wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
sudo apt-get install unzip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
sudo apt-get install -y xvfb
pip install pandas 
pip install pyvirtualdisplay

https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/
https://launchpad.net/ubuntu/trusty/+package/chromium-chromedriver
"""

# import python packages
import itertools
from datetime import datetime
from datetime import date
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import boto3
import os
import time

# import credentials for upload to S3
from config import ACCESS_KEY,SECRET_KEY

# define useful functions

def s3_upload(access_key,secret_key, write_path):
    
    s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    )
    bucket_resource = s3
    
    filename = write_path
    
    bucket_resource.upload_file(
    Bucket = 'retailscrapes',
    Filename=filename,
    Key=filename
    )
    
# define global variables

## record time script started running
st = datetime.now()

# define path to chrome driver and chrome options

## set depending on where you installed chromedriver
chromedriver_path = '/usr/lib/chromium-browser/chromedriver'
chromedriver_path = '/usr/bin/chromedriver'

display = Display(visible=0, size=(1920, 1080))
display.start()
options = webdriver.ChromeOptions()

## set lists of days, months and years to cycle through

dayList = list(range(1,32))
monthList = list(range(3,13))
yearList = [2020]

# set places to search for as needed for url
London = 'London+%28LON-All+Airports'
NY = 'New+York+%28NYC-All+Airports'
Zurich = 'Zurich%2C+Switzerland+%28ZRH-Zurich'
Paris = 'Paris+%28PAR-All+Airports'
#Dubai = 'Dubai+%28DXB-All+Airports'
#Dublin = 'Dublin+%28DUB-Dublin'
#Madrid = 'Madrid+%28MAD-All+Airports'
#Istanbul = 'Istanbul+%28IST-All+Airports'
#Rio = 'Rio+de+Janeiro+%28RIO-All+Airports'

places = [London, NY, Zurich, Paris]
df = pd.DataFrame(columns = ['date', 'airline','route','time','price'])


# generate list of day, month, year tuples in the correct format for the url
dates = []
base = datetime.datetime.today()
for i in range(1,275):
    dt = base + datetime.timedelta(days=i)
    d = f"{dt.day:02d}"
    m = f"{dt.month:02d}"
    y = f"{dt.year:04d}"
    dt_tup = (d,m,y)
    dates.append(dt_tup)
        			


for pair in itertools.permutations(places, r=2):
    with webdriver.Chrome(chromedriver_path, options=options) as driver:
        for x in dates:
            try:
                 date_stamp = x[1] +'%2F'+ x[0] + '%2F'+ x[2]
                 date_clean = x[1] + "-" + x[0] + "-" + x[2]
                 dep = pair[0]
                 arr = pair[1]
                 
                 dep_name = dep.split('+',1)[0]
                 arr_name = arr.split('+',1)[0]
                 
                 u = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=" + date_stamp +"&mode=search&trip=oneway&leg1=from%3A" + dep+"%29%2Cto%3A"+arr+"%29%2Cdeparture%3A" + date_stamp +"TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
         
                 driver.get(u)      
                 time.sleep(10)
         					
         			# click x to close pop up
                 try:
                     driver.find_element(By.XPATH,'//img[@class = " needsclick"]').click()
                 except:
                     pass
                 
                 prices = driver.find_elements_by_xpath('//span[@class = "full-bold no-wrap"]')
                 print(prices)
                 departure = driver.find_elements_by_xpath('//span[@class  = "medium-bold"]')
                 airline = driver.find_elements_by_xpath('//span[@data-test-id  = "airline-name"]')
                 route = driver.find_elements_by_xpath('//div[@class  = "secondary-content no-wrap"]')
 			
                 for k in range(len(prices)):
                     df2 = pd.DataFrame([[date_clean, airline[k+1].text,route[k].text, departure[k].text,prices[k].text]], columns = ['date','airline','route','time','price'])
                     print(df2)
                     df = df.append(df2, ignore_index = True)
                     print('length df:' + str(df.shape[0]))
                 time.sleep(10)
            except:
                    pass		
    
    df['extraction_date'] = datetime.now()
    write_path='expedia_data/'+dep+"_"+arr+str(date.today())+'.tsv'
    df.to_csv(write_path, sep='\t', index=False)
    
    
    os.remove(write_path)
    print(datetime.now() - st)

