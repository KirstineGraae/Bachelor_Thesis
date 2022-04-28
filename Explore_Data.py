import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

#Your datapath
data_path = './Data'

con_data = pd.read_csv(data_path + '/con_data.csv',sep = ',',low_memory=False)
order_data = pd.read_csv(data_path + '/order_data.csv',sep = ',',low_memory=False)

def dictionary_con(df):
    names = df['Department'].str.split(',', expand=True)
    df['Department'] = names[0]

    dictionary = Counter(df['Department'])
    dictionary = dict(sorted(dictionary.items()))

    return dictionary

con_dict = dictionary_con(con_data)

def dictionary_order(df):
    names = df['Department'].str.split(',', expand=True)
    df['Department'] = names[0]
    dictionary = {}
    departments = list(set(df['Department']))
    for dep in departments:
        df1 = df.loc[lambda df: df['Department'] == dep]
        dictionary[dep] = df1['Number_of_Packages'].sum()
    dictionary = dict(sorted(dictionary.items()))
    return dictionary

order_dict = dictionary_order(order_data)

def plot_departments(dictionary,con = True):
    if con == True:
        fig, ax = plt.subplots(figsize=(10, 5))
        plt.grid(color='grey', linestyle='--', linewidth=0.5,zorder= 0)
        plt.bar(dictionary.keys(), dictionary.values(), color='#C291A4',zorder = 2)
        plt.title('Number of consumptions per department in 2021')
        ax.set_xlabel('Departments')
        ax.set_ylabel('Number of consumptions')
        plt.savefig('./Figures/Consumptions.png',dpi=600)

    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        plt.grid(color='grey', linestyle='--', linewidth=0.5,zorder=0)
        plt.bar(dictionary.keys(), dictionary.values(), color='#00b3b3',zorder=2)
        plt.title('Number of orders per department in 2021')
        ax.set_xlabel('Departments')
        ax.set_ylabel('Number of orders')
        plt.savefig('./Figures/Orders.png',dpi=600)

plot_departments(con_dict,con=True)
plot_departments(order_dict,con=False)

