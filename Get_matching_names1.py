import numpy as np
import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

con_data = pd.read_csv('./Data/con_data_ATC_match.csv',sep=',',low_memory= False)
apo = pd.read_csv('./Data/Apovision_data.csv', sep=';',low_memory=False)
order_data = pd.read_csv('./Data/order_data_ATC_match.csv',sep=',',low_memory= False)

order_data['Adm_way'] = np.zeros(len(order_data))
order_data['Strength_measure'] = np.zeros(len(order_data))
order_data['Key'] = np.zeros(len(order_data))
order_data['Quantity'] = np.zeros(len(order_data))
order_data['Quantity_measure'] = np.zeros(len(order_data))
order_data['Portion_size'] = np.zeros(len(order_data))

def clean_hope(df,apo,ATC,k,length):
    a = df.loc[lambda df: df['ATC5'] == ATC]
    b = apo.loc[lambda apo: apo['ATC_kode'] == ATC]
    a['Strength'] = a['Strength'].str.lower()
    b['Strength'] = b['Strength'].str.lower()
    a['Order_name'] = a['Order_name'].str.lower()
    b['Description'] = b['Description'].str.lower()
    for i in list(a.index):
        for j in list(b.index):
            if a['Strength'][i] == b['Strength'][j] and a['Order_name'][i] == b['Description'][j]:
                a['Strength'][i] = b['Styrke'][j]
                a['Adm_way'][i] = b['Adm_vej_kode'][j]
                a['Strength_measure'][i] = b['Styrkekode'][j]
                a['Key'][i] = [ATC,a['Strength'][i],a['Strength_measure'][i],a['Adm_way'][i]]
                a['Quantity_measure'][i] = b['Pakningsstr_enhed'][j]
                if a['Quantity_measure'][i] == 'ML' or a['Quantity_measure'][i] == 'ml':
                    a['Quantity'][i] = 1
                    a['Portion_size'][i] = b['Pakningsstr'][j]
                    break
                else:
                    a['Quantity'][i] = b['Pakningsstr'][j]
                    a['Portion_size'][i] = 1
                    break
    print('Order ATC {} of {}'.format(k+1, length + 1))
    df.loc[a.index, ['Strength','Strength_measure','Adm_way','Key','Quantity','Portion_size','Quantity_measure']] = a[:]
    return df
order_ATC = list(set(order_data['ATC5']))
for k,ATC in enumerate(order_ATC):
    order_data = clean_hope(order_data,apo,ATC,k,len(order_ATC))

con_data['Adm_way'] = np.zeros(len(con_data))
con_data['Key'] = np.zeros(len(con_data))
con_data['Quantity'] = np.zeros(len(con_data))
con_data['Quantity_measure'] = np.zeros(len(con_data))
con_data['Portion_size'] = np.zeros(len(con_data))

def clean_hope1(df,apo,ATC,k,length):
    a = df.loc[lambda df: df['ATC5'] == ATC]
    b = apo.loc[lambda apo: apo['ATC_kode'] == ATC]
    a['Generic_name'] = a['Generic_name'].str.lower()
    b['Description'] = b['Description'].str.lower()
    for i in list(a.index):
        for j in list(b.index):
            if a['Generic_name'][i] == b['Description'][j]:
                a['Strength'][i] = b['Styrke'][j]
                a['Adm_way'][i] = b['Adm_vej_kode'][j]
                a['Strength_measure'][i] = b['Styrkekode'][j]
                a['Key'][i] = [ATC,a['Strength'][i],a['Strength_measure'][i],a['Adm_way'][i]]
                a['Quantity_measure'][i] = b['Pakningsstr_enhed'][j]
                if a['Quantity_measure'][i] == 'ML' or a['Quantity_measure'][i] == 'ml':
                    a['Quantity'][i] = 1
                    a['Portion_size'][i] = b['Pakningsstr'][j]
                    break
                else:
                    a['Quantity'][i] = b['Pakningsstr'][j]
                    a['Portion_size'][i] = 1
                    break
            else:
                continue
    print('Con ATC {} of {}'.format(k+1,length+1))
    df.loc[a.index, ['Strength','Strength_measure','Adm_way','Key','Quantity','Portion_size','Quantity_measure']] = a[:]
    return df
con_ATC = list(set(con_data['ATC5']))
for k,ATC in enumerate(con_ATC):
    con_data = clean_hope1(con_data,apo,ATC,k,len(con_ATC))

print(a)
a = [','.join(map(str, l)) for l in con_data['Key'] if l != np.float()]
aa = set(a)
b = [','.join(map(str, l)) for l in order_data['Key'] if l != np.float()]
bb = set(b)
aa.intersection(bb)