import pandas as pd
con_data = pd.read_csv('./Data/con_data.csv', sep=',', low_memory=False)
order_data = pd.read_csv('./Data/order_data.csv', sep=',', low_memory=False)

departments = list(sorted(set(order_data['Department'])))

def department_consumptions(df,df1,departments):
    all_ATC = set(df['ATC5'])
    cons = []
    orders = []
    spend = []
    unique_ATC = []
    for dep in departments:
        a = df.loc[lambda df: df['Department'] == dep]
        b = df1.loc[lambda df1: df1['Department'] == dep]
        cons.append(len(a))
        orders.append(b['Units'].sum())
        spend.append(b['Cost'].sum())
        u = set(a['ATC5'])
        unique_ATC.append(len(u.intersection(all_ATC)))

    return cons, orders, spend, unique_ATC
cons, orders, spend, unique_ATC = department_consumptions(con_data,order_data,departments)
departments.append('Total')
cons.append(sum(cons))
orders.append(sum(orders))
spend.append(sum(spend))
unique_ATC.append(len(set(order_data['ATC5'])))

df = pd.DataFrame(list(zip(departments,unique_ATC,cons,orders,spend)),columns=['Department','Unique ATCs','Units Consumed','Units Orderes','Total Cost'])
