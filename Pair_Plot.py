import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

con_data = pd.read_csv('./Data/matched_con_data.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/matched_order_data.csv',sep=',',low_memory= False)

def get_A_df(order_data):

    A_keys = ["['L01XD04', '30', 'MGM', 'OR']", "['N05AD08', '2,5', 'MGM', 'IV']", "['N02BE01', '50', 'MG', 'PR']", "['V04CX', '2,5', 'PC', 'IVSC']", "['H02AB02', '4', 'MGM', 'COIMIRIV']", "['N01AX10', '10', 'MGM', 'IV']", "['C07AG01', '5', 'MGM', 'IV']",
              "['N03AE01', '1', 'MGM', 'IV']", "['C07AB09', '10', 'MGM', 'IV']", "['B05BB01', '9', 'MGM', 'IV']", "['N02AA01', '10', 'MGM', 'IMIVSC']", "['A10BJ06', '1', 'MG', 'SC']", "['N02BE01', '10', 'MGM', 'IV']", "['N01BB01', '2,5', 'MGM', 'EDIRPE']", "['N01BB52', '10', 'MGM', 'IMSC']",
              "['A06AD11', '667', 'MGM', 'OR']", "['A04AA01', '2', 'MGM', 'IV']"]

    df = order_data[order_data['Key'].isin(A_keys)]

    return df,A_keys

df,A = get_A_df(order_data)

def new_df(df,A):
    x = list(np.arange(1,53,1))*len(A)
    y = []
    z = []
    keys = []
    for key in A:
        df1 = df[df['Key'] == key]
        df1.fillna(0)
        for i in range(1,53):
            y.append((df['Number_of_Packages_w{}'.format(i)]*df['Quantity']).sum())
            z.append(df1['Cost_w{}'.format(i)].sum())
            keys.append(key)

    df = pd.DataFrame(list(zip(keys,x,y,z)),
                      columns=['Keys', 'Week', 'Units Ordered', 'Cost'])
    return df

df = new_df(df,A)

def pairplot(df):
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    sns.pairplot(df,hue='Keys',diag_kind = 'hist')
    plt.savefig('./Figures/PairPlot.png')

pairplot(df)

print(a)