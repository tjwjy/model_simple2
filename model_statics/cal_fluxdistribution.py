import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
path=r'C:\Users\Administrator\Desktop\taxidata\beijing.csv'
df=pd.read_csv(path)
temp_df=df[df['flux']!=0]
temp_df=temp_df[temp_df['O_id']!=temp_df['D_id']]
valuelist1=np.sort(temp_df['flux'].values)

# temp_df=df[df['model_value_scale']>0]
# valuelist2=np.sort(temp_df['model_value'].values)
# valuelist2=np.round(valuelist2)
#  unique2,cont2=np.unique(valuelist2,return_counts=True)
#  rank1=range(len(valuelist1)+1,1,-1)
#  plt.scatter(unique2,cont2,c='r')
unique1,cont1=np.unique(valuelist1,return_counts=True)
cont1=cont1/len(valuelist1)
# cont2=cont2/len(valuelist2)

# rank2=range(len(valuelist2)+1,1,-1)
# plt.scatter(rank1,valuelist1,c='y')
# plt.scatter(rank2,valuelist2,c='r')
plt.scatter(unique1,cont1,c='y')

plt.xscale('log')
plt.yscale('log')
plt.ylim(0.000001,0.9)
plt.show()