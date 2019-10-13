#!/usr/bin/env python
# coding: utf-8

# In[155]:


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
import scipy.stats as stats


# In[126]:


wine = pd.read_csv('wine.csv')
wine = pd.DataFrame(wine)
print(wine.columns)
print('\n', wine.describe())


# In[127]:


wine.head()


# Experiment: We're going to look into the correlation between points and price - does the number of points a wine is *awarded* correlate with the listing price? While it may seem obvious that the more expensive wines will have more points, the cost and quality of wine has recently come into question. With vendors like [Walmart selling world class wines for under $10](https://www.foxnews.com/food-drink/walmarts-6-red-wine-named-one-of-the-best-in-the-world), can we really be sure price ensures quality?
# 
# The data we're looking at was scraped from WineEnthusiast in 2017. With almost 130,000 red and white wines (pink, champagne, or sparkling?), there are points and prices listed for nearly all of them. While a wine can be alloted points from 50 to 100, the wines in this data start at 80, and the average price for the wines is just over $36.
# 
# Each five-point section has a category, so we'll create a new column with the category for each wine and use that information to run our analysis. We'll run t-tests between the different categories and their prices and use a degree of significance as a p-value of 0.05 or below. Our metric of success will be the price of wine.
# 
# My hypothesis is that yes, there is a correlation between how many points a wine has and how much it sells for. If my hypothesis is incorrect and we fail to reject the null hypothesis, we will look into how region affects the price. 

# In[128]:



# Here we'll add a column Scale which will indicate the points category each wine is in. 

wine['scale'] = ''
print(wine.columns)
wine.loc[(80 <= wine['points']) & (wine['points'] <= 84), 'scale'] = 'Good'
wine.loc[(85 <= wine['points']) & (wine['points'] <= 89), 'scale'] = 'Very Good'
wine.loc[(90 <= wine['points']) & (wine['points'] <= 94), 'scale'] = 'Outstanding'
wine.loc[(95 <= wine['points']) & (wine['points'] <= 100), 'scale'] = 'Classic'

print(wine.head())


# In[129]:


plt.figure(figsize=(10, 4))
sns.boxplot(x='scale',y='price', data=wine, fliersize=0, order=["Good", "Very Good", "Outstanding", "Classic"]) 
plt.title('Price by Point Category')
plt.show()

# why am I not seeing outliers? How can I zoom into say $0-$1,000?


# Out of 130k rows, there are 14 wines with prices over \\$1,000 with the most expensive at \\$3,300. This is making the data quite difficult to visualize - I will remove the wine listed at \\$3,300 as it is clearly an outlier and may remove the others depending on how they affect the data. 

# In[130]:


# why did wine.drop(index=80290) not work?

wine = wine[wine.price != 3300]
print(wine.sort_values(by=['price'], ascending=False).head())


# There are 12,430 wines in the Good category and 598 of them do not have a price listed. This is just under 5%, so I'm comfortable removing lines without this information. 
# 
# There are 68,495 wines in the Very Good category and 4,744 of them do not have a price listed. This is just under 7%, so I'm not sure how comfortable I am removing lines without this information. 
# 
# There are 46,629 wines in the Outstanding category and 3,449 of them do not have a price listed. This is just over 7%, so I'm comfortable removing lines without this information. 
# 
# There are 2,416 wines in the Classic category and 205 of them do not have a price listed. This is over 8%, so I'm not sure how comfortable I am removing lines without this information. 
# 
# I think I'll remove the lines. If the missing prices would not have changed the analysis, then I don't gain anything by imputing. If the prices would have skewed the data further to one side, then I will lose accuracy by forcing central tendency values on the missing values.

# In[145]:


wine.dropna(subset=['price'])


good = wine.loc[wine['scale'] == 'Good']
vgood = wine.loc[wine['scale'] == 'Very Good']
outstanding = wine.loc[wine['scale'] == 'Outstanding']
classic = wine.loc[wine['scale'] == 'Classic']

# ax_good = plt.hist(good['price'], 50)
# ax_good.set_yscale('log')
good['price'].value_counts(dropna=False)
print('Median Good Price: ', good['price'].median())
print('Average Good Price: ', round(good['price'].mean()))
good.describe()

vgood['price'].value_counts(dropna=False)
print('Median Very Good Price: ', vgood['price'].median())
print('Average Very Good Price: ', round(vgood['price'].mean()))
vgood.describe()

outstanding['price'].value_counts(dropna=False)
print('Median Outstanding Price: ',outstanding['price'].median())
print('Average Outstanding Price: ', round(outstanding['price'].mean()))
outstanding.describe()

classic['price'].value_counts(dropna=False)
classic.describe()
print('Median Classic Price: ', classic['price'].median())
print('Average Classic Price: ', round(classic['price'].mean()))


# The average price for every class is greater than the median, indicating that the data is skewed (to the left?) in having more expensive outliers.

# In[175]:


good_prices = good[['price']]
good_prices = good_prices.iloc[:, 0]
vgood_prices = vgood[['price']]
vgood_prices = vgood_prices.iloc[:, 0]
outstanding_prices = outstanding[['price']]
classic_prices = classic[['price']]

print(type(good_prices))


# In[176]:


t_val = stats.ttest_ind(good_prices, vgood_prices, equal_var=True)
print(t_val)


# In[ ]:




