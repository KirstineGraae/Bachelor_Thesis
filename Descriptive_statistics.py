import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import seaborn as sns
from scipy.stats import t
import matplotlib.pyplot as plt
from collections import Counter

with open("./Data/ATC_dict", "rb") as fp:
    ATC_dict = pickle.load(fp)

con_data = pd.read_csv('./Data/con_data_ATC_match.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/order_data_ATC_match.csv',sep=',',low_memory = False)

def table1(df,dict):
    keys = list(dict.keys())
    stats = {}
    df['Ordinationsoprettelsesdato'] = pd.to_datetime(df['Ordinationsoprettelsesdato'])

    #Mean of consumptions according to a weekly basis
    df_dates = df.groupby(['Udleveringsoverafdeling navn', df['Ordinationsoprettelsesdato'].dt.strftime('%W')])[
        'Antal ordinationer'].sum()
    df_dates = df_dates.to_frame()
    df_dates = df_dates.reset_index(level=[0,1])
    for i,key in enumerate(keys):
        df_dep_dates = df_dates.loc[lambda df_dates: df_dates['Udleveringsoverafdeling navn'] == key]
        m = df_dep_dates['Antal ordinationer'].mean()
        s = df_dep_dates['Antal ordinationer'].std()
        dof = len(df_dep_dates['Antal ordinationer']) - 1
        confidence = 0.95
        t_crit = np.abs(t.ppf((1 - confidence) / 2, dof))
        conf_int = (m-s*t_crit/np.sqrt(len(df_dep_dates['Antal ordinationer'])), m+s*t_crit/np.sqrt(len(df_dep_dates['Antal ordinationer'])))
        stats[key] = [np.round(m),np.round(s),np.round(conf_int)]
    return stats

stats = table1(con_data,ATC_dict)

def names_shortened(dict):
    keys = list(dict.keys())
    names = []
    for i in keys:
        name = i.split(',')
        names.append(name[0])
    return names

names = names_shortened(ATC_dict)

def boxplots(df):
    df['Ordinationsoprettelsesdato'] = pd.to_datetime(df['Ordinationsoprettelsesdato'])
    #Mean of consumptions according to a weekly basis
    df_dates = df.groupby(['Udleveringsoverafdeling navn', df['Ordinationsoprettelsesdato'].dt.strftime('%W')])[
        'Antal ordinationer'].sum()

    df_dates = df_dates.to_frame()
    df_dates = df_dates.reset_index(level=[0,1])
    names= df_dates['Udleveringsoverafdeling navn'].str.split(',',expand=True)
    df_dates['Udleveringsoverafdeling navn'] = names[0]

    sns.set_theme(style="whitegrid")
    p = sns.boxplot(x=df_dates['Udleveringsoverafdeling navn'], y=df_dates['Antal ordinationer'].to_numeric(), data=df_dates,palette = 'hls')
    p.set_title('Weekly consumptions for each department')
    p.set_xlabel('Department')
    p.set_ylabel('Weekly consumptions')
    plt.savefig('./Figures/Boxplot.png', dpi=600)
#boxplots(con_data)

def top_5_ATC(df,key):
    df = df.loc[lambda df: df['Udleveringsoverafdeling navn'] == key]
    count_ATC = Counter(df['ATC5'])
    count_ATC = dict(sorted(count_ATC.items(), key=lambda item: item[1],reverse=True))
    top_ATC = list(count_ATC.keys())[:5]
    top_values = list(count_ATC.values())[:5]
    percentage = [x / sum(count_ATC.values()) for x in top_values]
    percentage = [x*100 for x in percentage]
    percentage = [round(num, 2) for num in percentage]

    return [top_ATC,top_values,percentage]

top_ATC_con = {}

for i in list(ATC_dict.keys()):
    top_ATC_con[i] = top_5_ATC(con_data,i)

def polar_plots(df,key,top_ATC):
    top_5 = top_ATC[key][0]
    df = df.loc[lambda df: df['Udleveringsoverafdeling navn'] == key]
    df = df[df['ATC5'].isin(top_5)]
    df['Ordinationsoprettelsesdato'] = pd.to_datetime(df['Ordinationsoprettelsesdato'])
    # Mean of consumptions according to a weekly basis
    df_dates = df.groupby(['ATC5', df['Ordinationsoprettelsesdato'].dt.strftime('%W')])[
        'Antal ordinationer'].sum()
    df_dates = df_dates.to_frame()
    df_dates = df_dates.reset_index(level=[0, 1])
    name = key.split(',')

    fig = px.line_polar(df, r=df_dates['Antal ordinationer'], theta=df_dates['Ordinationsoprettelsesdato'],
                        color=df_dates['ATC5'], line_close=True,
                        title='Polar seasonal plot',
                        width=600, height=500)
    plt.title('Weekly top ATC consumption for {}'.format(name[0]))
    plt.savefig('./Figures/PP_{}.png'.format(name[0]), dpi=600)

#for i in list(ATC_dict.keys()):
    #polar_plots(con_data,i,top_ATC_con)


print(a)