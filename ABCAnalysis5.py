import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
Inspiration taken from:
https://practicaldatascience.co.uk/data-science/how-to-create-an-abc-inventory-classification-model
"""

# Find annual demand (quantity) from the consumption for each item
# Dictionary where keys are item (ATC code) and values are annual demand (# of ordinations)
df1 = pd.read_csv('./Data/con_data_ATC_match.csv', sep=',', low_memory= False)
keys = list(df1['ATC5'])
qty = dict()
for i in keys:
    qty[i] = qty.get(i, 0) + 1

# Find cost per unit (unit cost) from the orders for each item
# Dictionary where keys are item (ATC code) and values are cost per unit (yearly dkk divided by qty)
columns = ['ATC5', 'Cost', 'Number_of_Packages', 'Quantity']
df2 = pd.read_csv('./Data/order_data_portions_added.csv', sep=',', low_memory=False, usecols=columns)
cost = pd.Series(df2.Cost.values, index=df2.ATC5).to_dict()

# Make dataframe with items (keys from both dicts), qty and unit cost
df = pd.DataFrame([qty, cost]).T
df.columns = ['d{}'.format(i) for i, col in enumerate(df, 1)]
df.columns = ['Qty', 'Cost']
# Make a column with index (ATC codes)
df = df.reset_index(level=0)

# Drop row with inf value (J07BX03)
# Drop row with NaN value (H01CB02)
df.replace(np.inf, np.nan, inplace=True)
df = df.dropna()

# Sort (ascending)
df = df.sort_values('Cost', ascending=False)
# Cumulative sum of cost
df['CumSum'] = df['Cost'].cumsum()
# Total sum of cost
df['Sum'] = df['Cost'].sum()
# Find %
df['Pct'] = df['CumSum'] / df['Sum']
# Drop the index column
df = df.drop('index', 1)
# Drop the Sum column
df = df.drop('Sum', 1)

# Build k-means model with 3 cluster (A, B and C)
model = KMeans(3)
# Fit model
model.fit(df)

# Visualize
identified_clusters = model.fit_predict(df)
data_with_clusters = df.copy()
data_with_clusters['Clusters'] = identified_clusters
plt.scatter(data_with_clusters['Qty'], data_with_clusters['Cost'], c=data_with_clusters['Clusters'], cmap='rainbow')
plt.show()

# Extract the cluster id from labels_ and assign it to each SKU in the dataframe.
df.loc[:, 'Cluster'] = model.labels_
class_map = {0: "C", 1: "B", 2: "A"}
df['Class_kmeans'] = df['Cluster'].apply(lambda x: class_map[x])

table2 = df.groupby('Cluster').agg(
    Items=('Cluster', 'count'),
    Qty=('Qty', sum),
    Cost=('Cost', sum)
)

print(table2)



print(a)