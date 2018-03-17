import pandas as pd
import Environment
import agent
import math
import Point
import IO
import time
import geopandas as gpd
import agent2
from shapely.geometry import Polygon


def dis_func1(Point1,Point2):
    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)

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
        s=temp_df.shape[0]
        if(flag%1000==0):
            print (i)
        dict[(O,D)]=s
    return dict


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
def dis_func2_1(dataframe,PointList):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    for point in PointList:
        O=point.ID
        flag+=1
        sample=dataframe.loc[dataframe['O_id']==O]
        sort_value=sample.sort_values(by=['dis'])
        rank=0
        pre_dis=0

        for itr, row in sort_value.iterrows():
            if(int(pre_dis/10)!=int(row['dis']/10)):
                rank+=1

            pre_dis=row['dis']
            D=row['D_id']
            dict[(O, D)] = rank
            slist.append([O, D, rank])
        #
        # if(O_N+D_N==0):
        #     continue
        # temp_dfO=df[df['O_id']==O]
        # temp_df=temp_dfO[temp_dfO['dis']<=dis]
        # s=temp_df['D_N'].sum()+O_N
        if(flag%10==0):
            print (flag)
        # dict[(O,D)]=s
        # slist.append([O,D,s])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','dis'])
    df=df.set_index(keys=['O_id','D_id'])
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['dis']=df1['dis']
    df.to_csv('D:\\dis.csv')

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

def get_point_from_shp(path,gama):
    gdf=gpd.read_file(path)

    gdf['point']=gdf.centroid
    pointlist=[]
    for index,row in gdf.iterrows():
        pointx,pointy=row['point'].x,row['point'].y
        weight=row['popsum']
        ID=int(row['id'])
        temp_point = Point.Point(x=pointx, y=pointy, gridid=0, ID=ID, state=0,
                             weight=math.pow(weight, gama))
        temp_point.weight2=weight
        pointlist.append(temp_point)
    return pointlist
def run(path=r'D:\data_test\mapdata\shanghai\\Shanghai_Pop_Lambert_filter.shp', pathod='E:\\data\\taxidata\\beijing.csv'):
    ##the disput of population
    args_model = [0.6, -0.21]
    args_time = [2, 1]
    args_steps = [1]
    gama = 1
    time1 = time.localtime()
    path = path
    pathod = pathod

    PointList=get_point_from_shp(path,gama=gama)
    Envir=Environment.Envronment(PointList,10,10)
    Envir.cal_dis_dict(dis_function=dis_func1)
    temp_value=[]

    for item in Envir.dis_dict.items():
        keys=list(item[0])
        value=item[1]
        keys.append(value)
        temp_value.append(keys)

    dis_gdf=pd.DataFrame(data=temp_value,columns=['O_id','D_id','dis'])
    dis_gdf['O_N'] = 0
    dis_gdf['O_N']=0

    for item in PointList:
        dis_gdf.loc[dis_gdf['O_id']==item.ID,'O_N']=item.weight2
        dis_gdf.loc[dis_gdf['D_id']==item.ID,'D_N']=item.weight2

    # od_df=pd.read_csv(pathod)
    # od_df=od_df.set_index(keys=['O_id','D_id'],drop=False)
    # dis_gdf=dis_gdf.set_index(keys=['O','D'])
    # od_df['dis']=0
    # od_df['dis']=dis_gdf['dis']
    #
    # od_df=od_df.dropna(axis=0)
    ##del the chongfu data

    Envir.dis_dict=dis_func2_1(dis_gdf,PointList)
    simulate_time=200
    people_num=3000
    temp_routeList=[]
    flag=0

    time1=time.localtime()
    getmon=str(time1.tm_mon)
    getday=str(time1.tm_mday)
    gethour=str(time1.tm_hour)
    temp_path='D:\\modelSSh'+str(gama)+'_'+str(people_num)+"_"+getmon+getday+gethour
    for i in range(0,people_num):
    #model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
        model=agent2.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,environment=Envir)
        model.simulate_home_repeat1()
        mid=model.data_mid
        mid.person_tag = i
        write = IO.IO(mid)
        write.write_txt(temp_path+'+.txt', i)
        print (time.localtime())
        if(flag%100==0):
            print (flag)
        flag+=1
    print (00)
    return temp_path