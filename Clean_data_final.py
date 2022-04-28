import pandas as pd
import numpy as np
from collections import Counter
import re
data_path = './Data'

order_data = pd.read_csv(data_path + '/order_weekly.csv',sep = ';',header=2,low_memory=False)
con_data = pd.read_csv(data_path + '/Northwing_consumption.csv',sep=';',low_memory=False)
match_data = pd.read_csv(data_path + '/Department_Conversions.csv',sep = ';')

def clean_order(order_data):
    #New column names
    new_names = ['Department', 'ATC5', 'Order_number', 'Order_name', 'Strength', 'Type_of_Medicine',
                          'Package_size', 'Cost', 'Number_of_Packages']
    #Columns to drop -
    drop_cols = ['Kunder Debitor Nr Navn', 'DDD']

    for i in range(1, 53, 1):
        drop_cols.append('DDD.{}'.format(i))
        new_names.append('Cost_w{}'.format(i))
        new_names.append('Number_of_Packages_w{}'.format(i))
    for d in drop_cols:
        order_data.drop(d,axis=1,inplace=True)
    order_data.columns = new_names
    order_data.drop(0,inplace=True)
    order_data.reset_index(drop=True,inplace=True)
    order_data['Department'] = order_data['Department'].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    return order_data
order_data = clean_order(order_data)

def clean_con(con_data):
    # New column names
    new_names = ['Department', 'ATC_ID', 'ATC5', 'Medicine_name', 'Generic_name', 'Trade_name', 'Date',
                        'Strength','Strength_measure', 'Type_of_Medicine', 'Way', 'Number_ordinations', 'Dosis', 'Dosis_measure']
    #Columns to drop
    drop_cols = ['P. Krypteret ID', 'Patientafdeling navn', 'Patientafsnit navn']

    #Drop columns
    for d in drop_cols:
        con_data.drop(d,axis=1,inplace=True)
    #Give new names
    con_data.columns = new_names
    con_data['Department'] = con_data['Department'].str.split(',').str[0]
    con_data['Department'].str.replace(r'[^0-9]+', '', regex=True)
    con_data['Date'] = pd.to_datetime(con_data['Date'])

    return con_data
con_data = clean_con(con_data)

def clean_match(match_data):
    new_names = ['Department_order','Department_names']
    #Keep following
    keep = ['Kunder Afdeling Nr Navn','SP afd navn SOR']
    match_data = match_data[keep]
    match_data.columns = new_names
    match_data['Department_order'] = match_data['Department_order'].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    match_data['Department_abbs'] = match_data['Department_names'].str.split(',').str[0]
    return match_data
match_data = clean_match(match_data)

def dep_match(match_data,df,j):
    if j == 'con':
        dicts = dict(zip(list(match_data['Department_abbs']), list(match_data['Department_names'])))
    elif j == 'order':
        dicts = dict(zip(list(match_data['Department_order']), list(match_data['Department_names'])))
    df['Department'] = df['Department'].apply(lambda x: dicts[x])

    return df
con_data = dep_match(match_data,con_data,j = 'con')
order_data = dep_match(match_data,order_data,j = 'order')

def intersection_deps(con_data,order_data):
    deps_con = set(con_data['Department'])
    deps_order = set(order_data['Department'])
    inter = deps_con.intersection(deps_order)

    return list(inter)

intersections_departments = intersection_deps(con_data,order_data)

con_data = con_data[con_data['Department'].isin(intersections_departments)]
order_data = order_data[order_data['Department'].isin(intersections_departments)]

def to_english(df,intersection):
    #Convert to english department names
    english_names = ['AHOC, The Department of Anesthesiology','ANEU, Department of Neuroanesthesiology',
     'F, Department of Ortorhinolaryngology', 'N, Department of Neurology', 'NK, Department of Neurosurgery', 'OE, Department of Ophthalmology',
     'PBB, Department of Plastic Surgery and Burns Treatment','U, Department of Orthopedic Surgery',
     'X, Department of Diagnostic Radiology']
    english_names1 = [x.split(',') for x in english_names]
    current_names = sorted(intersection)

    for i,dep in enumerate(current_names):
        name = dep.split(',')
        name = name[0].split(' ')
        abbrev = name[1]
        for j,abb in enumerate(english_names1):
            if abbrev == abb[0]:
                df['Department'] = df['Department'].replace(dep, english_names[j])
            else:
                continue
    df['Department'] = df['Department'].replace('RH Ã˜, Ã˜JENKLINIKKEN, Ã˜','OE, Department of Ophthalmology')
    return df
order_data =  to_english(order_data,intersections_departments)
con_data = to_english(con_data,intersections_departments)

def numeric_transform(df):
    cols = list(df.columns)
    for col in cols[7:]:
        df[col] = df[col].astype(str)
        df[col] = [x.replace('.', '') for x in df[col]]
        df[col] = [x.replace(',', '.') for x in df[col]]
        df[col] = df[col].astype(float)
    return df
order_data = numeric_transform(order_data)

#Convert to correct date format
con_data['Date'] = pd.to_datetime(con_data['Date'],format='%Y-%m-%d')

#Check if any medicine is consumped 0 times
consumptions = Counter(con_data['Number_ordinations'])
zero_consumptions = consumptions['0']
if zero_consumptions != 0:
    print('ZERO CONSUMPTION')

#Make a new row for every singel consumptions seen in 'Antal ordinationer'
con_data = con_data.loc[con_data.index.repeat(con_data['Number_ordinations'])].reset_index(drop=True)
con_data['Number_ordinations'] = 1

#Save CSV
con_data.to_csv('./Data/con_data.csv',index = False)
order_data.to_csv('./Data/order_data.csv',index = False)

