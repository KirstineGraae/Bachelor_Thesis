import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
Inspiration taken from:
https://practicaldatascience.co.uk/data-science/how-to-create-an-abc-inventory-classification-model
"""

# Annual quantity from the orders for each item
# Annual cost from the orders for each item
columns = ['ATC5', 'Cost', 'Number_of_Packages', 'Quantity']
df = pd.read_csv('./Data/order_data_portions_added.csv', sep=',', low_memory=False, usecols=columns)
df['Qty'] = df['Number_of_Packages'] * df['Quantity']
keys = list(df['ATC5'])
qty = pd.Series(df.Qty.values, index=df.ATC5).to_dict()
cost = pd.Series(df.Cost.values, index=df.ATC5).to_dict()

# Make dataframe with items (keys from both dicts), qty and unit cost
data = pd.DataFrame([qty, cost]).T
data.columns = ['d{}'.format(i) for i, col in enumerate(data, 1)]
data.columns = ['Qty', 'Cost']
# Make a column with index (ATC codes)
data = data.reset_index(level=0)

# Drop row with inf value (J07BX03)
# Drop row with NaN value (H01CB02)
data.replace(np.inf, np.nan, inplace=True)
data = data.dropna()

# Multiply the two columns qty and cost to have the annual consumption value
data['CumSum'] = data['Cost'].cumsum()
# Sum the the annual consumption values
data['Sum'] = data['Cost'].sum()
# Find %
data['Pct'] = (data['CumSum'] / data['Sum']) * 100

# For method 1
data1 = data.copy()
# For method 2
data2 = data.copy()

# METHOD 1

def classify(perc):
    if perc > 0 and perc <= 80:
        return 'A'
    elif perc > 80 and perc <= 95:
        return 'B'
    else:
        return 'C'

data1['Class'] = data1['Pct'].apply(classify)
data1['Rank'] = data1['Pct'].rank().astype(int)

table1 = data1.groupby('Class').agg(
    Items=('index', 'count'),
    Qty=('Qty', sum),
    Cost=('Cost', sum)
)

print(table1)

# METHOD 2

# Drop the index column
data2 = data2.drop('index', 1)
# Drop the Sum column
data2 = data2.drop('Sum', 1)

# Build k-means model with 3 cluster (A, B and C)
model = KMeans(3)
# Fit model
model.fit(data2)

# Extract the cluster id from labels_ and assign it to each SKU in the dataframe.
data2.loc[:, 'Cluster'] = model.labels_
class_map = {0: "C", 1: "B", 2: "A"}
data2['Class_kmeans'] = data2['Cluster'].apply(lambda x: class_map[x])

table2 = data2.groupby('Cluster').agg(
    Items=('Cluster', 'count'),
    Qty=('Qty', sum),
    Cost=('Cost', sum)
)

print(table2)


# Visualize
identified_clusters = model.fit_predict(data)
data_with_clusters = data.copy()
data_with_clusters['Clusters'] = identified_clusters
plt.scatter(data_with_clusters['Qty'], data_with_clusters['Cost'], c=data_with_clusters['Clusters'], cmap='rainbow')
plt.show()


print(a)

