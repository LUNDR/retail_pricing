# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:51:53 2020

@author: lundr
"""


import boto3
import pandas as pd
from io import StringIO
import numpy as np
from datetime import time
from datetime import datetime
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

from config import ACCESS_KEY,SECRET_KEY

# bespoke functions

def make_dep_time(x):
    
    """ function to extract arrival time and convert to datetime object
        args: string of flight time
    
    """ 
    
    if 'pm' in x.split('-',1)[0]:
        a = x.split('pm',1)[0]
        
        if int(a.split(':')[0])>11:
            hour = int(a.split(':')[0])
        else:
            hour= int(a.split(':')[0])+12
        b = time(hour=hour,minute=int(a.split(':')[1]))
    else:
        a = x.split('am',1)[0]
        b = time(hour=int(a.split(':')[0]),minute=int(a.split(':')[1] ))
    return b

def make_arr_time(x):
    
    """ function to extract arrival time and convert to datetime object
        args: string of flight time
    
    """ 
    
    k = x.split('-',1)[1]
    if 'pm' in k :
        a = k.split('pm',1)[0]
    else:
        a = k.split('am',1)[0]
    b = time(hour=int(a.split(':')[0]),minute=int(a.split(':')[1] ))
    return b

def ListFiles(client,_BUCKET_NAME,_PREFIX):
    
    """List files in specific S3 URL"""
    
    response = client.list_objects(Bucket=_BUCKET_NAME, Prefix=_PREFIX)
    for content in response.get('Contents', []):
        yield content.get('Key')


if __name__ == "__main__":

    # create list of filenames
    
    s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    )
    
    objt = s3.list_objects(Bucket='retailscrapes')
    
    
    _BUCKET_NAME = 'retailscrapes'
    _PREFIX = 'expedia_data/'


    file_list = ListFiles(s3,_BUCKET_NAME,_PREFIX)
    
    files=[]
    for f in file_list:
        files.append(f)
    
    files = [f for f in files if '.txt' in f]
    
    df = pd.DataFrame(columns = ['date', 'airline','route','time','price','extraction_date'])
    
    for i in files:
        
      
        obj = s3.get_object(Bucket = _BUCKET_NAME, Key = i)
        body = obj['Body'].read()
        
        s=str(body,'utf-8')
        
        data = StringIO(s) 
        
        temp = pd.read_csv(data, sep='\t')
        
        df = df.append(temp, ignore_index = True)
    
    
    df = df.loc[df['price'].notnull()]
    
    df.price = df.price.map(lambda x : float(x.split('$')[1]))
    
    
    
    # transform variables into dat/time
    df['dep_time'] = df.time.map(lambda x : make_dep_time(x))
    df['arr_time'] = df.time.map(lambda x : make_arr_time(x))
    df['flt_date'] =df.date.map(lambda x : datetime.strptime(x,'%m-%d-%Y'))
    df['scrape_date'] =pd.to_datetime(df['extraction_date'])
    
    df['day_of_week'] = df.flt_date.map(lambda x: x.weekday())
    df['days_from_scrape'] = df.flt_date - df.scrape_date
    df['days_from_scrape']= df.days_from_scrape.map(lambda x: x.days)
    
   