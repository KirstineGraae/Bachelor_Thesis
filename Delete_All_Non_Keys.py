import pandas as pd
import numpy as np
from collections import Counter

con_data = pd.read_csv('./Data/con_data.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/order_data.csv',sep=',',low_memory= False)
apo = pd.read_csv('./Data/Apovision_data.csv', sep=';',low_memory=False)

con_rem = con_data[con_data['Key'] =='0.0']
order_rem = order_data[order_data['Key'] =='0.0']

def con_elec(df,apo):
    a = df[df['ATC5'] == 'B05BB01']
    b = apo[apo['ATC_kode'] == 'B05BB01']
    a['Medicine_name'] = a['Medicine_name'].str.split(' ').str[0].str.lower()
    a['Medicine_name'] = a['Medicine_name']

#con_elec(con_rem,apo)

con_data = con_data[con_data['Key'] != '0.0']
order_data = order_data[order_data['Key'] != '0.0']

Unique_keys_order = set(order_data['Key'])
Unique_keys_con = set(con_data['Key'])
intersection_keys = list(Unique_keys_order.intersection(Unique_keys_con))

con_data = con_data[con_data['Key'].isin(intersection_keys)]
order_data = order_data[order_data['Key'].isin(intersection_keys)]


dict_con = Counter(con_data['Key'])
dict_order = {}
for key in list(dict_con.keys()):
    d = order_data[order_data['Key'] == key]
    dict_order[key] = d['Units'].sum()

larger_orders = []
for key in list(dict_con.keys()):
    if dict_con[key] <= dict_order[key]:
        larger_orders.append(key)

order_data.to_csv('./Data/matched_order_data.csv',index=False)
con_data.to_csv('./Data/matched_con_data.csv',index=False)


