import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy import stats
import seaborn as sns

df = pd.read_csv('./Data/matched_con_data.csv',sep=',')
f = open('./Data/Patients_Weekly.json')
pw = json.load(f)

def con_dict(df,dep):
    df = df.loc[lambda df: df['Department'] == dep]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby(['Department', df['Date'].dt.strftime('%W')])[
        'Number_ordinations'].sum()
    df = df.to_frame()
    df = df.reset_index(level=[0,1])
    for i in range(0,53,1):
        if i <=9:
            i = '0{}'.format(i)
            if i not in list(df['Date']):
                df = df.append({'Department':dep,'Date': i,'Number_ordinations':0},ignore_index=True)
        else:
            if str(i) not in list(df['Date']):
                df = df.append({'Department':dep,'Date': str(i),'Number_ordinations':0},ignore_index=True)
    df = df.sort_values(by=['Date'])
    dep_weekly_consumptions = list(df['Number_ordinations'])
    return dep_weekly_consumptions

dict_con = {}

for dep in list(set(df['Department'])):
    dict_con[dep] = con_dict(df,dep)

def new_df(d,p):
    df = pd.DataFrame.from_dict(d,orient='columns')
    df['Patients'] = p.values()
    return df

def corr_table_holidays(df,k):
    a = stats.pointbiserialr(df['Patients'], df[k])
    return [round(a[0],2),round(a[1],2)]

df1 = new_df(dict_con,pw)
patients_corr = {}
for key in sorted(dict_con.keys()):
    abb = key.split(',')[0]
    patients_corr[abb] = corr_table_holidays(df1,key)
df1 = pd.DataFrame.from_dict(patients_corr,columns=['Correlation Coefficient','P-value'],orient='index')
t1 = df1.to_latex(index=True)
