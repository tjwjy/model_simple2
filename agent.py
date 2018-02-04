import move_rules
import Environment
import data_mid
import numpy as np
import Point
import random
import math
class Individual():
    def __init__(self):
        # attributes
        self.home_loc = 0
        self.work_loc = 0
        # location of family and work.
        self.Envir=[]
        # model coorditions
        self.work_time = []
        self.rest_time = []
        # set the time to work[start,end] and sleep[start,end]
        self.args_time = [-1.55, 1, 17, 10000]
        # set powerlaw disput time.beta=-1.55,time is between [0,17],simulate time is 10000
        self.args_steps = [-1.80, 5]
        # set steplegth ,beta and up limit
        # grid dimension,grid_args(powerlaw contains [beta,min,max],normal contains [xmean,xsigma,ymean,ysigema]),number of point
        self.simulate_time = 10000
        # simulate times=10000
        self.home_locationList = []
        self.work_locatonList = []
        self.commute_LocationList = []
        # the place the person has visit
        self.data_mid=[]
        self.speed=30000

        # function

    def set_grid(self):
        pass

    def set_home_loc(self):
        pass

    def set_work_loc(self):
        pass

    def set_work_time(self):
        pass

    def set_rest_time(self):
        pass

    def set_args(self, args_model, args_step, args_t, simulate_time):
        self.args_model = args_model
        self.args_step = args_step
        self.args_t = args_t
        self.simulate_time = simulate_time

    def simulate(self):
        pass

    def set_time(self, time):
        self.time += time
        self.time24 = time % 24
        print(self.time24)


class Nomal_Individual(Individual):
    #create the model location disput nomal
    #peole select home and work randomly base on the position density
    def set_home_loc(self):
        self.home_loc=random.choice(self.Envir.PointList)
        if(self.Envir.PointList):
            weight=[]
            weight_sum=0
            for point in self.Envir.PointList:
                weight_sum+=point.weight2
                weight.append([point,weight_sum])
            p_random=random.uniform(0,weight_sum)
            for item in weight:
                if(p_random<=item[1]):
                    self.home_loc=item[0]
                    break
        else:
            print ('you should set pointlist')
    def set_work_loc(self,beta):
        # self.work_loc = random.choice(self.Envir.PointList)
        weight = []
        weight_sum = 0
        if(self.home_loc):
            for p in self.Envir.PointList:
                i=self.home_loc.ID
                j=p.ID
                if(i-j):
                    dis=self.Envir.find_distance(i,j)
                    temp_weight=float(p.weight2)/math.pow(dis,beta)
                    weight_sum=weight_sum+temp_weight
                    weight.append([weight_sum,p])
            p_random = random.uniform(0, weight_sum)
            for item in weight:
                if (p_random <= item[0]):
                    self.work_loc = item[1]
                    break
        else:
            print ('you should set home_loc to environment')

    def set_work_time(self):
        start=random.normalvariate(7.5,.5)
        end=random.normalvariate(17.5,1)
        self.work_time=[start,end]
    def set_rest_time(self):
        start = random.normalvariate(22, 1)
        end = random.normalvariate(6.5, .5)
        self.rest_time = [start, end]

    def __init__(self,args_model, args_step, args_t, simulate_time,environment):
        self.speed=30000
        self.Envir=Environment.Envronment([],1)
        self.Envir.copy_environment(environment)
        if(not environment.dis_dict):
            self.Envir.cal_dis_dict(self.Envir.dis_func1)
        self.set_args(args_model, args_step, args_t, simulate_time)
        self.data_mid=data_mid.data_mid(environment,person_tag=0)
        self.set_home_loc()
        self.set_work_loc(beta=args_step[0])
        self.home_locationList =[]
        self.work_locatonList = []
        self.commute_LocationList = []
        for i in range(1):
            self.home_locationList.append(self.home_loc)
            self.work_locatonList.append(self.work_loc)
            self.data_mid.add_location([self.home_loc,self.work_loc])
            self.data_mid.important_loc=[self.home_loc,self.work_loc]


    def simulate(self):
        print ([self.home_loc.x,self.home_loc.y])
        print ([self.work_loc.x,self.work_loc.y])
        simulate_time=0
        while(simulate_time<self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if(t_now<self.work_time[0]and t_now>=self.rest_time[1]):
                #pass
                temp_Model=move_rules.Commute_Model(self.args_model,environment=self.Envir,homeposition=self.home_loc,workposition=self.work_loc,visited_Place=self.commute_LocationList)
                temp_Model.set_t_constraint(t_now=t_now,t_end=self.work_time[0],args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed,self.args_step)
                self.commute_LocationList,tempRoute=temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now=temp_Model.t_now
                #do things commute
                #parameter is t_now and work_time[0]
            if(t_now>self.work_time[0] and t_now<self.work_time[1]):
                #pass
                temp_Model =move_rules.HomeOrWork_Model(self.args_model,self.Envir,self.home_loc,self.work_loc,self.work_locatonList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[1],args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.work_locatonList,tempRoute = temp_Model.get_route(self.work_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                #do something around work
            if(t_now>self.work_time[1] and t_now<self.rest_time[0]):
                #pass
                while(t_now<self.rest_time[0]):
                    temp=random.random()
                    if(temp<0.9):
                        break
                    temp_Model = move_rules.Commute_Model(self.args_model,self.Envir,self.home_loc,self.work_loc,self.commute_LocationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=t_now+0.1,args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.commute_LocationList,tempRoute = temp_Model.get_route(self.work_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                while(t_now<self.rest_time[0]):
                    temp_Model = move_rules.HomeOrWork_Model(self.args_model,self.Envir,self.home_loc,self.work_loc,self.home_locationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0],args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.home_locationList,tempRoute=temp_Model.get_route(self.home_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                #do things commute and then do things around home
            if(t_now>self.rest_time[0] or t_now<self.rest_time[1]):
                t_now=self.rest_time[1]
                simulate_time+=1
                #print (simulate_time)
                #sleep

    def simulate_home(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        while (simulate_time < self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now):
                # pass
                temp_Model = move_rules.HomeOrWork_Model(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.home_locationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.home_locationList, tempRoute = temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                simulate_time+=1
                # do something around work


    def simulate_home_repeat(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        while (simulate_time < self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now):
                # pass
                temp_Model = move_rules.HomeOrWork_Model_repeat(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.home_locationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.home_locationList, tempRoute = temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                simulate_time += 1
                # do something around work

    def simulate_repeat(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        while (simulate_time < self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now < self.work_time[0] and t_now >= self.rest_time[1]):
                # pass
                temp_Model = move_rules.Commute_Model_repeat(self.args_model, environment=self.Envir,
                                                      homeposition=self.home_loc, workposition=self.work_loc,
                                                      visited_Place=self.commute_LocationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.commute_LocationList, tempRoute = temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do things commute
                # parameter is t_now and work_time[0]
            if (t_now > self.work_time[0] and t_now < self.work_time[1]):
                # pass
                temp_Model = move_rules.HomeOrWork_Model_repeat(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.work_locatonList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[1], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.work_locatonList, tempRoute = temp_Model.get_route(self.work_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do something around work
            if (t_now > self.work_time[1] and t_now < self.rest_time[0]):
                # pass
                while (t_now < self.rest_time[0]):
                    temp = random.random()
                    if (temp < 0.9):
                        break
                    temp_Model = move_rules.Commute_Model_repeat(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                          self.commute_LocationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=t_now + 0.1, args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.commute_LocationList, tempRoute = temp_Model.get_route(self.work_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                while (t_now < self.rest_time[0]):
                    temp_Model = move_rules.HomeOrWork_Model_repeat(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                             self.home_locationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.home_locationList, tempRoute = temp_Model.get_route(self.home_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                    # do things commute and then do things around home
            if (t_now > self.rest_time[0] or t_now < self.rest_time[1]):
                t_now = self.rest_time[1]
                simulate_time += 1
                # print (simulate_time)


    def simulate_repeat2(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        while (simulate_time < self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now < self.work_time[0] and t_now >= self.rest_time[1]):
                # pass
                temp_Model = move_rules.Commute_Model_repeat2(self.args_model, environment=self.Envir,
                                                      homeposition=self.home_loc, workposition=self.work_loc,
                                                      visited_Place=self.commute_LocationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.commute_LocationList, tempRoute = temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do things commute
                # parameter is t_now and work_time[0]
            if (t_now > self.work_time[0] and t_now < self.work_time[1]):
                # pass
                temp_Model = move_rules.HomeOrWork_Model_repeat2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.work_locatonList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[1], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.work_locatonList, tempRoute = temp_Model.get_route(self.work_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do something around work
            if (t_now > self.work_time[1] and t_now < self.rest_time[0]):
                # pass
                while (t_now < self.rest_time[0]):
                    temp = random.random()
                    if (temp < 0.9):
                        break
                    temp_Model = move_rules.Commute_Model_repeat2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                          self.commute_LocationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=t_now + 0.1, args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.commute_LocationList, tempRoute = temp_Model.get_route(self.work_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                while (t_now < self.rest_time[0]):
                    temp_Model = move_rules.HomeOrWork_Model_repeat2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                             self.home_locationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.home_locationList, tempRoute = temp_Model.get_route(self.home_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                    # do things commute and then do things around home
            if (t_now > self.rest_time[0] or t_now < self.rest_time[1]):
                t_now = self.rest_time[1]
                simulate_time += 1
                # print (simulate_time)


    def simulate2(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        while (simulate_time < self.simulate_time):
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now < self.work_time[0] and t_now >= self.rest_time[1]):
                # pass
                temp_Model = move_rules.Commute_Model2(self.args_model, environment=self.Envir,
                                                      homeposition=self.home_loc, workposition=self.work_loc,
                                                      visited_Place=self.commute_LocationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.commute_LocationList, tempRoute = temp_Model.get_route(self.home_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do things commute
                # parameter is t_now and work_time[0]
            if (t_now > self.work_time[0] and t_now < self.work_time[1]):
                # pass
                temp_Model = move_rules.HomeOrWork_Model2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.work_locatonList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[1], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.work_locatonList, tempRoute = temp_Model.get_route(self.work_loc)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do something around work
            if (t_now > self.work_time[1] and t_now < self.rest_time[0]):
                # pass
                while (t_now < self.rest_time[0]):
                    temp = random.random()
                    if (temp < 0.9):
                        break
                    temp_Model = move_rules.Commute_Model2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                          self.commute_LocationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=t_now + 0.1, args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.commute_LocationList, tempRoute = temp_Model.get_route(self.work_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                while (t_now < self.rest_time[0]):
                    temp_Model = move_rules.HomeOrWork_Model2(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                             self.home_locationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.home_locationList, tempRoute = temp_Model.get_route(self.home_loc)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                    # do things commute and then do things around home
            if (t_now > self.rest_time[0] or t_now < self.rest_time[1]):
                t_now = self.rest_time[1]
                simulate_time += 1
                # print (simulate_time)

    def simulate_repeat_add1(self):
        print ([self.home_loc.x, self.home_loc.y])
        print ([self.work_loc.x, self.work_loc.y])
        simulate_time = 0
        S=0
        while (simulate_time < self.simulate_time):
            # S=set(self.commute_LocationList.extend(self.home_locationList.extend(self.work_locatonList)))
            self.set_work_time()
            self.set_rest_time()
            t_now = self.rest_time[1]
            if (t_now < self.work_time[0] and t_now >= self.rest_time[1]):
                # pass
                temp_Model = move_rules.Commute_Model_repeat_add1(self.args_model, environment=self.Envir,
                                                      homeposition=self.home_loc, workposition=self.work_loc,
                                                      visited_Place=self.commute_LocationList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[0], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.commute_LocationList, tempRoute,S = temp_Model.get_route(self.home_loc,S)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do things commute
                # parameter is t_now and work_time[0]
            if (t_now > self.work_time[0] and t_now < self.work_time[1]):
                # pass
                temp_Model = move_rules.HomeOrWork_Model_repeat_add1(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                         self.work_locatonList)
                temp_Model.set_t_constraint(t_now=t_now, t_end=self.work_time[1], args_t=self.args_t)
                temp_Model.set_space_constrain(self.speed, self.args_step)
                self.work_locatonList, tempRoute ,S= temp_Model.get_route(self.work_loc,S)
                self.data_mid.add_location(tempRoute.route)
                t_now = temp_Model.t_now
                # do something around work
            if (t_now > self.work_time[1] and t_now < self.rest_time[0]):
                # pass
                while (t_now < self.rest_time[0]):
                    temp = random.random()
                    if (temp < 0.9):
                        break
                    temp_Model = move_rules.Commute_Model_repeat_add1(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                          self.commute_LocationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=t_now + 0.1, args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.commute_LocationList, tempRoute,S = temp_Model.get_route(self.work_loc,S)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                while (t_now < self.rest_time[0]):
                    temp_Model = move_rules.HomeOrWork_Model_repeat_add1(self.args_model, self.Envir, self.home_loc, self.work_loc,
                                                             self.home_locationList)
                    temp_Model.set_t_constraint(t_now=t_now, t_end=self.rest_time[0], args_t=self.args_t)
                    temp_Model.set_space_constrain(self.speed, self.args_step)
                    self.home_locationList, tempRoute ,S= temp_Model.get_route(self.home_loc,S)
                    t_now = temp_Model.t_now
                    self.data_mid.add_location(tempRoute.route)
                    # do things commute and then do things around home
            if (t_now > self.rest_time[0] or t_now < self.rest_time[1]):
                t_now = self.rest_time[1]
                simulate_time += 1
                # print (simulate_time)

