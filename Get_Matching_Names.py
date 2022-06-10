import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

con_data = pd.read_csv('./Data/con_data.csv',sep=',',low_memory= False)
apo = pd.read_csv('./Data/Apovision_data.csv', sep=';',low_memory=False)
order_data = pd.read_csv('./Data/order_data.csv',sep=',',low_memory= False)

order_data['ATC5'] = order_data['ATC5'].str.replace('*','')
order_data['Adm_way'] = np.zeros(len(order_data))
order_data['Strength_measure'] = np.zeros(len(order_data))
order_data['Key'] = np.zeros(len(order_data))
order_data['Units'] = order_data['Quantity']*order_data['Number_of_Packages']

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
                break
            else:
                continue
    print('Order ATC {} of {}'.format(k+1, length + 1))
    df.loc[a.index, ['Strength','Strength_measure','Adm_way','Key']] = a[:]
    return df

order_ATC = list(set(order_data['ATC5']))
for k,ATC in enumerate(order_ATC):
    order_data = clean_hope(order_data,apo,ATC,k,len(order_ATC))

con_data['Adm_way'] = np.zeros(len(con_data))
con_data['Key'] = np.zeros(len(con_data))
con_data['ATC5'] = con_data['ATC5'].str.replace('*','')

def change_percent_strength(a):
    a['Strength'] = a['Strength'].str.replace(',','')
    a[['Strength','Strength1','Strength2']] = a['Strength'].str.split('.',expand=True)
    a['Strength1'] = a['Strength1'].map(lambda x: '_' if (x is None) else x)
    a['Strength1'] = a['Strength1'].fillna('_')
    a['Strength'] = a['Strength'].fillna('_')
    a['Strength1'] = a['Strength1'].str.replace('0','')
    a['Strength1'] = a['Strength1'].map(lambda x: x if (x == '_') else ',{}'.format(x))
    a['Strength'] = a[['Strength', 'Strength1']].apply(lambda x: ''.join(x), axis=1)
    a['Strength'] = a['Strength'].str.replace('_','')
    for i in range(0,10,1):
        a['Strength'] = a['Strength'].str.replace('0{}'.format(i),'{}'.format(i))

    return a

con_data = change_percent_strength(con_data)

def clean_hope1(df,apo,ATC,k,length):
    a = df.loc[lambda df: df['ATC5'] == ATC]
    b = apo.loc[lambda apo: apo['ATC_kode'] == ATC]
    a['Strength_measure'] = a['Strength_measure'].str.lower()
    b['Styrkekode_beskrivelse'] = b['Styrkekode_beskrivelse'].str.lower()
    for i in list(a.index):
        for j in list(b.index):
            if a['Strength'][i] == b['Styrke'][j] and a['Strength_measure'][i] == b['Styrkekode_beskrivelse'][j]:
                a['Strength'][i] = b['Styrke'][j]
                a['Adm_way'][i] = b['Adm_vej_kode'][j]
                a['Strength_measure'][i] = b['Styrkekode'][j]
                a['Key'][i] = [ATC,a['Strength'][i],a['Strength_measure'][i],a['Adm_way'][i]]
                break
            else:
                continue
    print('Con ATC {} of {}'.format(k+1,length+1))
    df.loc[a.index, ['Strength','Strength_measure','Adm_way','Key']] = a[:]
    return df
con_ATC = list(set(con_data['ATC5']))
for k,ATC in enumerate(con_ATC):
    con_data = clean_hope1(con_data,apo,ATC,k,len(con_ATC))

order_data.to_csv('./Data/order_data.csv',index=False)
con_data.to_csv('./Data/con_data.csv',index=False)

