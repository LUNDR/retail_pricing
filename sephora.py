# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:52:22 2020

@author: lundr
"""

import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ast
import pandas as pd
from datetime import datetime
from datetime import date
import boto3

## establish how many products there are on the main products page

main_url = "https://www.sephora.fr/shop-shop/"
no_res = requests.get(main_url)      
no_soup = bs4.BeautifulSoup(no_res.content, features="lxml")

headline = no_soup.find_all('div',{'id':'main-js'})
    
for div in headline:
    n = div.h2.text
    n2 = n.split("P",1)[0]
    n3 = n2.replace(" ","")
    n4 = int(n3)
    print(str(n4)+" Products")




url = ["https://www.sephora.fr/shop-shop/?srule=rank&sz=28&start=0&t2scookie=rank1&"]

for i in range(28,n4,28):
    new_url = "https://www.sephora.fr/shop-shop/?srule=rank&sz=28&start="+str(i)+"&t2scookie=rank1&"
    url.append(new_url)
    

print("there are "+str(len(url))+" urls")
print(url[0])

product = []
n=0

for u in url:
    print("url number" + str(n))
    res = requests.get(u)      
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    
    # =============================================================================
    # for i in soup.find_all(name="div", attrs={"class":"product-pricing"}):
    #     print(i.text)
    # =============================================================================
    
    
    products = soup.find_all(name = 'div', attrs={"class":"product-tile clickable"})
       
    exceptions = []    
    for div in products:
        try:
            p=ast.literal_eval(div['data-tcproduct'])
            product.append(p)
        except:
           exceptions.append(div['data-tcproduct']) 
    n+=1   
        
print(len(product))
print(len(exceptions))

df = pd.DataFrame(product)
df.drop_duplicates(subset="product_pid",keep="first",inplace=True)

now = datetime.now()
df['extraction_date'] = now

write_path='sephora.fr_'+str(date.today())+'.txt'
df.to_csv(write_path, sep='\t', index=False)
    
    

from config import ACCESS_KEY,SECRET_KEY

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
# =============================================================================
# for div in soup.findChildren('div',{'class':'product-pricing'}):
#     print(div.text)
# =============================================================================


# =============================================================================
# for span in products.a.h3.find_all('span', recursive=False):
#     print(span.attrs['title'])
# =============================================================================
