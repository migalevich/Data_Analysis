#!/usr/bin/env python
# coding: utf-8

# In[440]:


import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns


# In[441]:


data = pd.read_excel('d:/Pythoning/test_task/test.xlsx', index_col=None, dtype = 
                     {
                        'Retention' : int, 'MaxLevelPassed' : int, 'User_id' : int, 'SumRevenue' : int, 'CountBuy' : int,
                     'Get_Ads' : int})


# In[442]:


data.head()


# In[443]:


df = data[['Retention', 'User_id', 'AB_Cohort','SumRevenue', 'CountBuy', 'Get_Ads']] # новый dataframe


# In[444]:


df


# In[445]:


# кол-во пользователей по тестовым группам сделавших покупки


# In[446]:


users_count  = df.groupby('AB_Cohort', as_index=False)                    .agg({'User_id':'count'})                      .rename(columns={'User_id':'users_count'})


# In[447]:


users_count


# In[448]:


users_did_b = df.query('SumRevenue > 0')     .groupby('AB_Cohort', as_index=False)    .agg({'SumRevenue':'count'})    .rename(columns={'SumRevenue':'users_did_bought'})


# In[449]:


users_count["users_did_bought"]  = users_did_b["users_did_bought"] 


# In[450]:


users_count


# In[451]:


# Процент людей в группе сделавших покупку
users_count["Rate1"] = round(users_count.users_did_bought/users_count.users_count * 100, 2)


# In[452]:


users_count


# In[453]:


# КОГОРТНЫЙ АНАЛИЗ


# In[454]:


retention_A_group = df.query('AB_Cohort == "A"')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count'})                      .rename(columns={'User_id':'users_count', 'Retention':'retention_day'})


# In[455]:


retention_A_group


# In[456]:


retention_B_group = df.query('AB_Cohort == "B"')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count'})                      .rename(columns={'User_id':'users_count', 'Retention':'retention_day'})


# In[457]:


# Retention (Удержание)


# In[458]:


# День установки
users_install_B = retention_B_group[retention_B_group.retention_day == 0].users_count
users_install_A = retention_A_group[retention_A_group.retention_day == 0].users_count


# In[459]:


users_install_B


# In[460]:


retention_B_group['users_install'] = 0
for i in retention_B_group['retention_day'].tolist():
    retention_B_group['users_install'][i] = users_install_B;


# In[461]:


retention_A_group['users_install'] = 0
for i in retention_A_group['retention_day'].tolist():
    retention_A_group['users_install'][i] = users_install_A;


# In[462]:


retention_A_group


# In[463]:


retention_B_group["Retention"] = round(retention_B_group.users_count/retention_B_group.users_install * 100, 2 )
retention_A_group["Retention"] = round(retention_A_group.users_count/retention_A_group.users_install * 100, 2 )


# In[464]:


import matplotlib.pyplot as plt
plt.plot(retention_A_group.query("retention_day != 0").retention_day, retention_A_group.query("retention_day != 0").Retention, label='A Cohort')
plt.plot(retention_B_group.query("retention_day != 0").retention_day, retention_B_group.query("retention_day != 0").Retention, label='B Cohort')
plt.legend()
plt.title('Day N Retention = Number of users that launched the game on Day N / Number of users who installed the game * 100%')
plt.xlabel('Days from install')
plt.ylabel('Retention')


# In[465]:


# ВЫВОД: Удержание стало снижаться в группе B после 3-го дня игры.


# In[466]:


# ARPPU = Revenue / Paying Users


# In[467]:


revenue_A_group = df.query('AB_Cohort == "A" & SumRevenue > 0')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count', 'SumRevenue':'sum'})                      .rename(columns={'User_id':'Users_paying', 'Retention':'Retention_day'})


# In[468]:


revenue_B_group = df.query('AB_Cohort == "B" & SumRevenue > 0')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count', 'SumRevenue':'sum'})                      .rename(columns={'User_id':'Users_paying', 'Retention':'Retention_day'})


# In[469]:


revenue_B_group


# In[470]:


retention_A_group["SumRevenue"] = revenue_A_group.SumRevenue.cumsum()
retention_B_group["SumRevenue"] = revenue_B_group.SumRevenue.cumsum()
retention_A_group["Users_paying"] = revenue_A_group.Users_paying
retention_B_group["Users_paying"] = revenue_B_group.Users_paying


# In[477]:


retention_A_group


# In[472]:


retention_B_group


# In[478]:


retention_A_group["ARPPU"] = round(retention_A_group.SumRevenue/retention_A_group.Users_paying, 2)
retention_B_group["ARPPU"] = round(retention_B_group.SumRevenue/retention_B_group.Users_paying, 2)


# In[479]:


retention_A_group


# In[480]:


retention_B_group


# In[481]:


import matplotlib.pyplot as plt
plt.plot(retention_A_group.retention_day, retention_A_group.ARPPU, label = 'A Chohort')
plt.plot(retention_B_group.retention_day, retention_B_group.ARPPU, label = 'B Chohort')
plt.legend()
plt.title('ARPPU = Revenue / Paying Users')
plt.xlabel('Days from install')
plt.ylabel('ARPPU')


# In[482]:


# ВЫВОД: Средняя доходность от одного платящего юзера в группе В выше


# In[483]:


# DAU - the number of unique users per day (Daily Active Users)


# In[484]:


users_A_did_buying  = df.query('AB_Cohort == "A" & SumRevenue > 0 ')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count'})                      .rename(columns={'User_id':'users_count_did_buying'})


# In[485]:


retention_A_group["users_count_did_buying"] = users_A_did_buying.users_count_did_buying


# In[486]:


retention_A_group["DAU"] = round(retention_A_group.users_count_did_buying/retention_A_group.users_count*100,2)


# In[487]:


retention_A_group


# In[488]:


users_B_did_buying  = df.query('AB_Cohort == "B" & SumRevenue > 0 ')                    .groupby('Retention', as_index=False)                    .agg({'User_id':'count'})                      .rename(columns={'User_id':'users_count_did_buying'})


# In[489]:


retention_B_group["users_count_did_buying"] = users_B_did_buying.users_count_did_buying


# In[490]:


retention_B_group["DAU"] = round(retention_B_group.users_count_did_buying/retention_B_group.users_count*100,2)


# In[491]:


retention_B_group


# In[492]:


import matplotlib.pyplot as plt
plt.plot(retention_A_group.Retention, retention_A_group.DAU)
plt.plot(retention_B_group.Retention, retention_B_group.DAU)


# In[493]:


# Средний чек


# In[494]:


count_buyings_A = df.query('AB_Cohort == "A"')                    .groupby('Retention', as_index=False)                    .agg({'CountBuy':'sum'})


# In[495]:


retention_A_group


# In[504]:


retention_A_group["count_buyings"] = count_buyings_A.CountBuy.cumsum()


# In[505]:


retention_A_group["Avg_Bill"] = round(retention_A_group.SumRevenue/retention_A_group.count_buyings,2)


# In[506]:


retention_A_group


# In[507]:


count_buyings_B = df.query('AB_Cohort == "B"')                    .groupby('Retention', as_index=False)                    .agg({'CountBuy':'sum'})


# In[508]:


retention_B_group["count_buyings"] = count_buyings_B.CountBuy.cumsum()


# In[509]:


retention_B_group["Avg_Bill"] = round(retention_B_group.SumRevenue/retention_B_group.count_buyings,2)


# In[510]:


retention_B_group


# In[514]:


import matplotlib.pyplot as plt
plt.plot(retention_A_group.retention_day, retention_A_group.Avg_Bill, label = 'A Chohort')
plt.plot(retention_B_group.retention_day, retention_B_group.Avg_Bill, label = 'B Chohort')
plt.legend()
plt.title('Avg Bill = Sum Revenue / count_buyings ')
plt.xlabel('Days from install')
plt.ylabel('Avg Bill')


# In[ ]:


# Среднее пройденное кол-во уровней ????


# In[ ]:


# Процент пользователей просмотревших рекламу


# In[515]:


users_getAds_B = df.query('AB_Cohort == "B" & Get_Ads > 0')                    .groupby('Retention', as_index=False)                    .agg({'Get_Ads':'count'})                      .rename(columns={'Get_Ads':'users_getAds'})


# In[516]:


retention_B_group["users_getAds"] = round(users_getAds_B.users_getAds/retention_B_group.users_count*100,2)


# In[517]:


retention_B_group


# In[518]:


users_getAds_A = df.query('AB_Cohort == "A" & Get_Ads > 0')                    .groupby('Retention', as_index=False)                    .agg({'Get_Ads':'count'})                      .rename(columns={'Get_Ads':'users_getAds'})


# In[519]:


retention_A_group["users_getAds"] = round(users_getAds_A.users_getAds / retention_A_group.users_count * 100 ,2)


# In[521]:


import matplotlib.pyplot as plt
plt.plot(retention_A_group.retention_day, retention_A_group.users_getAds, label = 'A Chohort')
plt.plot(retention_B_group.retention_day, retention_B_group.users_getAds, label = 'B Chohort')
plt.legend()
plt.title('Percent Users who watched ads = Users who watched ads / All users ')
plt.xlabel('Days from install')
plt.ylabel('Percent Users who watched ads')


# In[ ]:


# Теперь нам необходимо проверить, какая из гипотез верна:
#* Нулевая гипотеза Н0 - конверсии равны.
#* Альтернативная гипотеза - конверсии не равны.


# In[ ]:


# стат.критерий (p-value), Хи-квадрат


# In[157]:


import statsmodels.stats.proportion as proportion


# In[158]:


get_ipython().run_line_magic('pinfo2', 'proportion.proportions_chisquare')


# In[159]:


chi2start, pval, table = proportion.proportions_chisquare(users_count['users_did_bought'],users_count['users_count'])


# In[160]:


alpha = 0.05


# In[161]:


print(pval < alpha) # Можем ли мы отклонить нулевую гипотезу


# In[ ]:


# ВЫВОД: Конверсии НЕ равны!


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




