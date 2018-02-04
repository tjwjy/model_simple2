import pandas as pd
import numpy as np
import Cal
import IO
import matplotlib.pyplot as plt
import heapq
import test_agentR
import Environment
import time
import agent2


def simulate4n(path='E:\\data\\taxidata\\shanghai\\20140301grid.csv', pathod='E:\\data\\taxidata\\shanghai.csv'):
    ##the disput of population
    args_model = [0.6, -0.1]
    args_time = [2, 1]
    args_steps = [1.31]
    gama = 1
    path = path
    pathod = pathod
    PointList = test_agentR.get_point_from_geodf(path, gama=gama)
    Envir = Environment.Envronment(PointList, 10, 10)
    Envir.cal_dis_dict(dis_function=test_agentR.dis_func1)
    temp_value = []
    for item in Envir.dis_dict.items():
        keys = list(item[0])
        value = item[1]
        keys.append(value)
        temp_value.append(keys)

    dis_gdf = pd.DataFrame(data=temp_value, columns=['O_id', 'D_id', 'dis'])

    Envir.dis_dict = test_agentR.dis_func3(dis_gdf)
    simulate_time = 720
    people_num = 10
    MidList = []
    for i in range(0,people_num):
    #model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
        model=agent2.Nomal_Individual(args_model=args_model,args_t=args_time,args_step=args_steps,simulate_time=simulate_time,environment=Envir)
        model.simulate_home_repeat1()
        mid=model.data_mid
        mid.Envir=Envir
        mid.person_tag = i
        MidList.append(mid)
        print(i)
        print (time.localtime())
    return MidList
def get_visited_frequency(MidList):

    Pointlist=[]
    for data_mid in MidList:
        cal=Cal.Cal_agent(data_mid.route,data_mid.Envir)
        # temp_PointList = cal.del_norepeat_PointList()
        temp_PointList=data_mid.route
        Pointlist.append(temp_PointList)
    temp=[]
    for index,item in enumerate(Pointlist):
        rankvalue=cal.get_visitfrequency_points(item)
        rankvalue=np.array(rankvalue)
        if(len(rankvalue)>20):
            temp.append(rankvalue[0:20])
    temp=np.array(temp).mean(axis=0)
    ax=plt.scatter(range(1,21),temp/temp.sum(),c='r',zorder=0)

    def cal_len(x):
        str_list = str(x).split(';')
        return len(str_list)

    point_path = 'E:\\data\\shenzhen_deal_mid\\shenzhen.csv'
    df = pd.read_csv(point_path)
    df['len'] = df['t'].apply(cal_len)
    grouped = df['t'].groupby(df['id'])
    df_grouped = grouped.count()
    df_array = df_grouped.values
    max_value = heapq.nlargest(10, df_array)[2:-1]
    indexlist = []
    for item in max_value:
        max_grouped = df_grouped[df_grouped == item]
        index = max_grouped.index.values
        indexlist.extend(index)
    temp = []
    for index, item in enumerate(indexlist):
        temp_df = df[df['id'] == item]
        lenlist = temp_df['len'].values
        lenlist.sort()
        if (len(lenlist) - 20 > 0):
            temp.append(np.array(lenlist[0:20]))
    temp = np.array(temp)
    temp = temp.mean(axis=0)
    plt.scatter(range(len(temp), 0, -1), temp / temp.sum(), c='y', s=50)

    plt.xscale('log')
    plt.yscale('log')
    plt.legend()

    plt.ylim(0.001,1)
    plt.xlim(.9,30)
    plt.show()

Midlist=simulate4n()
get_visited_frequency(Midlist)