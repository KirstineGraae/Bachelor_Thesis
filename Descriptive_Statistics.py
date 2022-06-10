import json
import statistics as st
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn_qqplot import pplot
import numpy as np
import collections
import random
import statsmodels.stats.api as sms
from numpy.random import normal
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot_2samples

#Load Data
f = open('./Data/weekly_consumptions_Akeys.json')
con_dict = json.load(f)

f = open('./Data/weekly_orders_Akeys.json')
order_dict = json.load(f)

f = open('./Data/Patients_Weekly.json')
pw = json.load(f)

def des_stat(d):
    keys = sorted(d.keys())
    mini = []
    maxi = []
    avg = []
    med = []
    std = []
    coeff = []
    zero_count = []
    total = []
    conf_int = []
    for key in keys:

        mini.append(min(d[key]))
        maxi.append(max(d[key]))
        avg.append(round(st.mean(d[key]),2))
        med.append(round(st.median(d[key]),2))
        total.append(sum(d[key]))
        std.append(round(st.pstdev(d[key]),2))
        coeff.append(round(st.pstdev(d[key])/st.mean(d[key]),2))
        zero_count.append(d[key].count(0))
        ci = (sms.DescrStatsW(d[key]).tconfint_mean())
        ci = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, ci))
        conf_int.append(ci)
    keys = [w.replace('[', '$[') for w in keys]
    keys = [w.replace(']', ']$') for w in keys]
    df = pd.DataFrame(list(zip(keys,mini,maxi,avg,med,total,std,conf_int,coeff,zero_count)), columns=['Identifier','Minimum','Maximum',
                                                                                      'Average','Median','Total','Standard Deviation','Confidence Interval','Coefficient of Variation','Weeks with 0 Units'])
    return df


con_stat = des_stat(con_dict)
order_stat = des_stat(order_dict)
a = con_stat.to_latex(index=False)
a = a.replace('\$','$')

def choose_identifiers(df,d):
    df = df[df['Coefficient of Variation'] <= 0.25]
    df['Identifier'] = df['Identifier'].str.replace('$','')
    con_dict_updated = {}
    for key in list(df['Identifier']):
        con_dict_updated[key] = d[key]
    return con_dict_updated

con_dict_updated = choose_identifiers(con_stat,con_dict)
with open('./Data/c1.json', 'w') as f:
    json.dump(con_dict_updated, f)

def test_normality(d):
    keys = []
    p_val = []
    for key in d.keys():
        shap = stats.shapiro(d[key])
        keys.append(key)
        p_val.append(round(shap.pvalue,2))
    keys = [w.replace('[', '$[') for w in keys]
    keys = [w.replace(']', ']$') for w in keys]
    df = pd.DataFrame(list(zip(keys,p_val)), columns=['Identifier','P-value'])
    return df

p_vals = test_normality(con_dict_updated)
a1 = p_vals.to_latex(index=False)
a1 = a1.replace('\$','$')

def to_df(d):
    d = collections.OrderedDict(sorted(d.items()))
    week = list(np.arange(1,54,1))*len(d)
    vals = [item for sublist in list(d.values()) for item in sublist]
    id = []
    for i,key in enumerate(d.keys()):
        l = [key]*len(d[key])
        id.append(l)
    id = [item for sublist in id for item in sublist]
    dist =(list(normal(loc=0, scale=1,
                    size=len(d[key]))))*len(id)
    df = pd.DataFrame(list(zip(id,week,vals,dist)), columns=['Identifier', 'Week','Number of Consumed Units','Distribution'])
    return df

def QQ(df):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    p = pplot(df,x='Distribution', y='Number of Consumed Units',hue='Identifier', kind='qq', height=8, aspect=2,
               display_kws={"identity": False, "fit": True, "reg": True, "ci": 0.05})
    p.fig.suptitle('Quantile-Quantile Plot Medicine Consumption',fontsize=20)
    p.axes[0,0].set_xlabel('Theoretical Quantile',fontsize=10)
    p.axes[0,0].set_ylabel('Number of Consumed Units', fontsize=10)
    plt.savefig('./Figures/QQ.png')
    plt.close('all')

df = to_df(con_dict_updated)
QQ(df)










