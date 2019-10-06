#!/usr/bin/env python
# coding: utf-8

# We are looking at a dataset of article open-access prices paid by the WELLCOME Trust between 2012 and 2013. We will determine the five most common journals and the total articles for each. Next, we'll calculate the mean, median, and standard deviation of the open-access cost per article for each journal.

# In[376]:


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
import seaborn as sns

wellcome = pd.read_csv('wellcome.csv')
wellcome = pd.DataFrame(wellcome)
print(wellcome.columns)
print('\n', wellcome.describe())


# I will first make all the publishers lowercase and strip space on the outsides of the names.

# In[377]:


wellcome['Publisher'] = wellcome['Publisher'].str.lower() # make everything lowercase
publishers = wellcome['Publisher']

wellcome['Publisher'] = wellcome['Publisher'].apply(lambda x: x.strip())

print(wellcome['Publisher'].unique())


# We'll find the most popular/correct name for each publisher using groupby.sum()

# # Need to check for null values **

# In[378]:


print(wellcome['Publisher'].value_counts())
print(len(wellcome['Publisher'].value_counts()))


# This function will search (and update if necessary) each publisher name for specific substrings.
# 
# Needs to be logical statement: if acs in publsher or chemical in publisher

# In[380]:


def name_repeats(df):
    for i, row in df.iterrows():
        publisher = df.iloc[i]['Publisher']
        if 'acs' in publisher or 'chemical' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american chemical society'
#         elif 'chemical' in publisher:
#             df.iloc[i, df.columns.get_loc('Publisher')] = 'american chemical society'
        elif 'physiological' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american physiological society'
        elif 'asm' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for microbiology'
        elif 'asbmb' in publisher or 'ambsb' in publisher or 'biochemistry' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'american society for biochemistry and molecular biology' 
        elif 'bmj' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'bmj'
        elif 'benthan' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'bentham science publishers'
        elif 'biomed' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'biomed central'
        elif 'cadmus' in publisher or 'camdus' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cadmus journal services'
        elif 'cup' in publisher or 'cambridge' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cambridge university press'
        elif 'cenveo' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cenveo publisher services'
        elif 'cold spring' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'cold spring harbor laboratory press publications'
        elif 'company of biologist' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'company of biologists'
        elif 'crystallography' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'international union of crystallography'
        elif 'dartmouth' in publisher or 'darmouth' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'dartmouth journal services'
        elif 'elsevier' in publisher or 'elseveier' in publisher:
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
        elif 'nature' in publisher or 'npg' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'nature publishing group'
        elif 'oup' in publisher or 'oxford' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'oxford university press'
        elif 'portland' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'portland press ltd'            
        elif 'sage' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'sage'
        elif 'springer' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'springer'
        elif 'neuro' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'society for neuroscience'
        elif 'faseb' in publisher or 'federation' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'the federation of american societies for experimental biology'
        elif 'pnas' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'pnas'
        elif 'plos' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'public library of science'
        elif 'visualized' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'the journal of visualized experiments'
        elif 'taylor' in publisher or 't&f' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'taylor & francis'
        elif 'royal' in publisher or 'rsc' in publisher:
             df.iloc[i, df.columns.get_loc('Publisher')] = 'the royal society of chemistry'     
        elif 'wiley' in publisher or 'wliey' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'john wiley & sons'
        elif 'wolters' in publisher:
            df.iloc[i, df.columns.get_loc('Publisher')] = 'wolters kluwer'
    return df

new_names = name_repeats(wellcome)
print(new_names['Publisher'].value_counts())
# print(len(new_names['Publisher'].value_counts()))


# This code replaces Publisher incorrect/unwanted names with the desired/more commonly used publisher name. The difference between this code and the function above is that this code will only replace the exact name we look for, whereas the code above will search for a substring and will replace any name that contains said substring.

# In[381]:


new_names['Publisher'] = (new_names['Publisher']
    .replace(['asm (american society for microbiology)','american society of microbiology' ],'american society for microbiology')
    .replace(['society for genermal microbiology', 'society of general microbiology'],'society for general microbiology')
    .replace(['the endocrine socety', 'the endrocrine society'], 'the endocrine society')
    .replace(['american society of hamatology', 'american society of haematology'], 'american society of hematology')
    .replace(['impact journals llc'], 'impact journals'))
# print(new_names['Publisher'].value_counts())
# print(len(new_names['Publisher'].value_counts()))


# In[382]:


#print(new_names['Publisher'].value_counts())


# Below are the five most common journals with the total number of articles. <br>
# Elsevier - 409 <br>
# Public Library of Science - 307 <br>
# John Wiley & Sons - 270 <br>
# Oxford University Press - 217 <br>
# Springer Science & Business Media - 95 <br>

# Calculate the mean, median, and standard deviation of the open-access cost per article for each journal. <br>
# I'll update the column name to 'Cost' so it's easier to deal with. All of the values have either a pound or dollar sign, so my first task is to strip the pound signs using a lambda funciton. As most of the values are in pounds, I'll convert all values in USD to pounds and strip the dollar sign before starting my analysis.

# In[383]:


new_names.columns = ['PMID/PMCID', 'Publisher', 'Journal title', 'Article title', 'Cost']
null_data = new_names[new_names['Cost'].isnull()] # checking to make sure there are no null values
print(null_data)
print(new_names.dtypes)


# In[384]:



# new_names['Cost'].str.replace('£', '').astype(float)
# new_names['Cost'] = new_names['Cost'].apply(lambda x: float(x.replace('£', '')) if '£' in x else x)
# new_names['Cost'] = new_names['Cost'].apply(lambda x: float(x.replace('$', ''))*0.6361 if '$' in x else x)
 
     
    
# new_names['Cost'] = pd.to_numeric(new_names['Cost'])
# print(new_names.dtypes)
   
# new_names['Cost'] = pd.to_numeric(new_names['Cost'])
# print(new_names.dtypes)

new_names['Cost'] = new_names['Cost'].apply(lambda x: x.replace('£', '') if isinstance(x, str) and '£' in x else x)
new_names['Cost'] = new_names['Cost'].apply(lambda x: float(x.replace('$', ''))*0.6361 if isinstance(x, str) and '$' in x else x)
   
new_names['Cost'] = pd.to_numeric(new_names['Cost'])
print(new_names.dtypes)


# In[385]:


# Dataframes showing mean, median, and standard deviations for each 
# 'john wiley & sons', 'public library of science', 'oxford university press', 'springer'
new_names.set_index('Publisher')
print(new_names[:5])
#top_5 = new_names.loc[['elsevier', 'springer', 'john wiley & sons', 'public library of science', 'oxford university press']]
new_names.set_index('Publisher')
mean_df = new_names.groupby('Publisher')['Cost'].mean()
mean_top_5 = mean_df.loc[['elsevier', 'springer', 'john wiley & sons', 'public library of science', 'oxford university press']]
print(mean_top_5)
print(new_names.sort_values('Cost'))


# In[325]:


median_df = new_names.groupby('Publisher')['Cost'].median()
median_top_5 = median_df.loc[['elsevier', 'springer', 'john wiley & sons', 'public library of science', 'oxford university press']]
print(median_top_5)


# In[429]:


mean_df = new_names.groupby('Publisher')['Cost'].mean()
mean_top_5 = mean_df.loc[['elsevier', 'springer', 'john wiley & sons', 'public library of science', 'oxford university press']]
print(mean_top_5)


# In[326]:


std_df = new_names.groupby('Publisher')['Cost'].std()
std_top_5 = std_df.loc[['elsevier', 'springer', 'john wiley & sons', 'public library of science', 'oxford university press']]
print(std_top_5)


# # Before Removing Outliers
# 
# | Publisher                  | Mean of Cost  || Median of Cost  | Standard Deviation of Cost |
# | -------------------------- | ------------- || --------------- | -------------------------- |
# | Elsevier                   | £26,825.33    || £2,352.53      | £154,255.65  |
# | Springer Science & Business| £2,026.04     || £1,981.19      | £270.95      |
# | John Wiley & Sons          | £17,532.90    || £2,009.95      | £121,308.95  |
# | Public Library of Science  | £50,551.90    || £1,039.87      | £215,817.57  |
# | Oxford University Press    | £19,775.35    || £2,040.00      | £134,545.69  |
# 
# 
# As we can see, the standard deviations for four of the five publishers are quite large and the medians are much larger than the mediansof the respective journals, indicating we have some outliers. When I create a box plot, I can see that there is at least one value of 999,999.00 pounds. I'm going to replace these values with the median values.

# In[392]:


# ax = sns.boxplot(x='top_5',y='Cost',data=new_names)  
# plt.title('Costs')
# sns.despine(offset=10, trim=True)
# ax.set(xlabel='', ylabel='Cost in Pounds')

new_names[['Publisher', 'Cost']].plot.box()
plt.title('Costs in Pounds')

plt.show()


# In[404]:


# new_names.set_index('Publisher', inplace=True)
print(new_names[:5])
elsevier = new_names.loc[['elsevier']]
springer = new_names.loc[['springer']]
jw = new_names.loc[['john wiley & sons']]
plos = new_names.loc[['public library of science']]
oup = new_names.loc[['oxford university press']]
# print(elsevier)


# In[411]:


# elsevier['Cost'] = elsevier['Cost'].apply(lambda x: x=2352.530 if x==999999 else 
print(elsevier.describe())
print(springer.describe())
print(jw.describe())
print(plos.describe())
print(oup.describe())


# In[428]:


elsevier_median = elsevier.loc[elsevier['Cost']<999999, 'Cost'].median()
print(elsevier_median)
elsevier.loc[elsevier.Cost > 800000, 'Cost'] = np.nan
print(elsevier[:10])
elsevier.fillna(elsevier_median,inplace=True)
elsevier.plot.box()


# In[432]:


# JW has outliers above 150,000, so that's where our cutoff will be.
jw_median = jw.loc[jw['Cost']<150000, 'Cost'].median()
print(jw_median)
jw.loc[jw.Cost > 150000, 'Cost'] = np.nan
print(jw[:10])
jw.fillna(jw_median,inplace=True)
jw.plot.box()


# In[436]:


# PLOS has outliers above 150,000, so that's where our cutoff will be.
plos_median = plos.loc[plos['Cost']<150000, 'Cost'].median()
print(plos_median)
plos.loc[plos.Cost > 150000, 'Cost'] = np.nan
print(plos[:10])
plos.fillna(plos_median,inplace=True)
plos.plot.box()


# In[463]:


# OUP has outliers above 150,000, so that's where our cutoff will be.
oup_median = oup.loc[oup['Cost']<9999999, 'Cost'].median()
print(oup_median)
oup.loc[oup.Cost > 999999999, 'Cost'] = np.nan
oup.fillna(oup_median,inplace=True)
print('Elsevier Mean: ', elsevier.mean(), '\n Elsevier Median: ', elsevier.median(), '\n Elsevier STD: ', elsevier.std())
print('Springer Mean: ', springer.mean(), '\n Springer Median: ', springer.median(), '\n Springer STD: ', springer.std())
print('John Wiley Mean: ', jw.mean(), '\n John Wiley Median: ', jw.median(), '\n John Wiley STD: ', jw.std())
print('PLOS Mean: ', plos.mean(), '\n PLOS Median: ', plos.median(), '\n PLOS STD: ', plos.std())
print('OUP Mean: ', oup.mean(), '\n OUP Median: ', oup.median(), '\n OUP STD: ', oup.std())


# In[ ]:





# # After Removing Outliers
# 
# | Publisher                  | Mean of Cost  || Median of Cost  | Standard Deviation of Cost |
# | -------------------------- | ------------- || --------------- | -------------------------- |
# | Elsevier                   | £2,432.78     || £2,343.56       | £783.77  |
# | Springer Science & Business| £2,026.04     || £1,981.19       | £270.95  |
# | John Wiley & Sons          | £2,010.74     || £2,007.74       | £369.20  |
# | Public Library of Science  | £1,117.38     || £1,014.38       | £392.88  |
# | Oxford University Press    | £1,847.94     || £2,040.00       | £508.13  |
# 
# 
# After we replace the extreme outliers with the median values of each publisher, the means and medians are much closer together and the standard deviations make more sense. It's hard to imagine journals being sold for £999,999!

# In[ ]:




