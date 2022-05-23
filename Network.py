import pandas as pd
from collections import Counter

con_data = pd.read_csv('./Data/con_data.csv',low_memory = False)


def FindConnections(df, deps):
    Connections = {}
    for ATC in list(set(df['ATC5'])):
        Edges = []
        for dep in deps:
            df1 = df[df['Department'] == dep]
            df1_ATC = Counter(df1['ATC5'])
            if ATC in list(df1_ATC.keys()):
                a = [dep] * df1_ATC[ATC]
                Edges.extend(a)
            else:
                continue
        Connections[ATC] = Edges

    return Connections

Connections = FindConnections(con_data,list(set(con_data['Department'])))


print(a)