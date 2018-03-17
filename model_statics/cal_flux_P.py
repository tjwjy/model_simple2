import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import powerlaw as pl
color=['#c23531','#2f4554','#61a0a8','#d48265','#91c7ae','#749f83','#ca8622','#bda29a','#6e7074','#546570','#c4ccd3']

path=r'D:\data_test\beijing\new\rank\modelR_30000_rank1.278.csv'
attribute='flux'
attribute2='model_value_scale'
df=pd.read_csv(path)
temp_df=df[df[attribute]!=0]
temp_df=temp_df[temp_df['O_id']!=temp_df['D_id']]
valuelist1=np.sort(temp_df[attribute].values)
model=pl.Fit(valuelist1,xmin=1,discrete=True)
# model.plot_pdf()
position,p=model.pdf()

choiceIndex=[2* i for i in range(int(len(p)/2))]
position=position[choiceIndex]
p=p[choiceIndex[:-1]]

plt.scatter(0.5*(position[1:]+position[:-1]),p,c=color[0],s=100,marker='H')

temp_df=df[df[attribute2]>0]
temp_df=temp_df[temp_df['O_id']!=temp_df['D_id']]
valuelist2=np.sort(temp_df[attribute2].values)
valuelist2=np.round(valuelist2)
model=pl.Fit(valuelist2,xmin=1,discrete=True)
# model.plot_pdf(c=color[0])
position,p=model.pdf()

# choiceIndex=[2* i for i in range(int(len(p)/2))]
position=position[choiceIndex]
p=p[choiceIndex[:-1]]

plt.scatter(0.5*(position[1:]+position[:-1]),p,c=color[1],s=100,marker='o')

# rank2=range(len(valuelist2)+1,1,-1)
# plt.scatter(rank1,valuelist1,c='y')
# plt.scatter(rank2,valuelist2,c='r')

plt.xscale('log')
plt.yscale('log')
x=np.arange(0,10,2)
y=1/pow(10,x)
plt.yticks(y,[r'$10^{0}$',r'$10^{-2}$',r'$10^{-4}$',r'$10^{-6}$',r'$10^{-8}$'])
plt.ylim(0.00000001,1)
plt.savefig('D:\shenzhenP.png',dpi=200)
plt.show()