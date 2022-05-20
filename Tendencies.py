import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Load Data
con_data = pd.read_csv('./Data/con_data.csv', sep=',', low_memory=False)
order_data = pd.read_csv('./Data/order_data_wQuantity.csv', sep=',', low_memory=False)
con_data = con_data.sort_values('Date').reset_index(drop=True)
order_data['Units'] = order_data['Number_of_Packages']*order_data['Quantity']
patients = pd.read_csv('./Data/patients_weekly.csv',sep=',')

# Get all department names
department_names = list(Counter(con_data['Department']).keys())

def weekly_orders_department_total(order_data,deps):
    weekly_orders = {}

    weekly_units = []
    for i in range(1,53,1):
        order_data
        order_data['weekly_units_w{}'.format(i)] = order_data['Number_of_Packages_w{}'.format(i)]*order_data['Quantity']
        weekly_units.append('weekly_units_w{}'.format(i))

    for dep in deps:
        df = order_data.loc[lambda order_data: order_data['Department'] == dep]
        df = df.reset_index()
        df = df[weekly_units]
        df = df.fillna(0)
        sums = list(df.sum())
        weekly_orders[dep] = sums
    return weekly_orders

weekly_orders = weekly_orders_department_total(order_data,department_names)

def con_time(df,name):
    df = df.loc[lambda df: df['Department'] == name]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby(['Department', df['Date'].dt.strftime('%W')])[
        'Number_ordinations'].sum()
    df = df.to_frame()
    df = df.reset_index(level=[0,1])
    return df

def plot_tendencies(con_data,weekly_orders,patients,name,j):
    orders = weekly_orders[name]
    df = con_time(con_data,name)
    names = df['Department'].str.split(',', expand=True)
    df['Department'] = names[0]
    p = patients[patients['Department'] == name]
    p = p.values.tolist()
    p = [item for sublist in p for item in sublist]
    p = p[1:]
    if len(df) == 53:
        orders.append(0)
    if len(df) == 53 and len(p)!=53:
        p.append(0)
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    pc = sns.lineplot(data=df,x='Date',y='Number_ordinations', marker='o',color='#C291A4', sort=False, ax=ax1, label='Consumptions')
    ax2 = ax1.twinx()
    ax2.grid(None)
    po = sns.lineplot(data=df, x='Date', y=orders, marker='o',color = '#889BAE', sort=False, ax=ax2, label='Orders')
    pp = sns.barplot(data=df, x='Date', y=p, alpha=0.5, ax=ax1)
    pc.set_xlabel('Week Number', fontsize=10)
    pc.set_ylabel('Number of Units Consumed and Patients', fontsize=10)
    po.set_ylabel('Number of Units Ordered', fontsize=10)
    pc.set_title('Consumption, Orders, and Patients for {}'.format(name))
    sns.move_legend(po, "upper left", bbox_to_anchor=(.89, .95))
    sns.move_legend(pc, "upper left", bbox_to_anchor=(.84, .998))

    plt.savefig('./Figures/Department_orders_consumptions{}.png'.format(j))

for j, dep in enumerate(department_names):
    plot_tendencies(con_data,weekly_orders,patients,dep,j)

