# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 07:47:25 2020

@author: lundr
"""


import pandas as pd
import numpy as np
from datetime import time
from datetime import datetime
import matplotlib.pyplot as plt

 # find lowest daily price.
tab_min = df.groupby(by = ['flt_date','scrape_date']).agg({'price':'min'}).unstack()

tab_min_restricted = tab_min.loc[tab_min.index <'2020-06-01']


#find average lowest price by day of week.
tab_min = df.groupby(by = ['flt_date','day_of_week',], as_index=False).agg({'price':'min'})
tab_min_day_of_week = tab_min.groupby(by = 'day_of_week').mean()


# plots
# =============================================================================
plt.plot(tab_min_restricted.iloc[:,0])
plt.plot(tab_min_restricted.iloc[:,3])
plt.plot(tab_min_restricted.iloc[:,5])
plt.xticks(rotation=90)

#plt.plot(tab_min.loc[tab_min['day_of_week']==0]['price'])
# plt.plot(tab_min.loc[tab_min['day_of_week']==4]['price'])
# plt.plot(tab_min.loc[tab_min['day_of_week']==2]['price'])
# 
# 
# plt.legend(['Friday', 'Monday','Wednesday'], loc='upper left')
# =============================================================================
