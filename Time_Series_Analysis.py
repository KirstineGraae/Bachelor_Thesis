import json
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

f = open('./Data/c1.json')
cons = json.load(f)

def ACF(c,k):
    print(a)
    df = pd.DataFrame(list(zip(c[k])), columns=[k])


for key in cons.keys():
    ACF(cons,key)

dta = sm.datasets.sunspots.load_pandas().data
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
del dta["YEAR"]
sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40)
plt.show()
print(a)