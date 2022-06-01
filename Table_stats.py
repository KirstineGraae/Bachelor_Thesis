import pandas as pd
con_data = pd.read_csv('./Data/matched_con_data.csv', sep=',', low_memory=False)
order_data = pd.read_csv('./Data/matched_order_data.csv', sep=',', low_memory=False)
c = pd.read_csv('./Data/con_data.csv', sep=',', low_memory=False)
o = pd.read_csv('./Data/order_data.csv', sep=',', low_memory=False)

departments = list(sorted(set(order_data['Department'])))

def department_consumptions(df,df1,c,o,departments):
    all_ATC = set(df['Key'])
    cons = []
    orders = []
    spend = []
    unique_ATC = []
    percentage_c = []
    percentage_o = []
    percentage_s = []
    for dep in departments:
        a = df.loc[lambda df: df['Department'] == dep]
        b = df1.loc[lambda df1: df1['Department'] == dep]
        c1 = c.loc[lambda c: c['Department'] == dep]
        o1 = o.loc[lambda o: o['Department'] == dep]
        cons.append(len(a))
        orders.append(b['Units'].sum())
        spend.append(b['Cost'].sum())
        u = set(a['Key'])
        unique_ATC.append(len(u.intersection(all_ATC)))
        percentage_c.append('{:.2f} %'.format((len(a)/len(c1))*100))
        percentage_o.append('{:.2f} %'.format((b['Units'].sum()/o1['Units'].sum())*100))
        percentage_s.append('{:.2f} %'.format((b['Cost'].sum()/o1['Cost'].sum())*100))

    return cons, orders, spend, unique_ATC,percentage_c,percentage_o,percentage_s
cons, orders, spend, unique_ATC,percentage_c,percentage_o,percentage_s = department_consumptions(con_data,order_data,c,o,departments)
departments.append('Total')
cons.append(sum(cons))
orders.append(sum(orders))
spend.append(sum(spend))
unique_ATC.append(len(set(order_data['Key'])))

df = pd.DataFrame(list(zip(departments,unique_ATC,cons,orders,spend,percentage_c,percentage_o,percentage_s)),columns=['Department','Unique Keys','Units Consumed','Units Ordered','Total Cost','% of all Consumptions','% of all Orders','% of Total Spend'])
a = df.to_latex(index=False)
