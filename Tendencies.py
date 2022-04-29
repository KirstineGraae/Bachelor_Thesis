import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#Load Data
con_data = pd.read_csv('./Data/con_data.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/order_data.csv',sep=',',low_memory=False)
con_data = con_data.sort_values('Date').reset_index(drop=True)

#Get all department names
department_names = list(Counter(con_data['Department']).keys())

def weekly_orders_department_total(order_data,deps):
    weekly_orders = {}

    packs = []
    for i in range(1,53,1):
        packs.append('Number_of_Packages_w{}'.format(i))

    for dep in deps:
        df = order_data.loc[lambda order_data: order_data['Department'] == dep]
        df = df.reset_index()
        df = df[packs]
        df = df.fillna(0)
        sums = list(df.sum())
        print('{} lenght of sums {}'.format(dep,len(sums)))
        weekly_orders[dep] = sums
    return weekly_orders

weekly_orders = weekly_orders_department_total(order_data,department_names)


def plot_dates(df,name,j,weekly_orders):
    orders = weekly_orders[name]
    df = df.loc[lambda df: df['Department'] == name]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby(['Department', df['Date'].dt.strftime('%W')])[
        'Number_ordinations'].sum()
    df = df.to_frame()
    df = df.reset_index(level=[0,1])
    names= df['Department'].str.split(',',expand=True)
    df['Department'] = names[0]
    if len(df) == 53:
        orders.insert(-1,0)
    #Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.grid(color='grey', linestyle='--', linewidth=0.3,zorder=0)
    ax.plot(df['Date'], df['Number_ordinations'], alpha=0.6, color='#ff1493', label='Weekly consumption',zorder=2)
    ax.plot(df['Date'],orders,color = '#226EC2',label = 'Weekly orders',zorder = 2)
    ax.set_xlabel('Week number')
    ax.set_ylabel('Number of consumptions')
    plt.title('Medicine consumption for {}'.format(name))
    plt.xticks(df['Date'],rotation=60,fontsize=10)
    ax.legend()
    plt.savefig('./Figures/Department_orders_consumptions{}.png'.format(j),dpi=600)

for j,dep in enumerate(department_names):
    plot_dates(con_data,dep,j,weekly_orders)

