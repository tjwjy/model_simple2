import IO
import pandas as pd
import Cal
import math
import numpy as np
import geopandas as gpd
from  shapely.geometry import Polygon,Point

#
def str2shape(row):
    str=row
    coor_str=str.replace('(',')').split(')')[2]
    coor_str=coor_str.replace(', ',',')
    coorlist=coor_str.split(',')
    valuelist=[]
    for item in coorlist:
        if(item):
            temp=item.split(' ')
            valuelist.append((float(temp[0]),float(temp[1])))
    return Polygon(valuelist)

##__updatae dis of the dataframe
##__you can change crs using shaply that you can cal any distance
##__make sure you have index the dataframe
def Update_dis(indexed_df):
    df=indexed_df
    df['O_geometry']=df['O_geometry'].apply(str2shape)
    df['D_geometry']=df['D_geometry'].apply(str2shape)

    gdf=gpd.GeoDataFrame(data=df,geometry='O_geometry')
    gdf['O_point']=gdf.centroid

    gdf=gpd.GeoDataFrame(data=df,geometry='D_geometry')
    gdf['D_point']=gdf.centroid

    valuelist=[]
    for index,row in gdf.iterrows():
        dis=row['O_point'].distance(row['D_point'])
        valuelist.append([int(row['O_id']),int(row['D_id']),dis])
    temp_dataframe=pd.DataFrame(data=valuelist,columns=['O_id','D_id','Dis'])
    temp_dataframe=temp_dataframe.set_index(keys=['O_id','D_id'])
    df['Dis']=temp_dataframe['Dis']
    return df

def cal_od_dic(dict,noReapeatPoint):
    for i in range(0,len(noReapeatPoint)-1):
        point1=noReapeatPoint[i]
        point2=noReapeatPoint[i+1]
        temp_tuple=(point1.ID,point2.ID)
        if(temp_tuple in dict.keys()):
            dict[temp_tuple]+=1
        else:
            dict[temp_tuple]=1
    return dict
def cal_od_dict24(dict,noReapeatPoint):
    for i in range(0,len(noReapeatPoint)-1):
        point1=noReapeatPoint[i]
        point2=noReapeatPoint[i+1]
        temp_tuple=(point1.ID,point2.ID)
        if(temp_tuple in dict.keys()):
            t=int(point1.t)%24
            dict[temp_tuple][t]+=1
        else:
            dict[temp_tuple]=np.zeros(24)
            t = int(point1.t) % 24
            dict[temp_tuple][t] += 1
    return dict
##__there are missing od in raw data
##__we can only cal all od from Envir
def get_allod_fromEnvir(Envir):
    pointlist=Envir.PointList
    dis_dict=Envir.dis_dict
    if(not dis_dict):
        dis_dict=Envir.cal_dis_dict()
    valuelist=[]
    for item in pointlist:
        for item2 in pointlist:
            if(item.ID!=item2.ID):
                temp_list=[item.ID,item2.ID,item.weight2,item2.weight2,dis_dict[(item.ID,item2.ID)]]
                valuelist.append(temp_list)
    df=pd.DataFrame(data=valuelist,columns=['O_id','D_id','O_N','D_N','Dis'])
    return df

def read_txt_tocsv(path,csv_path):

    csv_df=pd.read_csv(csv_path)
    csv_df=csv_df.set_index(keys=['O_id','D_id'],drop=False)
    # csv_df=Update_dis(csv_df)

    read=IO.IO()
    Envir,offset=read.read_Envr(path=path)

    ##__cal the all num between ods
    data_mid,offset=read.read_txt_step(path=path,offset=offset,temp_envir=Envir)
    flag=0
    OD_dict={}
    while (data_mid):
        cal=Cal.Cal_agent(data_mid.route,Envir)
        PointList=cal.del_norepeat_PointList()
        OD_dict=cal_od_dic(OD_dict,PointList)
        data_mid, offset = read.read_txt_step(path=path, offset=offset, temp_envir=Envir)
        flag+=1
        if(flag%100==0):
            print ('cal people num is'+str(flag))

    ## store them to the dataframe
    valuelist=[]
    for item in OD_dict.items():
        keys = list(item[0])
        value = item[1]
        keys.append(value)
        valuelist.append(keys)
    df=pd.DataFrame(data=valuelist,columns=['O_id','D_id','value'])
    df=df.set_index(keys=['O_id','D_id'])

    # ##__store dis to dataframe
    ##__the distance cal is delete because Environment distance is not the real distance but the S distance
    # dis_value=[]
    # for item in Envir.dis_dict.items():
    #     keys = list(item[0])
    #     value = item[1]
    #     keys.append(value)
    #     dis_value.append(keys)
    # dis_gdf = pd.DataFrame(data=dis_value, columns=['O_id', 'D_id', 'Dis'])
    # dis_gdf=dis_gdf.set_index(keys=['O_id','D_id'])

    ##__join the table and store
    allod=get_allod_fromEnvir(Envir)
    allod=allod.set_index(keys=['O_id','D_id'])
    allod['model_value']=df['value']
    allod['flux']=csv_df['flux']
    allod=allod.fillna(0)
    # csv_df['model_value']=0
    # csv_df['model_value']=df['value']
    # csv_df=csv_df.fillna(0)
    # scale2=math.log(csv_df['flux'].mean()/csv_df['model_value'].mean())
    scale=allod['flux'].sum()/allod['model_value'].sum()
    print ('scale is '+str(scale))
    allod['model_value_scale']=allod['model_value']*scale
    allod.to_csv(path+'.csv')

    print ('OK')
def read_txt_tocsv24(path,csv_path):

    csv_df=pd.read_csv(csv_path)
    csv_df=csv_df.set_index(keys=['O_id','D_id'],drop=False)
    # csv_df=Update_dis(csv_df)

    read=IO.IO()
    Envir,offset=read.read_Envr(path=path)

    ##__cal the all num between ods
    data_mid,offset=read.read_txt_step(path=path,offset=offset,temp_envir=Envir)
    flag=0
    OD_dict={}
    while (data_mid):
        cal=Cal.Cal_agent(data_mid.route,Envir)
        PointList=cal.del_norepeat_PointList()
        OD_dict=cal_od_dict24(OD_dict,PointList)
        data_mid, offset = read.read_txt_step(path=path, offset=offset, temp_envir=Envir)
        flag+=1
        if(flag%100==0):
            print ('cal people num is'+str(flag))

    ## store them to the dataframe
    valuelist=[]
    for item in OD_dict.items():
        keys = list(item[0])
        value = item[1]
        keys.extend(value)
        valuelist.append(keys)
    time=range(0,24)
    columnsnames=[str(item) for item in time]
    columnsnames2=['O_id', 'D_id']
    columnsnames2.extend(columnsnames)
    df=pd.DataFrame(data=valuelist,columns=columnsnames2)
    df=df.set_index(keys=['O_id','D_id'])
    df.to_csv(path+'24'+'.csv')
    print ('OK')
read_txt_tocsv(path=r'D:\modelSSh1_3000_31719+.txt',csv_path='E:\\data\\taxidata\\shanghai.csv')