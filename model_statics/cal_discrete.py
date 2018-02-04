##__ cal the displacement in the discrete space
import pandas as pd
import math
import Point
import time
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import powerlaw
import numpy as np

def str2shapeO(row):
    str=row['O_geometry']
    coor_str=str.replace('(',')').split(')')[2]
    coor_str=coor_str.replace(', ',',')
    coorlist=coor_str.split(',')
    valuelist=[]
    for item in coorlist:
        if(item):
            temp=item.split(' ')
            valuelist.append((float(temp[0]),float(temp[1])))
    x=0
    y=0
    for item in valuelist[0:4]:
        x+=item[0]
        y+=item[1]
    return [x/(len(valuelist)-1),y/(len(valuelist)-1)]
def str2shapeD(row):
    str=row['D_geometry']
    coor_str=str.replace('(',')').split(')')[2]
    coor_str=coor_str.replace(', ',',')
    coorlist=coor_str.split(',')
    valuelist=[]
    for item in coorlist:
        if(item):
            temp=item.split(' ')
            valuelist.append((float(temp[0]),float(temp[1])))
    x=0
    y=0
    for item in valuelist[0:4]:
        x+=item[0]
        y+=item[1]
    return [x/(len(valuelist)-1),y/(len(valuelist)-1)]

def dis_func1(row):
    str1='O_geometry'
    str2='D_geometry'
    Ox=row[str1][0]
    Oy = row[str1][1]
    Dx=row[str2][0]
    Dy=row[str2][1]
    return math.sqrt((Ox-Dx)**2+(Oy-Dy)**2)

    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)
def get_point_from_geodf(path):
    df=pd.read_csv(path)
    df['O_geometry']=df.apply(str2shapeO,axis=1)
    df['D_geometry'] = df.apply(str2shapeD, axis=1)
    df['Dis']=df.apply(dis_func1,axis=1)
    # df.to_csv(path)
    return df

path='D:\\data_test\\test\\od_test\\beijing\\xdis0.02\\beijing10.02od.csv'
df=get_point_from_geodf(path)
flux='flux'
dislist_flux=[]
for index,row in df.iterrows():
    if((index+1)%1000==0):
        print ('we have cal rows of data is '+str(index+1))
    fluxtemp=int(row[flux])
    dis = float(row['Dis'])
    if(fluxtemp):
        dislist_flux.extend((np.ones(fluxtemp)*dis).tolist())

Fit=powerlaw.Fit(dislist_flux,xmin=0.05)
Fit.plot_pdf()
Fit.power_law.plot_pdf()
Fit.lognormal.plot_pdf()
print (Fit.lognormal.mu)
# print(Fit.distribution_compare('lognormal','truncated_power_law'))
# print(Fit.distribution_compare('power_law','lognormal'))
print (Fit.alpha)
plt.show()