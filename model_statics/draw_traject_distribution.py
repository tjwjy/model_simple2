import seaborn as sns
import pandas as pd
import numpy as np
import IO
import Cal
import matplotlib.pyplot as plt
color=['#c23531','#2f4554','#61a0a8','#d48265','#91c7ae','#749f83','#ca8622','#bda29a','#6e7074','#546570','#c4ccd3']
path=r'D:\data_test\beijing\new\rank\modelR_30000_rank1.278.txt'
read = IO.IO()
Envir, offset = read.read_Envr(path=path)

##__cal the all num between ods
data_mid, offset = read.read_txt_step(path=path, offset=offset, temp_envir=Envir)
flag = 0
pointlist=[]
people_id=3
for i in range(0,people_id):
    pointlist=data_mid.route
    data_mid, offset = read.read_txt_step(path=path, offset=offset, temp_envir=Envir)
    flag += 1
    if (flag % 100 == 0):
        print('cal people num is' + str(flag))
unique,count=np.unique(np.array([point.ID for point in pointlist]),return_counts=True)
locationx_List=[item.x for item in pointlist]
locationy_List=[item.y for item in pointlist]
sizeList=[count[np.argwhere(unique==point.ID)[0]] for point in pointlist  ]
sns.kdeplot(locationx_List,locationy_List,shade=True,n_levels=40,cmap='Reds')
plt.scatter(locationx_List,locationy_List,s=sizeList*3)
figure=plt.gcf()
figure.set_size_inches(5,5)
plt.xticks([])
plt.yticks([])
plt.show()