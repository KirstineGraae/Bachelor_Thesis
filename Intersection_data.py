import pandas as pd
import pickle

con_data = pd.read_csv('./Data/con_data.csv', sep=',', low_memory= False)
order_data = pd.read_csv('./Data/order_data.csv', sep=',')

def change_V07(df):
    s = df['ATC5'].str.slice(stop=3)
    a = s[s == 'V07'].index
    for i in range(len(a)):
        df.at[a[i], 'ATC5'] = 'V07'
    return df

con_data = change_V07(con_data)
order_data = change_V07(order_data)

def ATC_matching(order_data, con_data):
    dep = list(set(con_data['Department']))
    dep.sort()
    ATC_table = []
    ATC_dict = {}
    for i, name in enumerate(dep):
        df = con_data[con_data['Department'].isin([dep[i]])]
        df1 = order_data[order_data['Department'].isin([dep[i]])]

        con_ATC5,order_ATC5 = set(df['ATC5']), set(df1['ATC5'])
        ATC5_int = con_ATC5.intersection(order_ATC5)
        ATC_dict[name] = list(ATC5_int)
        r = [len(con_ATC5), len(order_ATC5), len(ATC5_int)]
        ATC_table.append(r)

    ATC_df = pd.DataFrame(ATC_table,index = dep)
    ATC_df.columns = ['Consumption_ATC','Order_ATC','Intersection_ATC']

    return ATC_df, ATC_dict

ATC_df, ATC_dict = ATC_matching(order_data, con_data)

def remove_not_intersection(dict, df, df1):

    keys = list(dict.keys())
    values = list(dict.values())

    df_list = []
    df1_list = []

    for i, key in enumerate(keys):
        # Locate where they are used
        df2 = df.loc[lambda df: df['Department'] == key]
        df3 = df1.loc[lambda df1: df1['Department'] == key]
        # Remove ATCs not in intersection
        df2 =  df2[df2['ATC5'].isin(values[i])]
        df3 = df3[df3['ATC5'].isin(values[i])]
        df_list.append(df2)
        df1_list.append(df3)

    df = pd.concat(df_list)
    df1 = pd.concat(df1_list)

    return df, df1

con_data, order_data = remove_not_intersection(ATC_dict, con_data, order_data)

def not_needed_deps(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    remove_list = []
    for i in range(len(values)):
        if len(values[i]) <= 20:
            remove_list.append(keys[i])
        else:
            continue
    return remove_list

remove_list = not_needed_deps(ATC_dict)

con_data = con_data[(con_data['Department'] != remove_list[0])]
order_data = order_data[(order_data['Department'] != remove_list[0])]

for i in remove_list:
    del ATC_dict[i]

# Save data as files
con_data.to_csv('./Data/con_data_ATC_match.csv',index = False)
order_data.to_csv('./Data/order_data_ATC_match.csv',index = False)

# Save pickle of consumption department names
with open("./Data/ATC_dict", "wb") as fp:
    pickle.dump(ATC_dict, fp)
