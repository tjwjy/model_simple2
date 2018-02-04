import move_rules
import Point
import data_mid
import Environment
import math
import time
args_model=[0.6,-0.21]
args_time=[2,1]
args_steps=[0.84]
gama=1
Pointnum=50
def dis_func1(Point1,Point2):
    r2=(Point1.x-Point2.x)*(Point1.x-Point2.x)+(Point1.y-Point2.y)*(Point1.y-Point2.y)
    return math.sqrt(r2)
PointList=[]
for i in range(50):
    for j in range(50):
        point=Point.Point(i,j,gridid=0,ID=0)
        PointList.append(point)
Envir=Environment.Envronment(PointList,10,10)
Envir.cal_dis_dict(dis_function=dis_func1)
simulate_time=200
people_num=10000
temp_routeList=[]
flag=0

time1=time.localtime()
getmon=str(time1.tm_mon)
getday=str(time1.tm_mday)
gethour=str(time1.tm_hour)
temp_path='D:\\modeldis'+str(gama)+'_'+str(people_num)+"_"+getmon+getday+gethour
for i in range(0,people_num):
#model=Model5.HomeOrWork_Model(args_model=args_model,args_t=args_time,args_steps=args_steps,environment=Envir,visited_Place=[],homeposition=random.choice(Envir.locations),workposition=random.choice(Envir.locations))
    move_rules=move_rules.HomeOrWork_Model_repeat(args_model=args_model,environment=Envir,homeposition=Point.Point(0,0,0,0),workposition=Point.Point(0,0,0,0),visited_Place=[])
    model.simulate_repeat_add1()
    mid=model.data_mid
    mid.person_tag = i
    write = IO.IO(mid)
    write.write_txt(temp_path+'+.txt', i)
    print (time.localtime())
    if(flag%100==0):
        print (flag)
    flag+=1
print (00)
