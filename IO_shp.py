from arcpy import env
import arcpy
class IO():
    def read_shp(self,path,name,fied_list=[]):
        env.workspace=path
        fiedlist=fied_list
        fiedlist.append("SHAPE@XY")
        answer_list=[]
        with arcpy.da.SearchCursor(name,fiedlist)as curse:
            for row in curse:
                temp_list=[]
                for item in row:
                    temp_list.append(item)
                answer_list.append(temp_list)
        return answer_list
    def __init__(self,mid=None):
        self.mid=mid