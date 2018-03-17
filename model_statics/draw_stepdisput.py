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

color=['#c23531','#2f4554','#61a0a8','#d48265','#91c7ae','#749f83','#ca8622','#bda29a','#6e7074','#546570','#c4ccd3']
pre='gra_flux'
model_pre='model_value_scale'
path=r'D:\data_test\shanghai\new\rank\modelR1_30000_rank1.289.csv'
     ##'C:\\Users\\Administrator\\Desktop\\test\\od_test\\beijing\\xdis0model.csv'
od_dataframe=pd.read_csv(path)
dislist=[]
dislist_flux=[]
dislist_preflux=[]
scale=5
for index,row in od_dataframe.iterrows():
    if((index+1)%1000==0):
        print ('we have cal rows of data is '+str(index+1))
    value=int(int(row[model_pre])/scale)
    flux=int(int(row['flux'])/scale)
    pre_flux=int(int(row[pre]*100)/scale)

    dis = float(row['Dis'])*100
    if(value):
        dislist.extend((np.ones(value)*dis).tolist())
    if(pre_flux):
        dislist_preflux.extend((np.ones(pre_flux)*dis).tolist())
    if(flux):
        dislist_flux.extend((np.ones(flux)*dis).tolist())

interval=np.linspace(1,100,50,endpoint=False)
bins=0.5*(interval[1:]+interval[:-1])


# model=powerlaw.Fit(dislist_flux,xmin=2)
# position,p=model.pdf(original_data=True)
# plt.scatter(0.5*(position[1:]+position[:-1]),p,marker='H',c=color[0],label='model',s=50)
#
# model=powerlaw.Fit(dislist,xmin=2)
# position,p=model.pdf(original_data=True)
# plt.scatter(0.5*(position[1:]+position[:-1]),p,marker='H',c=color[2],label='model',s=50)




histom=np.histogram(a=dislist_flux,bins=interval,density=True)
plt.scatter(bins,histom[0],marker='o',c=color[0],label='real_data',s=80,zorder=1)
plt.plot(bins,histom[0],c=color[0],zorder=1)

histom=np.histogram(a=dislist,bins=interval,density=True)
plt.scatter(bins,histom[0],marker='H',c=color[1],label='model',s=100,zorder=2)
plt.plot(bins,histom[0],c=color[1],zorder=2)
# results.plot_pdf()
# results=powerlaw.Fit(dislist_flux,xmin=min(dislist_flux))
# print (results.alpha,results.xmin,results.xmax)
# ax=results.plot_pdf()
# print (results.exponential.parameter1)
# mu=results.lognormal.mu
# sigma=results.lognormal.sigma
# x=np.linspace(0.02,1,50)
# y=[lognormal(item,mu,sigma) for item in x]
# plt.plot(x,y)
# print(mu,sigma)
# results.lognormal.plot_pdf()
# print (1)
# ax=sbn.distplot(dislist_preflux,bins=interval,hist=False,norm_hist=False,color='orange',ax=ax)

# histom=np.histogram(a=dislist_preflux,bins=interval,density=True)
# plt.scatter(bins,histom[0],marker='p',c='#4daf4a',label='gra_flux',s=50)
# plt.plot(bins,histom[0],c=color[0])

# results=powerlaw.Fit(dislist_preflux,xmin=min(dislist))
# results.plot_pdf()

plt.ylabel('P(dist)')
plt.xlabel('distance(km),r')
plt.xscale('log')
plt.yscale('log')
x=np.arange(0,10,2)
y=1/pow(10,x)
plt.yticks(y,[r'$10^{0}$',r'$10^{-2}$',r'$10^{-4}$',r'$10^{-6}$',r'$10^{-8}$'])
plt.xlim(1.5,100)
plt.ylim(0.0000001,1)
plt.legend()
plt.savefig('D:\\step.png',dpi=200)
plt.show()