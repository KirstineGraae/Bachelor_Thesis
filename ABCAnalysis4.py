import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

"""
Inspiration taken from:
https://www.kaggle.com/code/danavg/abc-analysis-of-active-inventory/notebook
"""

def ABCClassify(perc):
    """
    Creates the 3 classes A, B, and C based
    on quantity % (A-80%, B-15%, C-5%)
    """
    if perc > 0 and perc < 0.8:
        return 'A'
    elif perc >= 0.8 and perc < 0.95:
        return 'B'
    elif perc >= 0.95:
        return 'C'

# Find annual demand (quantity) from the consumption for each item
# Dictionary where keys are item (ATC code) and values are annual demand (# of ordinations)
df1 = pd.read_csv('./Data/con_data_ATC_match.csv', sep=',', low_memory= False)
keys1 = list(df1['ATC5'])
qty = dict()
for i in keys1:
    qty[i] = qty.get(i, 0) + 1

# Find cost per unit (unit cost) from the orders for each item
# Dictionary where keys are item (ATC code) and values are cost per unit (yearly dkk divided by qty)
columns = ['ATC5', 'Strength','Cost', 'Number_of_Packages', 'Quantity']
df2 = pd.read_csv('./Data/order_data_portions_added.csv', sep=',', low_memory=False, usecols=columns)
df2['CostPerUnit'] = (df2['Cost'] / (df2['Number_of_Packages']* df2['Quantity']))

def func(df):
    dictionary = {}
    a = Counter(df['ATC5'])
    a = list(a.keys())

    for i,atc in enumerate(a):
        df3 = df[df['ATC5'].isin([atc])]
        b = list(Counter(df3['Strength']).keys())
        for j,strength in enumerate(b):
            df4 = df3[df3['Strength'].isin([strength])]
            dictionary[atc,strength] = df4['CostPerUnit'].mean()
    return dictionary
    #df['Strength'] = [x.replace(r'\W', '') for x in df['Strength']]

dictionary = func(df2)

def func1(df):
    dictionary = {}
    a = Counter(df['ATC5'])
    a = list(a.keys())

    for i,atc in enumerate(a):
        df3 = df[df['ATC5'].isin([atc])]
        dictionary[atc] = df3['CostPerUnit'].mean()
    return dictionary
unitcost = func1(df2)


#unitcost = pd.Series(df2.CostPerUnit.values, index=df2.ATC5).to_dict()




# Make dataframe with items (keys from both dicts), qty and unit cost
df = pd.DataFrame([qty, unitcost]).T
df.columns = ['d{}'.format(i) for i, col in enumerate(df, 1)]
df.columns = ['Qty', 'UnitCost']
# Make a column with index (ATC codes)
df = df.reset_index(level=0)

# Drop row with inf value (J07BX03)
# Drop row with NaN value (H01CB02)
df.replace(np.inf, np.nan, inplace=True)
df = df.dropna()

# Multiply the two columns qty and unit cost to have the annual consumption value
df['AnnualConsumptionValue'] = df['Qty'] * df['UnitCost']
# Sort (ascending)
df = df.sort_values('AnnualConsumptionValue', ascending=False)
# Running annual consumption value
df["CumAnnualConsumptionValue"] = df["AnnualConsumptionValue"].cumsum()
# Sum the the annual consumption values
df["SumAnnualConsumptionValue"] = df["AnnualConsumptionValue"].sum()
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


performance = df['AnnualConsumptionValue'].tolist()
y_pos = np.arange(len(performance))

plt.plot(y_pos, performance)
plt.ylabel('Cost')
plt.title('ABC Analysis - Cost per item')
plt.grid(True)
plt.ylim((0, 100000))
plt.show()


performance = df['CumPct'].tolist()
y_pos = np.arange(len(performance))

plt.plot(y_pos, performance)
plt.ylabel('Running Total Percentage')
plt.title('ABC Analysis - Cumulative Cost per item')
plt.grid(True)
plt.show()


print(a)