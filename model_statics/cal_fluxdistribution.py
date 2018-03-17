import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
color=['#c23531','#2f4554','#61a0a8','#d48265','#91c7ae','#749f83','#ca8622','#bda29a','#6e7074','#546570','#c4ccd3']

path=r'D:\modelRShanghai_30000.csv'
attribute='flux'
attribute2='model_value_scale'
df=pd.read_csv(path)
temp_df=df[df[attribute]!=0]
temp_df=temp_df[temp_df['O_id']!=temp_df['D_id']]
valuelist1=np.sort(temp_df[attribute].values)
unique1,cont1=np.unique(valuelist1,return_counts=True)
cont1=cont1/df.shape[0]
plt.scatter(unique1,cont1,c=color[0],s=50)

temp_df=df[df[attribute2]>0]
temp_df=temp_df[temp_df['O_id']!=temp_df['D_id']]
valuelist2=np.sort(temp_df[attribute2].values)
valuelist2=np.round(valuelist2)
unique2,cont2=np.unique(valuelist2,return_counts=True)
cont2=cont2/df.shape[0]
plt.scatter(unique2,cont2,c=color[1],s=50)


# rank2=range(len(valuelist2)+1,1,-1)
# plt.scatter(rank1,valuelist1,c='y')
# plt.scatter(rank2,valuelist2,c='r')

plt.xscale('log')
plt.yscale('log')
plt.ylim(0.00001,1)
plt.show()