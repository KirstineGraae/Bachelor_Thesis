import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy import stats
import seaborn as sns

f = open('./Data/Patients_Weekly.json')
pw = json.load(f)
f = open('./Data/c1.json')
con_dict_updated = json.load(f)

def new_df(d):
    df = pd.DataFrame.from_dict(d,orient='columns')
    holiday_calender = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    df['Holidays'] = holiday_calender
    return df

def new_df1(d,p):
    df = pd.DataFrame.from_dict(d,orient='columns')
    df['Patients'] = p.values()
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
    g.fig.suptitle('Correlation Between Consumed Medicine and Patients')
    plt.savefig('./Figures/Correlation_Holidays.png')
    plt.close('all')

def corr_matrix_Patients(df):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(17, 12))
    corr = df.corr()
    sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values,ax=ax1,cmap='Blues_r',annot=True)
    plt.yticks(rotation=-30)
    plt.xticks(rotation=30)
    ax1.set_title('Correlation Matrix for Consumed Medicine and Holidays',fontsize=25)
    plt.savefig('./Figures/Correlation_Matrix_P.png')

def corr_table_holidays(df,k):
    a = stats.pointbiserialr(df['Holidays'], df[k])
    df1 = df[df['Holidays'] == 1]
    df2 = df[df['Holidays'] == 0]
    l = stats.levene(df1[k],df2[k])
    return [round(l[1],2),round(a[0],2),round(a[1],2)]

def corr_table_patients(df,k):
    a = stats.pointbiserialr(df['Patients'], df[k])
    l = stats.levene(df['Patients'],df[k])
    return [round(l[1],2),round(a[0],2),round(a[1],2)]

df1 = new_df(con_dict_updated)
df2 = new_df1(con_dict_updated,pw)
holidays_corr = {}
pat_corr = {}
for key in con_dict_updated.keys():
    holidays_corr[key] = corr_table_holidays(df1,key)
    pat_corr[key] = corr_table_patients(df2,key)
df1 = pd.DataFrame.from_dict(holidays_corr,columns=['P-value Variance','Correlation Coefficient','P-value Correlation'],orient='index')
df2 = pd.DataFrame.from_dict(pat_corr,columns=['P-value Variance','Correlation Coefficient','P-value Correlation'],orient='index')
t1 = df1.to_latex(index=True)
t1 = t1.replace('[','$[')
t1 = t1.replace(']',']$')

corr_matrix_Patients(df2)