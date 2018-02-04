import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbn
import powerlaw
path='D:\\data_test\\shanghai\\gravity\\modeldis11_3000_exp2.45.csv'
df=pd.read_csv(path)

df=df[df['flux']!=0]
dis=df['Dis'].values
ON_OD=df['D_N']*df['O_N']
ON_OD=ON_OD.values
flux=df['flux'].values
flux_OD=ON_OD/flux
flux_OD=flux_OD/np.percentile(flux_OD,q=25)
flux=[]
for index,item in enumerate(flux_OD):
    temp=np.ones(shape=int(round(item)))*dis[index]
    flux.extend(temp.tolist())
    if(index%100==0):
        print(index)

Fit=powerlaw.Fit(flux,xmin=min(flux),xmax=0.15)
Fit.plot_pdf()

x=np.linspace(0.01,1,100)

y=x**(-2.45)
plt.plot(x,y)
plt.xscale('log')
plt.yscale('log')
plt.show()