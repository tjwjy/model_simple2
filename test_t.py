import pandas as pd
import Environment
import agent2
import math
import Point
import IO
import time
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import seaborn as sns
import matplotlib.pyplot as plt
args_model=[0.6,-0.21]
args_time=[2,1]
args_steps=[3.15]
gama=1

def dis_func1(Point1,Point2):
    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)

def dis_func2(dataframe):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    for i,row in df.iterrows():
        flag+=1
        O=row['O_id']
        D=row['D_id']
        dis=row['dis']
        O_N=row['O_N']
        D_N=row['D_N']
        if(O_N+D_N==0):
            continue
        temp_dfO=df[df['O_id']==O]
        temp_df=temp_dfO[temp_dfO['dis']<=dis]
        s=temp_df['D_N'].sum()+O_N
        if(flag%1000==0):
            print (i)
        dict[(O,D)]=s
        slist.append([O,D,s])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','dis'])
    df=df.set_index(keys=['O_id','D_id'])
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['dis']=df1['dis']
    df.to_csv('D:\\dis.csv')
    return dict

def dis_func3(dataframe):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    for i,row in df.iterrows():
        flag+=1
        O=row['O_id']
        D=row['D_id']
        dis=row['dis']
        O_N=row['O_N']
        D_N=row['D_N']
        if(O_N+D_N==0):
            continue
        temp_dfO=df[df['O_id']==O]
        temp_df=temp_dfO[temp_dfO['dis']<=dis]
        s=temp_df.columns.size
        if(flag%1000==0):
            print (i)
        dict[(O,D)]=s
    return dict


def str2shape(row):
    str=row['geometry']
    coor_str=str.replace('(',')').split(')')[2]
    coor_str=coor_str.replace(', ',',')
    coorlist=coor_str.split(',')
    valuelist=[]
    for item in coorlist:
        if(item):
            temp=item.split(' ')
            valuelist.append((float(temp[0]),float(temp[1])))
    return Polygon(valuelist)

def get_point_from_geodf(path,gama):
    df=pd.read_csv(path)
    df['geometry']=df.apply(str2shape,axis=1)
    gdf=gpd.GeoDataFrame(data=df,geometry='geometry')
    gdf['point']=gdf.centroid
    pointlist=[]
    for index,row in gdf.iterrows():
        pointx,pointy=row['point'].x,row['point'].y
        weight=row['popsum']
        ID=row['id']
        temp_point = Point.Point(x=pointx, y=pointy, gridid=0, ID=ID, state=0,
                             weight=math.pow(weight, gama))
        temp_point.weight2=weight
        pointlist.append(temp_point)
    return pointlist
def run(args_steps = [3.15],path='D:\\beijing1000\\beijing01000grid.csv',pathod='D:\\beijing1000\\beijing01000od.csv'):
    ##the disput of population
    args_model = [0.6, -0.21]
    args_time = [1.5, 0.5]
    args_steps = args_steps
    gama = 1
    time1=time.localtime()
    path=path
    pathod=pathod
    PointList=get_point_from_geodf(path,gama=gama)
    PointList=PointList[0:3]
    Envir=Environment.Envronment(PointList,10,10)
    # Envir.cal_dis_dict(dis_function=dis_func1)
    # od_df=pd.read_csv(pathod)
    # od_df=od_df.set_index(keys=['O_id','D_id'],drop=False)

##cal dis for S. this model cal the raw distance
# temp_value=[]
# for item in Envir.dis_dict.items():
#     keys=list(item[0])
#     value=item[1]
#     keys.append(value)
#     temp_value.append(keys)
#
# dis_gdf=pd.DataFrame(data=temp_value,columns=['O','D','dis'])
# dis_gdf=dis_gdf.set_index(keys=['O','D'])
# od_df['dis']=dis_gdf['dis']
# Envir.dis_dict=dis_func2(od_df)

    P=np.ones(24)*.5
    simulate_time=200
    people_num=1000
    temp_routeList=[]
    flag=0

    time1=time.localtime()
    getmon=str(time1.tm_mon)
    getday=str(time1.tm_mday)
    gethour=str(time1.tm_hour)
    temp_path='D:\\modeldis'+str(gama)+'_'+str(people_num)+"_"+getmon+getday+gethour
    tList=[]
    for i in range(0,people_num):
    #model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
        model=agent2.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,environment=Envir)
        ts=model.simulate_dualcentric24(p=P)
        tList.extend(ts)

        if(flag%100==0):
            print (flag)
            print (time.localtime())
        flag+=1
    sns.distplot(a=tList,bins=range(24))
    plt.show()
    print (00)

run()