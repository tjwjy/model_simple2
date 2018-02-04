import random
import Point
import math
class Envronment():
    def __init__(self,Point_List,dimension_x,dimmension_y=0):

        self.PointList=Point_List
        self.grid = Point.Grid(self.PointList,dimension_x, dimmension_y)
        self.grid.set_grid(self.PointList)
        self.dis_dict = {}
        # self.cal_dis_dict(dis_function=self.dis_func1)
        # to store the distance all poins
        #  the key is (id1,id2), and id1<=id2
    #deep copy
    def copy_environment(self,Envir):
        self.grid=Envir.grid
        self.PointList=Envir.PointList
        self.dis_dict=Envir.dis_dict
        # self.cal_dis_dict(dis_function=self.dis_func1)


    def add_Point(self,pointList):
        if(pointList):
            self.PointList.extend(pointList)
            self.grid.set_grid(self.PointList)

    # add a function to cal the dis matrix
    def cal_dis_dict(self,dis_function):
        for point in self.PointList:
            for point2 in self.PointList:
                if(point.ID!=point2.ID):
                    temp_dis=dis_function(point,point2)
                    self.dis_dict[(point.ID,point2.ID)]=temp_dis
    def find_distance(self,id1,id2):
        if((id1,id2) in self.dis_dict.keys()):
            return self.dis_dict[(id1,id2)]
        else:
            return pow(10,10)
    def dis_func1(self,Point1, Point2):
        r2 = (Point1.x - Point2.x) * (Point1.x - Point2.x) + (Point1.y - Point2.y) * (Point1.y - Point2.y)
        return math.sqrt(r2)

