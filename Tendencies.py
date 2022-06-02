import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import json

# Load Data
f = open('./Data/Patients_Weekly.json')
pw = json.load(f)
f = open('./Data/c1.json')
cons = json.load(f)
A_keys = list(cons.keys())
f = open('./Data/weekly_orders_Akeys.json')
orders = json.load(f)

def plot_tendencies(c,o,p,k,j):
    ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    fig, ax1 = plt.subplots(figsize=(12, 6))
    pc = sns.lineplot(x=p['Week'],y=c[k], marker='o',color='#C291A4', sort=False, label='Consumptions',ax=ax1)
    po = sns.lineplot(x=p['Week'], y=o[k], marker='o',color = '#889BAE', sort=False, label='Orders',ax=ax1)
    ax2 = ax1.twinx()
    ax2.grid(None)
    pp = sns.barplot(data = p,x='Week', y='Patients', alpha=0.3, ax=ax2,order=None)
    pc.set_xlabel('Week Number', fontsize=10)
    pc.set_ylabel('Number of Units Consumed and Ordered', fontsize=10)
    pp.set_ylabel('Number of Patients', fontsize=10)
    pc.set_title('Consumption and orders for identifier {}'.format(key))
    plt.savefig('./Figures/Department_orders_consumptions{}.png'.format(j))

p = pd.DataFrame(list(zip(pw.keys(),pw.values())), columns=['Week','Patients'])
for j, key in enumerate(A_keys):
    plot_tendencies(cons,orders,p,key,j)

