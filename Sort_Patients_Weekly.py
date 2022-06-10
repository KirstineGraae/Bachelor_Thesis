import pandas as pd
import json
from collections import Counter

patients = pd.read_csv('./Data/patiens_arrived.csv',sep = ';')
order_data = pd.read_csv('./Data/matched_order_data.csv',sep = ',')

def match_deps(order_data,patients):
    patients['Behandlingsansvarlig Afdeling navn'] = patients['Behandlingsansvarlig Afdeling navn'].str.split(',').str[
        0]
    patients['Behandlingsansvarlig Afdeling navn'] = patients['Behandlingsansvarlig Afdeling navn'].str.replace(r'[0-9]+', '')
    patients['Behandlingsansvarlig Afdeling navn'] = patients['Behandlingsansvarlig Afdeling navn'].str.replace('RH','')
    patients['Behandlingsansvarlig Afdeling navn'] = patients['Behandlingsansvarlig Afdeling navn'].str.replace('Ø','OE')
    patients['Behandlingsansvarlig Afdeling navn'] = patients['Behandlingsansvarlig Afdeling navn'].str.replace(' ','')
    dictionary = dict(zip(order_data['Department'].str.split(',').str[0],order_data['Department']))
    patients = patients[patients['Behandlingsansvarlig Afdeling navn'].isin(list(dictionary.keys()))]
    patients['Department'] = patients['Behandlingsansvarlig Afdeling navn'].map(lambda x: dictionary[x])
    return patients

patients = match_deps(order_data,patients)
wp = []

for i in range(0,53):
    wp.append('Week_{}'.format(i))

def weekly_count(df,k,k1):
    d = df.loc[df[k]==df[k1]]
    d1 = df.loc[df[k]!=df[k1]]
    pw = Counter(d[k])
    d1_1 = list(d1[k])
    d1_2 = list(d1[k1])
    for i,week in enumerate(d1_1):
        pw[week] += 1
        for j in range(1,(d1_2[i]-week)+1,1):
            pw[week+j] += 1
    return pw

patients_weekly = weekly_count(patients,'Kontakt startdato Uge nummer','Kontakt slutdato Uge nummer')
p = dict(sorted(patients_weekly.items()))

with open('./Data/Patients_Weekly.json', 'w') as f:
    json.dump(p, f)
