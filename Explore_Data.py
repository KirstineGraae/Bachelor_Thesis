import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Your datapath
data_path = './Data'

con_data = pd.read_csv(data_path + '/con_data.csv', sep=',', low_memory=False)
order_data = pd.read_csv(data_path + '/order_data.csv', sep=',', low_memory=False)

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
        df1['Units'] = df1['Number_of_Packages']*df1['Quantity']
        dictionary[dep] = df1['Units'].sum()
    dictionary = dict(sorted(dictionary.items()))
    return dictionary

order_dict = dictionary_order(order_data)

def to_df(dict1,dict2):
    g = []
    h = []
    g.append(list(dict1.values()))
    g.append(list(dict2.values()))
    g = [item for sublist in g for item in sublist]
    h.append(['Consumptions']*len(dict1))
    h.append(['Orders']*len(dict2))
    h = [item for sublist in h for item in sublist]
    df = pd.DataFrame(list(zip(list(dict1.keys())*2,g,h)),columns=['Department','Units','Type'])
    return df
df = to_df(con_dict,order_dict)

def plot_departments(df):
    colors = ['#C291A4','#889BAE']
    sns.set_palette(sns.color_palette(colors))
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    p = sns.barplot(data = df,x = 'Department',y='Units',hue = 'Type',ax=ax1)
    p.set_xlabel('Department', fontsize=10)
    p.set_ylabel('Number of Units Consumed and Ordered', fontsize=10)
    p.set_title('Total Number of Consumptions and Orders for all Departments',fontsize=15)
    plt.savefig('./Figures/Total_Units.png')

plot_departments(df)

