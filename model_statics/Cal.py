import numpy as np
import math
import Environment
class Cal_agent():
    def __init__(self,PointList,Envir):
        self.PointList=PointList
        self.Envir=Environment.Envronment([],10)
        self.Envir.copy_environment(Envir)
    #agent may stay at a position for many simulate time
    #we will del the position repeat
    #get the no repeat pointList as return
    def del_norepeat_PointList(self):
        temp_PointList=[]
        last_id=-1
        for point in self.PointList:
            if(last_id !=point.ID):
                temp_PointList.append(point)
                last_id=point.ID
        return temp_PointList

    def get_visitfrequency_points(self,norepeat_PointList):
        idlist=[]
        for point in norepeat_PointList:
            idlist.append(point.ID)
        id_array=np.array(idlist)
        id_array2=np.bincount(id_array)
        idlist2=id_array2.tolist()
        idlist3=sorted(idlist2,reverse=True)
        return idlist3

    def change_data2powerlaw_format(self,sorted_idlist):
        powerlaw_list=[]
        for i,item in enumerate(sorted_idlist):
            for j in range(int(item)):
                powerlaw_list.append(i+1)
        return powerlaw_list

    def get_step_dis_point(self,norepeat_PointList):
        disList=[]
        lastpoint=0
        for point in norepeat_PointList:
            if(lastpoint):
                tempi=min(point.ID,lastpoint.ID)
                tempj=max(point.ID,lastpoint.ID)
                dis=self.Envir.dis_dict[(tempi,tempj)]
                disList.append(dis)
            lastpoint=point
        return disList

    def get_Rog(self,norepeat_PointList):
        locationlist=norepeat_PointList
        list2=np.unique(locationlist)
        x=0
        y=0
        for location in locationlist:
            x+=location.x
            y+=location.y
        x=x/len(locationlist)
        y=y/len(locationlist)
        x2=0
        y2=0
        for location in locationlist:
            x2+=(location.x-x)*(location.x-x)
            y2+=(location.y-y)*(location.y-y)
        r=math.sqrt((x2+y2)/(len(locationlist)))
        return r
    def cal_OD(self,point1,point2,PointList):
        # if(point1 not in self.Envir.PointList):
        #     raise Exception("The OD have points not in Environment")
        # if(point2 not in self.Envir.PointList):
        #     raise Exception ("The OD have points not in Environment")
        ODlist=[]
        for i in range(len(PointList)-1):
            if(point1==PointList[i].ID):
                if(PointList[i+1].ID==point2):
                    ODlist.append([PointList[i],PointList[i+1]])
        return ODlist
    def cal_OD_24hours_disput(self,ODlist):
        if ODlist:
            t_list=[0]*25
            for OD in ODlist:
                t=OD[0].t
                t_int=int(t)
                t_list[t_int]+=1
            return t_list
        else:
            raise Exception("there is no t_list")




