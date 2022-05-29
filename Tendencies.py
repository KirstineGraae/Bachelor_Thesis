import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import json

# Load Data
con_data = pd.read_csv('./Data/matched_con_data.csv', sep=',', low_memory=False)
order_data = pd.read_csv('./Data/matched_order_data.csv', sep=',', low_memory=False)
con_data = con_data.sort_values('Date').reset_index(drop=True)
f = open('./Data/A_keys.json')
A_keys = json.load(f)

# Get all department names
department_names = list(Counter(con_data['Department']).keys())

def weekly_orders_department_total(order_data,keys):
    weekly_orders = {}

    weekly_units = []
    for i in range(1,53,1):
        order_data['weekly_units_w{}'.format(i)] = order_data['Number_of_Packages_w{}'.format(i)]*order_data['Quantity']
        weekly_units.append('weekly_units_w{}'.format(i))

    for key in keys:
        df = order_data.loc[lambda order_data: order_data['Key'] == key]
        df = df.reset_index()
        df = df[weekly_units]
        df = df.fillna(0)
        sums = list(df.sum())
        weekly_orders[key] = sums
    return weekly_orders

weekly_orders = weekly_orders_department_total(order_data,A_keys)

def con_time(df,key):
    df = df.loc[lambda df: df['Key'] == key]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby(['Key', df['Date'].dt.strftime('%W')])[
        'Number_ordinations'].sum()
    df = df.to_frame()
    df = df.reset_index(level=[0,1])
    for i in range(0,53,1):
        if i <=9:
            i = '0{}'.format(i)
            if i not in list(df['Date']):
                df = df.append({'Key':key,'Date': i,'Number_ordinations':0},ignore_index=True)
        else:
            if str(i) not in list(df['Date']):
                df = df.append({'Key':key,'Date': str(i),'Number_ordinations':0},ignore_index=True)
    df = df.sort_values(by=['Date'])
    return df

def plot_tendencies(con_data,weekly_orders,key,j):
    orders = weekly_orders[key]
    df = con_time(con_data,key)
    if len(df) == 53:
        orders.append(0)
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    pc = sns.lineplot(data=df,x='Date',y='Number_ordinations', marker='o',color='#C291A4', sort=False, label='Consumptions')
    #ax2 = ax1.twinx()
    #ax2.grid(None)
    po = sns.lineplot(data=df, x='Date', y=orders, marker='o',color = '#889BAE', sort=False, label='Orders')
    pc.set_xlabel('Week Number', fontsize=10)
    pc.set_ylabel('Number of Units Consumed', fontsize=10)
    po.set_ylabel('Number of Units Ordered', fontsize=10)
    pc.set_title('Consumption and orders for identifier {}'.format(key))
    sns.move_legend(po, "upper left", bbox_to_anchor=(.89, .95))
    sns.move_legend(pc, "upper left", bbox_to_anchor=(.84, .998))

    plt.savefig('./Figures/Department_orders_consumptions{}.png'.format(j))

for j, key in enumerate(A_keys):
    plot_tendencies(con_data,weekly_orders,key,j)

print(a)


l = {}
for key in A_keys:
    d = order_data.loc[lambda order_data: order_data['Key'] == key]
    d1 = con_data.loc[lambda con_data: con_data['Key'] == key]
    l[key] = [d['Units'].sum(),len(d1)]