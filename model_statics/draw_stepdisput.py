import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import powerlaw
import math
def lognormal(x,mu,sigma):
    first=x*sigma*math.sqrt(math.pi*2)
    second=(math.log(x)-mu)**2/(2*(sigma**2))
    third=math.pow(math.e,-second)/first
    return third
def dis_func(row):
    Ox = row['O_lon']
    Oy = row['O_lat']
    Dx = row['D_lon']
    Dy = row['D_lat']
    return math.sqrt((Ox-Dx)**2+(Oy-Dy)**2)

pre='gra_flux'
model_pre='model_value'
path='D:\\data_test\\shanghai\\rank\\modelR1_3000_exp1.31.csv'
     ##'C:\\Users\\Administrator\\Desktop\\test\\od_test\\beijing\\xdis0model.csv'
od_dataframe=pd.read_csv(path)
dislist=[]
dislist_flux=[]
dislist_preflux=[]

for index,row in od_dataframe.iterrows():
    if((index+1)%1000==0):
        print ('we have cal rows of data is '+str(index+1))
    value=int(row[model_pre])
    flux=int(row['flux'])
    pre_flux=int(row[pre]*100)

    dis = float(row['Dis'])
    if(value):
        dislist.extend((np.ones(value)*dis).tolist())
    if(pre_flux):
        dislist_preflux.extend((np.ones(pre_flux)*dis).tolist())
    if(flux):
        dislist_flux.extend((np.ones(flux)*dis).tolist())

interval=np.linspace(0.01,.8,40,endpoint=False)
bins=0.5*(interval[1:]+interval[:-1])


# ax=sbn.distplot(dislist,bins=interval,hist=False,norm_hist=False,color='dodgerblue')
histom=np.histogram(a=dislist,bins=interval,density=True)
plt.scatter(bins,histom[0],marker='v',c='#377eb8',label='model',s=50)
plt.plot(bins,histom[0],c='dodgerblue')
# results.plot_pdf()


# sbn.distplot(dislist_flux,bins=interval,hist=False,norm_hist=False,color='firebrick',ax=ax)
histom=np.histogram(a=dislist_flux,bins=interval,density=True)
plt.scatter(bins,histom[0],marker='v',c='#e41a1c',label='real_data',s=50)
# plt.plot(bins,histom[0],c='orangered')
results=powerlaw.Fit(dislist_flux,xmin=min(dislist_flux))
# print (results.alpha,results.xmin,results.xmax)
# ax=results.plot_pdf()
# print (results.exponential.parameter1)
mu=results.lognormal.mu
sigma=results.lognormal.sigma
x=np.linspace(0.02,1,50)
y=[lognormal(item,mu,sigma) for item in x]
plt.plot(x,y)
print(mu,sigma)
results.lognormal.plot_pdf()
print (1)
# ax=sbn.distplot(dislist_preflux,bins=interval,hist=False,norm_hist=False,color='orange',ax=ax)
histom=np.histogram(a=dislist_preflux,bins=interval,density=True)
plt.scatter(bins,histom[0],marker='v',c='#4daf4a',label='gra_flux',s=50)
plt.plot(bins,histom[0],c='#009688')
# results=powerlaw.Fit(dislist_preflux,xmin=min(dislist))
# results.plot_pdf()

plt.ylabel('P(dist)')
plt.xlabel('distance(m),r')
plt.xlim(0.02,1)
plt.ylim(0.00001,50)
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()