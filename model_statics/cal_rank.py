import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
import powerlaw
import numpy as np
import model_statics.color as color1
def cal_PWO2(dataframe):
    df=dataframe
    slist=[]
    flag=0
    for i,row in df.iterrows():
        flag+=1
        O=row['O_id']
        D=row['D_id']
        dis=row['Dis']
        O_N=row['O_N']
        D_N=row['D_N']
        if(O_N+D_N==0):
            continue
        temp_dfO=df[df['O_id']==O]
        temp_df=temp_dfO[temp_dfO['Dis']<dis]
        rank=temp_df.shape[0]+1
        if(flag%1000==0):
            print (i)
        slist.append([O,D,rank])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','rank'])
    df=df.set_index(keys=['O_id','D_id'],drop=False)
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['rank']=df1['rank']
    return df

path=r'D:\data_test\changsha\new\rank\modelR_3000_rank1.280.csv'
df=pd.read_csv(path)
df=cal_PWO2(df)
df['flux']=df['flux']/(df['O_N']*df['D_N'])
grouped=df['flux'].groupby(df['rank'])
rankflux=grouped.sum()
rankflux=rankflux/(rankflux.min() if rankflux.min()!=0 else rankflux.mean()/100)
# plt.scatter(np.linspace(1,len(rankflux.values)+1,len(rankflux.values),endpoint=False),rankflux.values)
ranklist=[]
for i in range(min(rankflux.index),rankflux.shape[0]+1):
    for item in range(0,int(rankflux[i])):
        ranklist.append(i)
fit=powerlaw.Fit(ranklist,discrete=True,xmin=1)
ax=fit.plot_pdf(color=color1.get_color(0),original_data=True)
fit.power_law.plot_pdf(ax=ax,color=color1.get_color(1))
bins,pdf=fit.pdf(original_data=True)
position=0.5*(bins[1:]+bins[:-1])
plt.scatter(position,pdf,color=color1.get_color(0))
print(fit.alpha,fit.sigma,fit.xmin)
x=np.linspace(1,1000,10000)
# plt.plot(x,x**-1.30)
plt.xscale('log')
plt.yscale('log')
plt.savefig('D:\\rankdistribution.png',dpi=200)
plt.show()