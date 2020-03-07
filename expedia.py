# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 20:02:47 2020

@author: lundr
"""


import pandas as pd
from datetime import datetime
from datetime import date
import boto3
import os
 
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pandas as pd
import time

from config import ACCESS_KEY,SECRET_KEY

st = datetime.now()
    


days = list(range(1,32))
month = [3,4,5,6,7,8,9,10,11,12]
year = 2020


df = pd.DataFrame(columns = ['date', 'airline','route','time','price'])
for j in month:
    
    print('month:'+ str(j))

    for i in days:
      
        try:
            if  datetime(year, j,i) < datetime.now():
                pass
            else:
            
                print('day:'+ str(i))
                
                if len(str(i))==1:
                    a='0'+str(i)
                else:
                    a = str(i)
                    
                    
                if len(str(j))==1:
                    m='0'+str(j)
                else:   
                    m = str(j)
                    
                date_stamp = m +'%2F'+ a+ '%2F'+ str(year)
                date_clean = m+"-"+a+"-"+str(year)
                
                dep = 'London'
                arr = 'Zurich'
                
                
                # london - zurich
                u = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=" + date_stamp +"&mode=search&trip=oneway&leg1=from%3A" + dep+"%2C+England%2C+UK+%28LON-All+Airports%29%2Cto%3A"+arr+"%2C+Switzerland+%28ZRH%29%2Cdeparture%3A" + date_stamp +"TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
             
              
                
                #https://www.expedia.com/Flights-Search?flight-type=on&starDate=03%2F02%2F2020&mode=search&trip=oneway&leg1=from%3ALondon%2C+England%2C+UK+%28LON-All+Airports%29%2Cto%3AZurich%2C+Switzerland+%28ZRH%29%2Cdeparture%3A03%2F02%2F2020TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY
              
                
                driver = webdriver.Chrome('C:/Users/lundr/Downloads/chromedriver_win32/chromedriver.exe')
                driver.get(u)
                time.sleep(10)
                
                
               
                # click x to close pop up
                try:
                    driver.find_element(By.XPATH,'//img[@class = " needsclick"]').click()
                except:
                    pass
                
                
                
                
                prices = driver.find_elements_by_xpath('//span[@class = "full-bold no-wrap"]')
                
                departure = driver.find_elements_by_xpath('//span[@class  = "medium-bold"]')
                airline = driver.find_elements_by_xpath('//span[@data-test-id  = "airline-name"]')
                route = driver.find_elements_by_xpath('//div[@class  = "secondary-content no-wrap"]')
                
                
        
            
                
                for k in range(len(prices)):
                  
                   df2 = pd.DataFrame([[date_clean, airline[k+1].text,route[k].text, departure[k].text,prices[k].text]], columns = ['date','airline','route','time','price'])
                   print(df2)
                   df = df.append(df2, ignore_index = True)
                
                
                
                print('length df:' + str(df.shape[0]))
                time.sleep(10)
                
                driver.close()
                
        except:
                pass
df['extraction_date'] = datetime.now()



write_path='expedia_data/expedia.com_pm'+dep+"_"+arr+str(date.today())+'.txt'
df.to_csv(write_path, sep='\t', index=False)
    
### send data to S3 bucket    



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

os.remove(write_path)
print(datetime.now() - st)