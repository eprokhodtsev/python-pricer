#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from interpolation import Interpolator


# In[2]:


RUB_Swaps = pd.read_csv('RUB swap points.csv')
RUB_Swaps=RUB_Swaps.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4'],axis=1)
USD_Rates = pd.read_csv('USD rates.csv')
USD_Rates.loc[0,'Conv, adj']=0.001295


# In[3]:


#RUB_Swaps['Start_date']=['11/05/21','18/05/21','25/05/21','11/06/21','11/07/21','11/08/21','11/11/21','11/02/22'
#                         ,'11/05/22','11/05/23','11/05/24','11/05/25','11/05/26']
RUB_Swaps['Start_date'] = [0,7,14,30,60,90,180,270,360,720,1080,1440,1800]
RUB_Swaps


# In[4]:


USD_Rates


# In[5]:


Inter = Interpolator()
USD_Rates_Interpolated=[]
Swap_points_interpolated = []
t = 1
for T in USD_Rates['StartDate'][1:]:
    time_delta = (pd.Timestamp(T)-datetime.datetime(2021,11,15)).days
    Swap_points_interpolated.append(Inter.interpolate(list(RUB_Swaps['Start_date']),list(RUB_Swaps['SW POINTS']),time_delta))
    #USD_Rates_Interpolated.append(USD_Rates['Unnamed: 1'][t] - Swap_points_interpolated[-1]/10**4)
    t+=1


# In[6]:


Swap_points_interpolated = pd.DataFrame({'Swap_points':Swap_points_interpolated,'Dates':USD_Rates['StartDate'][1:]})
Swap_points_interpolated.set_index('Dates',inplace=True)
Swap_points_interpolated.plot()


# In[7]:


Swap_points_interpolated


# In[8]:


Discount_factors= pd.DataFrame([1]*len(USD_Rates['StartDate'][1:]),index=USD_Rates['StartDate'][1:],columns=['Discount USD'])
Discount_factors

