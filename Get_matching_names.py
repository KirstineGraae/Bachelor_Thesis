import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")
import numpy as np

from collections import Counter
con_data = pd.read_csv('./Data/con_data_ATC_match.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/order_data_portions_added.csv', sep=',', low_memory= False)
apo = pd.read_csv('./Data/Apovision_data.csv',sep=';',low_memory=False)

df = con_data[['ATC5','Type_of_Medicine','Way','Strength','Strength_measure']]
df1 = order_data[['ATC5','Type_of_Medicine','Strength']]

def type_clean(df):
    df['Type_of_Medicine'] = df['Type_of_Medicine'].map(lambda x: str(x).encode('ascii','ignore').decode('ascii'))
    df['Type_of_Medicine'] = df['Type_of_Medicine'].map(lambda x: str(x).replace(' ',''))
    return df['Type_of_Medicine']

df['Type_of_Medicine'] = type_clean(df)
df1['Type_of_Medicine'] = type_clean(df1)

def Strength_divide(df1):
    df1['Strength_measure'] = df1['Strength'].map(lambda x: ''.join([i for i in str(x) if not i.isdigit()]))
    df1['Strength_measure'] = df1['Strength_measure'].map(lambda x: re.sub('[,._]',' ',str(x)))
    df1['Strength_measure'] = df1['Strength_measure'].map(lambda x: x.replace(' ', ''))
    df1['Strength_measure'] = df1['Strength_measure'].map(lambda x: x if x != '' else 0)

    df1['Strength'] = df1['Strength'].fillna('0')
    df1['Strength'] = df1['Strength'].map(lambda x: x.replace('.', ''))
    df1['Strength'] = df1['Strength'].map(lambda x: x.replace(',', '.'))
    df1['Strength'] = df1['Strength'].map(lambda x: re.sub('[^0123456789+x.]',' ',str(x)))
    df1['Strength'] = df1['Strength'].map(lambda x: x.replace(' ', ''))
    df1['Strength'] = df1['Strength'].map(lambda x: x if x != '' else 0)

    return df1['Strength_measure'],df1['Strength']

df1['Strength_measure'],df1['Strength'] = Strength_divide(df1)

apo['Strength_measure'],apo['Strength'] = Strength_divide(apo)


def strength_measure_match(df,apo):
    count = 0
    df['Strength_measure'] = df['Strength_measure'].fillna('0')
    measure_apo = list(set(apo['Styrkekode_beskrivelse']))
    for strength in measure_apo:
        if strength in list(df['Strength_measure']):
            strength_abb = apo.loc[apo['Styrkekode_beskrivelse'] == strength, 'Styrkekode'].iloc[0]
            df['Strength_measure'] = df['Strength_measure'].map(lambda x: x if str(x) != strength else strength_abb)
            count+=1

    return df['Strength_measure'],count

df1['Strength_measure'],count = strength_measure_match(df1,apo)
df['Strength_measure'],count1 = strength_measure_match(df,apo)





print(a)