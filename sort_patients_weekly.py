import pandas as pd
import numpy as np
import json
patients = pd.read_csv('./Data/patiens_arrived.csv',sep = ';')
order_data = pd.read_csv('./Data/order_data.csv',sep = ',')

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

for i in range(1,53):
    wp.append('Week_{}'.format(i))

dictionary = {}
for dep in list(set(patients['Department'])):
    patients_weekly = []
    df = patients[patients['Department'] == dep]
    for i in range(1,53):
        df1 = df[df['Kontakt startdato Uge nummer'] == i]
        patients_weekly.append(len(df1))
    dictionary[dep] = patients_weekly
    dictionary['AHOC, The Department of Anesthesiology'] = [0]*52
patients1 = pd.DataFrame.from_dict(dictionary,orient='index')
patients1 = patients1.reset_index(drop=False)
wp.insert(0,'Department')
patients1.columns = wp

patients1.to_csv('./Data/patients_weekly.csv',index=False)
