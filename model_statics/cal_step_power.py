import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import powerlaw
import sklearn
path='D:\\data_test\\changsha\\modelR1_3000_rank1.29.csv'
flux='flux'
od_dataframe=pd.read_csv(path)
dislist_flux=[]


for index,row in od_dataframe.iterrows():
    if((index+1)%1000==0):
        print ('we have cal rows of data is '+str(index+1))
    fluxtemp=int(row[flux])
    dis = float(row['Dis'])
    if(fluxtemp):
        dislist_flux.extend((np.ones(fluxtemp)*dis).tolist())

interval=np.linspace(0.05,0.57,30,endpoint=False)
bins=0.5*(interval[1:]+interval[:-1])


sbn.distplot(dislist_flux,bins=interval,hist=False,norm_hist=False,color='firebrick')
histom=np.histogram(a=dislist_flux,bins=interval,normed=True,density=True)
plt.scatter(bins,histom[0],marker='v',c='firebrick',label='real_data',s=50)
results=powerlaw.Fit(dislist_flux,xmin=0.02)
print (results.alpha,results.xmin,results.xmax)
results.plot_pdf()

plt.ylabel('P(dist)')
plt.xlabel('distance(m),r')
plt.xlim(0.05,.6)
plt.ylim(0.00001,50)
plt.xscale('log')
plt.yscale('log')
plt.legend()
print('OK')
plt.show()

