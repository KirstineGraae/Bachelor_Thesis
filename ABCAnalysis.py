import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
#Load data
df1 = pd.read_csv('./Data/matched_con_data.csv', sep=',', low_memory= False)
df2 = pd.read_csv('./Data/matched_order_data.csv', sep=',', low_memory=False)

# Find annual demand (quantity) from the consumption for each item
# Dictionary where keys are item (ATC code) and values are annual demand (# of ordinations)
keys = list(df1['ATC5'])
qty = dict()
for i in keys:
    qty[i] = qty.get(i, 0) + 1

# Find cost per unit (unit cost) from the orders for each item
# Dictionary where keys are item (ATC code) and values are cost per unit (yearly dkk divided by qty)
#columns = ['ATC5', 'Cost', 'Units']
df2['CostPerUnit'] = (df2['Number_of_Packages'] * df2['Quantity']) / df2['Cost']
unitcost = pd.Series(df2.CostPerUnit.values, index=df2.ATC5).to_dict()

# Make dataframe with items (keys from both dicts), qty and unit cost
df = pd.DataFrame([qty, unitcost]).T
df.columns = ['d{}'.format(i) for i, col in enumerate(df, 1)]
df.columns = ['Qty', 'UnitCost']
# Make a column with index (ATC codes)
df = df.reset_index(level=0)
print(a)
# Drop row with inf value (J07BX03)
# Drop row with NaN value (H01CB02)
df.replace(np.inf, np.nan, inplace=True)
df = df.dropna()

# Multiply the two columns qty (d1) and unit cost (d2) to have the annual consumption value
df["AnnualConsumptionValue"] = df['Qty'] * df['UnitCost']
# Sum the the annual consumption values
df["SumAnnualConsumptionValue"] = df["AnnualConsumptionValue"].sum()
# Find %
df['Pct'] = (df['AnnualConsumptionValue'] / df['SumAnnualConsumptionValue']) * 100
# Drop the SumAnnualConsumptionValue column
df = df.drop('SumAnnualConsumptionValue', 1)

# Build k-means model with 3 cluster (A, B and C)
model = KMeans(3)
# Fit model
model.fit(df)

# Visualize
identified_clusters = model.fit_predict(df)
df_with_clusters = df.copy()
df_with_clusters['Clusters'] = identified_clusters
plt.scatter(df_with_clusters['Qty'], df_with_clusters['UnitCost'], c=df_with_clusters['Clusters'], cmap='rainbow')
plt.legend(model.labels_ )
plt.show()




df.loc[:, 'cluster'] = model.labels_
class_map = {0: "C", 1: "B", 2: "A"}
df["class_kmeans"] = df["cluster"].apply(lambda x: class_map[x])

df.groupby('cluster').agg(
    Items=('cluster', 'count'),
    Qty=('Qty', sum),
    Cost=('UnitCost', sum)
)


#plt.scatter(df['d1'], df['d2'])
#plt.show()
x = df.iloc[:, 1:2].reshape(-1, 1)

# Multiply the qty and unit cost
abc_dict = {x: unitcost[x]*qty[x] for x in unitcost}
abc_list = list(abc_dict.values())
abc = np.array(abc_list)
dctAnalysis = abc_analysis(abc_list, True)

abc_plot(dctAnalysis)


