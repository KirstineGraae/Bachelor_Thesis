import json
import statistics as st
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn_qqplot import pplot
import numpy as np
import collections
import statsmodels.stats.api as sms
#Load Data
f = open('./Data/weekly_consumptions_Akeys.json')
con_dict = json.load(f)

f = open('./Data/weekly_orders_Akeys.json')
order_dict = json.load(f)

def des_stat(d):
    keys = sorted(d.keys())
    mini = []
    maxi = []
    avg = []
    std = []
    coeff = []
    zero_count = []
    total = []
    conf_int = []
    for key in keys:

        mini.append(min(d[key]))
        maxi.append(max(d[key]))
        avg.append(round(st.mean(d[key]),2))
        total.append(sum(d[key]))
        std.append(round(st.pstdev(d[key]),2))
        coeff.append(round(st.pstdev(d[key])/st.mean(d[key]),2))
        zero_count.append(d[key].count(0))
        ci = (sms.DescrStatsW(d[key]).tconfint_mean())
        ci = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, ci))
        conf_int.append(ci)
    keys = [w.replace('[', '$[') for w in keys]
    keys = [w.replace(']', ']$') for w in keys]
    df = pd.DataFrame(list(zip(keys,mini,maxi,avg,total,std,conf_int,coeff,zero_count)), columns=['Identifier','Minimum','Maximum',
                                                                                      'Average','Total','Standard Deviation','Confidence Interval','Coefficient of Variation','Weeks with 0 Units'])
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
    df = pd.DataFrame(list(zip(id,week,vals)), columns=['Identifier', 'Week','Number of Consumed Units'])
    return df

df = to_df(con_dict_updated)

def QQ(df):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    p = pplot(df,x='Week', y='Number of Consumed Units', hue='Identifier', kind='qq', height=8, aspect=2,
               display_kws={"identity": False, "fit": True, "reg": True, "ci": 0.025})
    p.fig.suptitle('Quantile-Quantile plot for the identifiers',fontsize=25)
    p.axes[0,0].set_xlabel('Week Number',fontsize=15)
    p.axes[0, 0].set_ylabel('Number of Consumed Units', fontsize=15)
    plt.savefig('./Figures/QQ.png')
    plt.close('all')

QQ(df)

def new_df(d):
    df = pd.DataFrame.from_dict(d,orient='columns')
    holiday_calender = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    df['Holidays'] = holiday_calender
    return df

def corrfunc(x, y, **kws):
    r, _ = stats.pearsonr(x, y)
    ax = plt.gca()
    ax.annotate("r = {:.2f}".format(r),
                xy=(.1, .9), xycoords=ax.transAxes)
def cor_plot(df):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    g = sns.PairGrid(df, palette=["red"])
    g.map_upper(plt.scatter, s=10)
    g.map_diag(sns.distplot, kde=False)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_lower(corrfunc)
    g.fig.suptitle('Correlation Between Consumed Medicine and Holidays')
    plt.savefig('./Figures/Correlation_Holidays.png')
    plt.close('all')

def corr_matrix(df):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(17, 12))
    corr = df.corr()
    sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values,ax=ax1,cmap='Blues_r',annot=True)
    ax1.set_title('Correlation Matrix for Condumed Medicine and Holidays',fontsize=25)
    plt.yticks(rotation=-30)
    plt.xticks(rotation=30)
    plt.savefig('./Figures/Correlation_Matrix.png')


df1 = new_df(con_dict_updated)
cor_plot(df1)
corr_matrix(df1)

print(a)





