#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings('ignore')


# In[2]:


postgres_user = 'dsbc_student'
postgres_pw = '7*.8G9QH21'
postgres_host = '142.93.121.174'
postgres_port = '5432'
postgres_db = 'useducation'


# In[3]:


engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
    postgres_user, postgres_pw, postgres_host, postgres_port, postgres_db))

usedu = pd.read_sql_query('select * from useducation',con=engine)

engine.dispose()


# In[21]:


usedu.info()
usedu.tail(30)


# 1. From a first glance just using the .info() function, below is what we have for datatypes and missing data.  Looking at the head and tail of the data, I don't see anything odd (any values that may be filling in for missing data). It looks like the majority of the missing data is at the bottom/recent years. I'm curious as to why this might be, as one would think that the missing data would be in older rows. Perhaps it hadn't been updated by the time the data set was uploaded to Kaggle.
# 
#                                 
# Value Type & Percent Missing <br>
# PRIMARY_KEY                     String, 0% <br>
# STATE                           String, 0% <br>
# YEAR                            Integer, 0% <br>
# ENROLL                          Float, 17.7%   <br>
# TOTAL_REVENUE                   Float, 14.3%<br>
# FEDERAL_REVENUE                 Float, 14.3%<br>
# STATE_REVENUE                   Float, 14.3%<br>
# LOCAL_REVENUE                   Float, 14.3%<br>
# TOTAL_EXPENDITURE               Float, 14.3%<br>
# INSTRUCTION_EXPENDITURE         Float, 14.3%<br>
# SUPPORT_SERVICES_EXPENDITURE    Float, 14.3%<br>
# OTHER_EXPENDITURE               Integer, 17.7%<br>
# CAPITAL_OUTLAY_EXPENDITURE      Float, 14.3%<br>
# GRADES_PK_G                     Float, 11.6%<br>
# GRADES_KG_G                     Float, 8.9%<br>
# GRADES_4_G                      Float, 8.8%<br>
# GRADES_8_G                      Float, 8.8%<br>
# GRADES_12_G                     Float, 8.8%<br>
# GRADES_1_8_G                    Float, 8.8%<br>
# GRADES_9_12_G                   Float, 8.8%<br>
# GRADES_ALL_G                    Float, 11.6%<br>
# AVG_MATH_4_SCORE                Float, 64.1%<br>
# AVG_MATH_8_SCORE                Float, 64.4%<br>
# AVG_READING_4_SCORE             Float, 64.3%<br>
# AVG_READING_8_SCORE             Float, 66.7$<br>

# In[19]:



usedu.isnull()

print(usedu.ENROLL.unique())


# In[ ]:




