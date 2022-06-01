import pandas as pd
import json

con_data = pd.read_csv('./Data/matched_con_data.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/matched_order_data.csv',sep=',',low_memory = False)
f = open('./Data/A_keys.json')
A_keys = json.load(f)

def order_dict(df,key):
    df1 = df[df['Key'] == key]
    weekly_orders = []
    for week in range(1,53,1):
        weekly_orders.append(df1['Number_of_Packages_w{}'.format(week)].sum())
    return weekly_orders

def con_dict(df,key):
    df = df.loc[lambda df: df['Key'] == key]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby(['Key', df['Date'].dt.strftime('%W')])[
        'Number_ordinations'].sum()
    df = df.to_frame()
    df = df.reset_index(level=[0,1])
    for i in range(0,53,1):
        if i <=9:
            i = '0{}'.format(i)
            if i not in list(df['Date']):
                df = df.append({'Key':key,'Date': i,'Number_ordinations':0},ignore_index=True)
        else:
            if str(i) not in list(df['Date']):
                df = df.append({'Key':key,'Date': str(i),'Number_ordinations':0},ignore_index=True)
    df = df.sort_values(by=['Date'])
    weekly_consumptions = list(df['Number_ordinations'])
    return weekly_consumptions

dict_order = {}
dict_con = {}

for key in A_keys:
    dict_order[key] = order_dict(order_data,key)
    dict_con[key] = con_dict(con_data,key)
    if len(dict_order[key]) < len(dict_con[key]):
        for i in range(len(dict_con[key])-len(dict_order[key])):
            dict_order[key].append(0)
    elif len(dict_order[key]) > len(dict_con[key]):
        for i in range(len(dict_order[key])-len(dict_con[key])):
            dict_con[key].append(0)

a_file1 = open('./Data/weekly_consumptions_Akeys.json','w')
json.dump(dict_con, a_file1)
a_file1.close()

a_file2 = open('./Data/weekly_orders_Akeys.json','w')
json.dump(dict_order, a_file2)
a_file2.close()
