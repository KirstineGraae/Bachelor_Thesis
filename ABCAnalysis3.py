import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from abc_analysis import abc_analysis, abc_plot
from sklearn.cluster import KMeans
import seaborn as sns

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
df2['CostPerUnit'] = (df2['Number_of_Packages'] * df2['Quantity']) / df2['Cost']
unitcost = pd.Series(df2.CostPerUnit.values, index=df2.ATC5).to_dict()

# Make dataframe with items (keys from both dicts), qty and unit cost
df = pd.DataFrame([qty, unitcost]).T
df.columns = ['d{}'.format(i) for i, col in enumerate(df, 1)]
df.columns = ['Qty', 'UnitCost']

# Drop row with inf value (J07BX03)
# Drop row with NaN value (H01CB02)
df.replace(np.inf, np.nan, inplace=True)
df = df.dropna()

# Multiply the two columns qty and unit cost to have the annual consumption value
df['AnnualConsumptionValue'] = df['Qty'] * df['UnitCost']
# Sum the the annual consumption values
df["SumAnnualConsumptionValue"] = df["AnnualConsumptionValue"].sum()
# Find %
df['Pct'] = (df['AnnualConsumptionValue'] / df['SumAnnualConsumptionValue']) * 100
# Sort by pct (asc.)
df = df.sort_values('Pct', ascending=False)
# Drop the Sum column
df = df.drop('SumAnnualConsumptionValue', 1)

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
df["class_kmeans"] = df["Cluster"].apply(lambda x: class_map[x])

table2 = df.groupby('Cluster').agg(
    Items=('Cluster', 'count'),
    Qty=('Qty', sum),
    Cost=('UnitCost', sum)
)

print(table2)


print(a)
