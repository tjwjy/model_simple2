import math
class Point():
    def __init__(self,x,y,gridid,ID,state=0,weight=1):
        self.x=x
        self.y=y
        self.gridID=gridid
        self.ID=ID
        self.state=state
        self.weight=weight
        self.t=0
        self.weight2=0

class Grid():
    def __init__(self,Point_List,dimension_x,dimension_y=0):
        self.PointList=Point_List
        self.dimension_x=dimension_x

        if(dimension_y==0):
            self.dimension_y=dimension_x
        else:
            self.dimension_y=dimension_y
        temp_xlist = []
        temp_ylist = []
        if(Point_List):
            for point in Point_List:
                temp_xlist.append(point.x)
                temp_ylist.append(point.y)
        else:
            temp_xlist=[0,100]
            temp_ylist=[0,100]
        self.Left_Point=[min(temp_xlist), min(temp_ylist)]
        self.Right_Point=[max(temp_xlist), max(temp_ylist)]
        self.dis_x=(-self.Left_Point[0]+self.Right_Point[0])/self.dimension_x
        self.dis_y=(-self.Left_Point[1]+self.Right_Point[1])/self.dimension_y
        self.grid_dict={}
    # update the point to id list
    def set_grid(self,PointList):
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                self.grid_dict[(int(i),int(j))]=[]
        for point in PointList:
            tempi=int(math.floor((point.x-self.Left_Point[0])/self.dis_x))
            tempj=int(math.floor((point.y-self.Left_Point[1])/self.dis_y))
            # if(tempi<=self.dimension_x and tempi>=0):
            #     if(tempj<=self.dimension_y and tempj>=0):
            if(tempi==self.dimension_x):
                tempi-=1
            if(tempj==self.dimension_y):
                tempj-=1
            self.grid_dict[(tempi,tempj)].append(point)
            #self.grid_dict[(tempi, tempj)]=1
            point.gridID=(tempi,tempj)

# select the grid in the rectangle out side circle
    def get_PointsByGrid(self,org_grid,r):
        temp_answer=[]
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                if(self.grid_dict[(i,j)]):
                    if(i-org_grid[0]<r and j - org_grid[1]<r):
                        temp_list=self.grid_dict([i,j])
                        temp_answer.extend(temp_list)
        return temp_answer

