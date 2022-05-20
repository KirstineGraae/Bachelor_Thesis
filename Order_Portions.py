import pandas as pd
from collections import Counter

con_data = pd.read_csv('./Data/con_data_ATC_match.csv',sep=',',low_memory= False)
order_data = pd.read_csv('./Data/order_data_ATC_match.csv',sep=',',low_memory = False)
#apo_data = pd.read_csv('./Data/Apovision_data.csv', sep=',',header=0,usecols = [2,3,4,5,15,16,17,18,22],low_memory=False)

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def unite_columns(df,name1,name2):
    df[name1] = df[name1].astype(float)
    df[name2] = df[name2].astype(float)
    df[name1] = df[[name1, name2]].max(1)
    return df

def order_portions_part1(order_data):
    # Select a few columns
    df = order_data.iloc[:, 5:8]
    # Make all letters lower case
    df['Package_size'] = df['Package_size'].str.lower()
    df['Package_size'] = df['Package_size'].str.replace(',','.')

    # Split string according to ml or mg
    df1 = df['Package_size'].str.split('ml|mg', expand=True)
    # Delete all white space
    df1[0] = df1[0].str.replace(' ', '')
    # Define the portion size of the object (ex. 300 ml)
    df1['Portionsize'] = df1[0].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Portionsize1'] = df1[0].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')
    # The portion size is no longer useful
    df1[0] = df1[0].map(lambda x: 'none' if (x.isnumeric()) else x)
    df1[0] = df1[0].map(lambda x: 'none' if (is_number(x)==True) else x)
    df1[1] = df1[1].fillna('none')
    df1[1] = df1[1].map(lambda x: 'none' if ([i for i in x if i == '(']) else x)
    # The quantity of units will be the only number in the column
    df1['Quantity'] = df1[1].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    df1['Quantity'] = df1['Quantity'].replace('', 0,regrex=True)

    return df1[0], df1['Portionsize'], df1['Quantity']

order_data['Leftover'],order_data['Portionsize'],order_data['Quantity'] = order_portions_part1(order_data)

def order_portions_part2(order_data):
    df = order_data.iloc[:,-3:]
    df1 = df['Leftover'].str.split('stk|doser|dosis', expand=True)
    df1[['Portionsize', 'Quantity']] = df[['Portionsize', 'Quantity']]
    df1['Quantity1'] = df1[0].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Quantity2'] = df1[0].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Quantity1', 'Quantity2')

    df1[0] = df1[0].map(lambda x: 'none' if (x.isnumeric()) else x)
    df1[0] = df1[0].map(lambda x: 'none' if (is_number(x) == True) else x)

    df1[1] = df1[1].fillna('none')
    df1[1] = df1[1].map(lambda x: 'none' if ([i for i in x if i == '(']) else x)
    df1 = unite_columns(df1,'Quantity', 'Quantity1')

    return df1[0], df1['Portionsize'], df1['Quantity']


order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part2(order_data)

def order_portions_part3(order_data):

    df = order_data.iloc[:,-3:]
    df1 = df['Leftover'].str.split('g', expand=True)
    df1[['Portionsize', 'Quantity']] = df[['Portionsize', 'Quantity']]
    df1['Portionsize1'] = df1[0].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Portionsize2'] = df1[0].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Portionsize1', 'Portionsize2')
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')

    df1[0] = df1[0].map(lambda x: 'none' if (x.isnumeric()) else x)
    df1[1] = df1[1].fillna('none')
    df1[1] = df1[1].map(lambda x: x if ([i for i in x if i == '.']) else 'none')
    df1[1] = df1[1].map(lambda x: 'none' if ([i for i in x if i == ')']) else x)
    df1['Portionsize1'] = df1[1].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    df1['Portionsize1'] = df1['Portionsize1'].replace('', 0)
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')

    return df1[0], df1['Portionsize'], df1['Quantity']

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part3(order_data)

def order_portions_part4(order_data,sep):
    df = order_data.iloc[:, -3:]
    df1 = df['Leftover'].str.split(sep, expand=True)
    df1[['Portionsize', 'Quantity']] = df[['Portionsize', 'Quantity']]
    df1['Quantity1'] = df1[0].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Quantity2'] = df1[0].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Quantity1', 'Quantity2')
    df1 = unite_columns(df1, 'Quantity', 'Quantity1')

    df1[0] = df1[0].map(lambda x: 'none' if (x.isnumeric()) else x)
    df1[0] = df1[0].map(lambda x: 'none' if (is_number(x) == True) else x)
    df1[1] = df1[1].fillna('none')
    df1[1] = df1[1].map(lambda x: 'none' if ([i for i in x if i == '(']) else x)

    df1['Portionsize1'] = df1[1].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Portionsize2'] = df1[1].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Portionsize1', 'Portionsize2')
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')

    return df1[0], df1['Portionsize'], df1['Quantity']

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part4(order_data,sep='x')

def order_portions_part5(order_data,sep):
    df = order_data.iloc[:, -3:]
    df1 = df['Leftover'].str.split(sep, expand=True)
    df1[['Portionsize', 'Quantity']] = df[['Portionsize', 'Quantity']]
    df1['Quantity1'] = df1[0].map(lambda x: x if (x.isnumeric()) else 0)
    df1['Quantity2'] = df1[0].map(lambda x: x if (is_number(x) == True) else 0)
    df1 = unite_columns(df1, 'Quantity1', 'Quantity2')
    df1 = unite_columns(df1, 'Quantity', 'Quantity1')

    df1[0] = df1[0].map(lambda x: 'none' if (x.isnumeric()) else x)
    df1[0] = df1[0].map(lambda x: 'none' if (is_number(x) == True) else x)
    df1[1] = df1[1].fillna('none')
    df1['Portionsize1'] = df1[1].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    df1['Portionsize1'] = df1['Portionsize1'].replace('', 0)
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')

    return df1[0], df1['Portionsize'], df1['Quantity']

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part5(order_data,sep = 'amp.')

def order_portions_part6(order_data):
    df = order_data.iloc[:, -3:]
    df1 = df['Leftover'].str.split('a', expand=True)
    df1[['Portionsize', 'Quantity']] = df[['Portionsize', 'Quantity']]

    df1[1] = df1[1].fillna('none')
    df1['Portionsize1'] = df1[1].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    df1['Portionsize1'] = df1['Portionsize1'].replace('', 0)
    df1 = unite_columns(df1, 'Portionsize', 'Portionsize1')

    return df1[0], df1['Portionsize'], df1['Quantity']

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part6(order_data)

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part5(order_data,sep = 'kædeá')

def order_portions_part7(order_data):
    df = order_data.iloc[:, -3:]
    df['Leftover'] = df['Leftover'].fillna('none')
    df['Quantity1'] = df['Leftover'].map(lambda x: ''.join([i for i in x if i.isdigit()]))
    df['Leftover'] = df['Leftover'].map(lambda x: x if (x.isnumeric()) else 'none')
    df['Quantity1'] = df['Quantity1'].replace('', 0)
    df = unite_columns(df, 'Quantity1', 'Quantity1')

    return df['Leftover'], df['Portionsize'], df['Quantity']

order_data['Leftover'], order_data['Portionsize'], order_data['Quantity'] = order_portions_part7(order_data)

def clean_orders(df):
    df.drop('Leftover', axis=1, inplace=True)
    df['Quantity1'] = df.apply(lambda x: float(1) if x['Quantity'] == 0 and x['Portionsize'] != 0 else float(0), axis=1)
    df['Quantity'] = df[['Quantity', 'Quantity1']].max(1)
    df.drop('Quantity1', axis=1, inplace=True)

    return df
order_data = clean_orders(order_data)

order_data.to_csv('./Data/order_data_portions_added.csv', index=False)


print(a)