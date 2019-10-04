#!/usr/bin/env python
# coding: utf-8

# We are looking at a dataset of article open-access prices paid by the WELLCOME Trust between 2012 and 2013. We will determine the five most common journals and the total articles for each. Next, we'll calculate the mean, median, and standard deviation of the open-access cost per article for each journal.

# In[98]:


import os
os.chdir('C:\\Users\\M246047\\Documents\\Python')
import numpy as np
import pandas as pd
import datetime as dt
import pylab
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import scipy as sc
from scipy.stats import ttest_ind
import re

wellcome = pd.read_csv('wellcome.csv')
wellcome = pd.DataFrame(wellcome)
print(wellcome.columns)
print('\n', wellcome.describe())


# I will first make all the publishers lowercase and strip space on the outsides of the names.

# In[99]:


wellcome['Publisher'] = wellcome['Publisher'].str.lower() # make everything lowercase
publishers = wellcome['Publisher']

wellcome['Publisher'] = wellcome['Publisher'].apply(lambda x: x.strip())

print(wellcome['Publisher'].unique())


# We'll find the most popular/correct name for each publisher using groupby.sum()

# # Need to check for null values **

# In[100]:


print(wellcome['Publisher'].value_counts())
print(len(wellcome['Publisher'].value_counts()))


# This function will search (and update if necessary) each publisher name for specific substrings.

# In[213]:


def name_repeats(df):
    for i, row in df.iterrows():
        publisher = df.iloc[i]['Publisher']
        if 'acs' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american chemical society'
        elif 'chemical' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american chemical society'
        elif 'physiological' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american physiological society'
        elif 'asm' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for microbiology'
        elif 'asbmb' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for biochemistry and molecular biology' 
        elif 'ambsb' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for biochemistry and molecular biology'
        elif 'biochemistry' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for biochemistry and molecular biology'
        elif 'bmj' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'bmj'
        elif 'benthan' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'bentham science publishers'
        elif 'biomed' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'biomed central'
        elif 'cadmus' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cadmus journal services'
        elif 'camdus' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cadmus journal services'
        elif 'cup' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cambridge university press'
        elif 'cambridge' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cambridge university press'
        elif 'cenveo' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cenveo publisher services'
        elif 'cold spring' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cold spring harbor laboratory press publications'
        elif 'company of biologist' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'company of biologists'
        elif 'crystallography' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'international union of crystallography'
        elif 'dartmouth' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'dartmouth journal services'
        elif 'darmouth' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'dartmouth journal services'
        elif 'elsevier' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'elsevier'
        elif 'elseveier' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'elsevier'
        elif 'frontiers' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'frontiers media'
        elif 'future medicine' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'future medicine'
        elif 'hindawi' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'hindawi'
        elif 'informa' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'informa healthcare'
        elif 'landes' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'landes bioscience'
        elif 'liebert' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'mary ann liebert inc'
        elif 'mit press' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'mit press'
        elif 'jove' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'my jove corp'
        elif 'national academy' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'national academy of sciences'
        elif 'nature' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'nature publishing group'
        elif 'npg' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'nature publishing group'
        elif 'oup' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'oxford university press'
        elif 'oxford' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'oxford university press'
        elif 'portland' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'portland press ltd'            
        elif 'sage' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'sage'
        elif 'springer' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'springer'
        elif 'neuro' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'society for neuroscience'
        elif 'faseb' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'the federation of american societies for experimental biology'
        elif 'federation' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'the federation of american societies for experimental biology'
        elif 'pnas' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'pnas'
        elif 'plos' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'public library of science'
        elif 'visualized' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'the journal of visualized experiments'
        elif 'taylor' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'taylor & francis'
        elif 't&f' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'taylor & francis'
        elif 'royal' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'the royal society of chemistry'    
        elif 'rsc' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'the royal society of chemistry' 
        elif 'wiley' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'john wiley & sons'
        elif 'wliey' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'john wiley & sons'
        elif 'wolters' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'wolters kluwer'
    return df

new_names = name_repeats(wellcome)
# print(new_names['Publisher'].value_counts())
# print(len(new_names['Publisher'].value_counts()))


# This code replaces Publisher incorrect(?) names with the desired/more commonly used publisher name. The difference between this code and the function above is that this code will only replace the exact name we look for, whereas the code above will search for a substring and will replace any name that containsthe substring.

# In[215]:


new_names['Publisher'] = (new_names['Publisher']
    .replace(['asm (american society for microbiology)','american society of microbiology' ],'american society for microbiology')
    .replace(['society for genermal microbiology', 'society of general microbiology'],'society for general microbiology')
    .replace(['the endocrine socety', 'the endrocrine society'], 'the endocrine society')
    .replace(['american society of hamatology', 'american society of haematology'], 'american society of hematology')
    .replace(['impact journals llc'], 'impact journals'))
# print(new_names['Publisher'].value_counts())
# print(len(new_names['Publisher'].value_counts()))


# In[212]:


# print(new_names['Publisher'].unique())


# Below are the five most common journals with the total number of articles. <br>
# Elsevier - 409 <br>
# Public Library of Science -307 <br>
# John Wiley & Sons -270 <br>
# Oxford University Press - 217 <br>
# Springer Science & Business Media <br>

# Calculate the mean, median, and standard deviation of the open-access cost per article for each journal. I'll update the column name to 'Cost In Pounds' so it's easier to deal with. Most of the values are in pounds, but some are in USD, so I'm going to convert everything to pounds before I start my analysis. I'll need to remove the pound symbol and convert the Cost column to float values.

# In[244]:


null_data = new_names[new_names['Cost'].isnull()]
print(null_data)


# In[240]:


print(new_names.columns)


def all_pounds(df):
    for row, i in df.iterrows():
        cost = df.iloc[i]['Cost']
        if '£' in cost:
            df.iloc[i, df.columns.get_loc('Cost In Pounds')] = cost
        elif '$' in cost:
            cost.strip('$')
            cost = float(cost) * 0.6361  # this is the conversion rate as of June 13, 2013        
            df.iloc[i, df.columns.get_loc('Cost In Pounds')] = cost
    return cost
   
converted = all_pounds(new_names)    
# converted['Cost In Pounds'] = converted['Cost'].apply(lambda x: x.strip('£'))
# new_names['Cost In Pounds'] = converted['Cost'].apply(lambda x: x.strip())
# converted['Cost'] = converted['Cost'].apply(pd.to_numeric)
# print(converted[:20])


# In[ ]:




