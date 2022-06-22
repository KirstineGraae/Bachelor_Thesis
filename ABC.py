import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
import json
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import pickle
from scipy.stats import t
# Load matched data
con_data = pd.read_csv('./Data/matched_con_data.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/matched_order_data.csv',sep=',',low_memory= False)

"""
Inspiration taken from:
https://www.kaggle.com/code/danavg/abc-analysis-of-active-inventory/notebook
"""

def ABCClassify(perc):
    """
    Creates the 3 classes A, B, and C based
    on quantity % (A-80%, B-15%, C-5%)
    """
    if perc > 0 and perc < 0.9:
        return 'A'
    elif perc >= 0.9 and perc < 0.99:
        return 'B'
    elif perc >= 0.99:
        return 'C'

# Make dict with number of consumptions for each key
dict_con = Counter(con_data['Key'])

# Annual demand (quantity) from the consumption for each item
# Dictionary where keys are item (ATC code etc.) and values are annual demand (# of ordinations)
qty = dict(dict_con)

# Find cost per unit (unit cost) from the orders for each item
# Dictionary where keys are item (ATC code) and values are cost per unit (yearly dkk divided by qty)
data = order_data[['Key', 'Cost', 'Units']]
# Drop L01XD04
#data = data[data.Key != "['L01XD04', '30', 'MGM', 'OR']"]
# Find sum of cost and units
data = data.groupby('Key').sum()
# Calculate cost per unit
data['CostPerUnit'] = data['Cost'] / data['Units']

# Collect in a dictionary
unitcost = pd.Series(data.CostPerUnit.values, index=data.index).to_dict()




# Make dataframe with items (keys from both dicts), qty and unit cost
df = pd.DataFrame([qty, unitcost]).T
df.columns = ['d{}'.format(i) for i, col in enumerate(df, 1)]
df.columns = ['Qty', 'UnitCost']
# Make a column with index (ATC codes etc)
#df = df.reset_index(level=0)

# Drop row with inf value
# Drop row with NaN value
df.replace(np.inf, np.nan, inplace=True)
df = df.dropna()


# Multiply the two columns qty and unit cost to have the annual consumption value
df['AnnualConsumptionValue'] = df['Qty'] * df['UnitCost']
# Sort (ascending)
df = df.sort_values('AnnualConsumptionValue', ascending=False)
# Running annual consumption value
df['CumAnnualConsumptionValue'] = df['AnnualConsumptionValue'].cumsum()
# Sum the annual consumption values
df['SumAnnualConsumptionValue'] = df['AnnualConsumptionValue'].sum()
# Find cumulative %
df['CumPct'] = df['CumAnnualConsumptionValue'] / df['SumAnnualConsumptionValue']
# Create the column of the class
df['Class'] = df['CumPct'].apply(ABCClassify)

# Total items for each class
print(df.Class.value_counts())

# Total cost per class
print('Cost of Class A :', df[df.Class == 'A']['AnnualConsumptionValue'].sum())
print('Cost of Class B :', df[df.Class == 'B']['AnnualConsumptionValue'].sum())
print('Cost of Class C :', df[df.Class == 'C']['AnnualConsumptionValue'].sum())

# Percent of total cost per class
print('Percent of Cost of Class A :', df[df.Class == 'A']['AnnualConsumptionValue'].sum()/df['AnnualConsumptionValue'].sum())
print('Percent of Cost of Class B :', df[df.Class == 'B']['AnnualConsumptionValue'].sum()/df['AnnualConsumptionValue'].sum())
print('Percent of Cost of Class C :', df[df.Class == 'C']['AnnualConsumptionValue'].sum()/df['AnnualConsumptionValue'].sum())

# Basic description
print(df.describe())

def count_orders(df,df1):
    med = list(df.index)
    count = []
    for m in med:
        d = df1[df1['Key'] == m]
        q = 0
        for week in range(1, 53, 1):
            c = d['Number_of_Packages_w{}'.format(week)].sum()
            if c != 0:
                q += 1
        count.append(q)
    df['Count'] = count
    return df

def sizes(df):
    df['Size'] = 1.5
    return df


df = count_orders(df,order_data)
df = sizes(df)
# Scatterplot
ax1 = sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
fig, ax1 = plt.subplots(figsize=(12, 6))
s = sns.scatterplot(data=df, x="Qty", y="AnnualConsumptionValue", hue="Class", size="UnitCost", palette="husl", legend=True)
h, l = s.get_legend_handles_labels()
plt.legend(h[0:4], l[0:4],loc='upper right')
ax1.set_title("Quantity vs Annual Consumption Value",fontsize=20)
ax1.set_xlabel('Quantity',fontsize=15)
ax1.set_ylabel('Annual Consumption Value',fontsize=15)
plt.savefig('./Figures/ABCScatter.png')
plt.close('all')
#3D

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
fig = px.scatter_3d(df,x='Qty',y='AnnualConsumptionValue',z='Count',color='Class',size='Size',opacity=0.7)
fig.show()
#plt.savefig('./Figures/ABCScatter3D.png')
print(a)
plt.close('all')

# Graph
performance = df['CumPct'].tolist()
performance.insert(0, 0)
y_pos = np.arange(len(performance))
graph = sns.lineplot(y_pos, performance)
plt.ylabel('Running Total Percentage')
plt.title('ABC Analysis - Cumulative Cost per item')
plt.grid(True)
plt.ylim(0, 1)
graph.axhline(0.90)
graph.axhline(0.99)
plt.show()

# Make a list of A keys
df1 = df[df['Class'] == 'A']
key_list = list(df1.index)
with open('./Data/A_keys.json', 'w') as f:
    json.dump(key_list, f)

# Make a copy of the dataframe
dfd = df1.copy()

# Drop the Sum column
dfd = dfd.drop('CumAnnualConsumptionValue', 1)
dfd = dfd.drop('SumAnnualConsumptionValue', 1)
dfd = dfd.drop('CumPct', 1)
dfd = dfd.drop('Class', 1)
dfd = dfd.drop('UnitCost', 1)

# Basic description
print(dfd.describe())

Z = linkage(dfd, 'ward')

# Plot title
plt.title('Hierarchical Clustering Dendrogram')

# Plot axis labels
plt.xlabel('A Class')
plt.ylabel('Distance (Ward)')

# Make the dendrogram
dendrogram(Z, labels=dfd.index, leaf_rotation=90)

# Rotate x-labels a bit
plt.xticks(rotation=35, ha='right', size=9)

# Show the graph
plt.show()
