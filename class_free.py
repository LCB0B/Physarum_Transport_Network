# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:47:22 2020

@author: boucher
"""
import numpy as np
import random 
import  matplotlib.pyplot as plt 

class agent:
    def __init__(self, x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle 
        
    def get_pos(self):
        return([self.x,self.y])
        
    def try_go_forward(self,SS): # get is forward position
        x1 = self.x + SS*np.cos(self.angle)
        y1 = self.y + SS*np.sin(self.angle)
        return(x1,y1)
    
    def go_forward(self,x,y):
        self.x = x
        self.y = y
        
class data_map:
    def __init__(self, liste_agent,trail_map,SA,RA,SO,SW,SS,depT,decayT):
        self.list_agent = []
        self.trail_map = trail_map
        self.free_place = np.array([])
        self.depT= depT
        self.SA = SA
        self.RA = RA
        self.SO = SO
        self.SW = SW
        self.SS = SS
        self.depT = depT
        self.decayT = decayT
        
    def add_agent(self,agent):
        self.list_agent.append(agent)
        
    def initialise(self,pop,L,l):
        n_agent = int(pop * L**2)
        self.free_place = np.ones([L+2*l,L+2*l])
        if self.trail_map.all() == 0:
            print('ONES')
            #self.trail_map = np.ones([L+2*l,L+2*l])
        for i in range(n_agent):
            x,y,angle = np.array([l,l,0]) + np.array([L*random.random() , L*random.random(), 2*np.pi*random.random()])
            if self.free_place[int(x),int(y)]:
                self.add_agent(agent(x,y,angle))
                self.free_place[int(x),int(y)]=0
    
    def plot_free_place(self):
        #plt.figure()
        plt.matshow(self.free_place,cmap=plt.cm.inferno)
        plt.show()
    
    def plot_trail_map(self):
        #plt.figure()
        plt.matshow(self.trail_map,cmap=plt.cm.gray)
        plt.show()
    
    def motor_step(self):
        #random.shuffle(self.list_agent)
        for ag in self.list_agent :
            x_0,y_0 = ag.get_pos()
            #print('step : '  , x_0,y_0)
            x,y = ag.try_go_forward(self.SS)
            x,y =  np.array([x,y]) % len(self.free_place) # circle board !
            #self.free_place[int(x_0),int(y_0)] = 1
            #self.free_place[int(x),int(y)] = 0
            #print('step2 : '  , [int(x_0),int(y_0)])
            self.trail_map[int(x_0),int(y_0)] = self.trail_map[int(x_0),int(y_0)] + self.depT     
            ag.go_forward(x,y)
           
                

    def get_FL(self,trail_map,SW,SA,SO,angle,x_0,y_0):      
        L = len(trail_map)
        x_FL_1 = (x_0 + SO*np.cos(angle+SA) ) % L
        x_FL_2 = ( x_FL_1 + SW) % L
        y_FL_1 = (y_0 + SO*np.sin(angle+SA) ) % L
        y_FL_2 =  (y_FL_1 + SW ) % L
        
        x_lim = np.sort([x_FL_1, x_FL_2]).astype(int)
        y_lim = np.sort([y_FL_1, y_FL_2]).astype(int)  


        FL = np.mean(trail_map[x_lim[0]:x_lim[1] , y_lim[0]:y_lim[1] ])
        return(FL)
        
    def get_FR(self,trail_map,SW,SA,SO,angle,x_0,y_0):
        L = len(trail_map)
        x_FR_1 = (x_0 + SO*np.cos(angle-SA) ) % L
        x_FR_2 = ( x_FR_1 + SW) % L
        y_FR_1 = (y_0 + SO*np.sin(angle-SA) ) % L
        y_FR_2 =  (y_FR_1 + SW ) % L
        
        x_lim = np.sort([x_FR_1, x_FR_2]).astype(int)
        y_lim = np.sort([y_FR_1, y_FR_2]).astype(int)  

        FR = np.mean(trail_map[x_lim[0]:x_lim[1] , y_lim[0]:y_lim[1] ])
        return(FR)
    
    def get_F(self,trail_map,SW,SA,SO,angle,x_0,y_0):      
        L = len(trail_map)
        x_F_1 = (x_0 + SO*np.cos(angle) ) % L
        x_F_2 = ( x_F_1 + SW) % L
        y_F_1 = (y_0 + SO*np.sin(angle) ) % L
        y_F_2 =  (y_F_1 + SW ) % L
        
        x_lim = np.sort([x_F_1, x_F_2]).astype(int)
        y_lim = np.sort([y_F_1, y_F_2])   .astype(int)  

        F = np.mean(trail_map[x_lim[0]:x_lim[1] , y_lim[0]:y_lim[1] ])
        return(F)
        
    def sensory_step(self):
        #random.shuffle(self.list_agent)
        for ag in self.list_agent :
            x_0,y_0= ag.get_pos()
            FL = self.get_FL(self.trail_map,self.SW,self.SA,self.SO,ag.angle,x_0,y_0)
            FR =  self.get_FR(self.trail_map,self.SW,self.SA,self.SO,ag.angle,x_0,y_0)
            F =  self.get_F(self.trail_map,self.SW,self.SA,self.SO,ag.angle,x_0,y_0)
            if  F>FL and F > FR:
                pass
            elif  F<FL and F < FR:
                ag.angle = random.choice([ag.angle+self.RA, ag.angle-self.RA])

            elif FL < FR :
                #ag.angle = ag.angle-self.RA*(random.random()+1)
                ag.angle = ag.angle-self.RA

            elif FL > FR :
                #ag.angle = ag.angle + self.RA*(random.random()+1)
                ag.angle = ag.angle+self.RA

            else:
                pass
            
    def diffusion_eq(self,trail_map,Dx,Dy):
        L = len(trail_map)
        new_trail_map = np.zeros([L,L])
        for i in range(L):
            for j in range(L):
                new_trail_map[i,j]=Dx*(trail_map[(i+1)%L,j]+trail_map[(i-1)%L,j]) + Dy*(trail_map[i,(j+1)%L]+trail_map[i,(j-1)%L]) + (1-2*Dx-2*Dy)*trail_map[i,j]
        return(np.array(new_trail_map))
        
    def diffusion_mean(self,K,t):
        L = len(self.trail_map)
        new_trail_map = np.zeros([L,L])
        for i in range(L):
            for j in range(L):
                new_trail_map[i,j]=(1-t)*new_trail_map[i,j] + t*np.mean(self.trail_map[(i-K)%L:(i+K)%L,(j-K)%L:(j+K)%L])
        return(np.array(new_trail_map))
        
        
        
    def decay(self,trail_map,decayT):
        new_trail_map = np.array([[ decayT*j for j in i] for i in trail_map])
        return(new_trail_map)
    
    
    
    def border_test(self,x,y,x_0,y_0): # stay where yo uare if go over border
        L = len(self.free_place)
        if x >= L or y>= L:
            r=t
        return()
    
                
                
            

"""

class Student:
    def __init__(self, name, student_number):
        self.name = name
        self.student_number = student_number
        self.classes = []

    def enrol(self, course_running):
        self.classes.append(course_running)
        course_running.add_student(self)


class Department:
    def __init__(self, name, department_code):
        self.name = name
        self.department_code = department_code
        self.courses = {}

    def add_course(self, description, course_code, credits):
        self.courses[course_code] = Course(description, course_code, credits, self)
        return self.courses[course_code]


class Course:
    def __init__(self, description, course_code, credits, department):
        self.description = description
        self.course_code = course_code
        self.credits = credits
        self.department = department
        self.department.add_course(self)

        self.runnings = []

    def add_running(self, year):
        self.runnings.append(CourseRunning(self, year))
        return self.runnings[-1]


class CourseRunning:
    def __init__(self, course, year):
        self.course = course
        self.year = year
        self.students = []

    def add_student(self, student):
        self.students.append(student)


"""