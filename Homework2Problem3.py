# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 22:24:44 2021

@author: cuav
"""


import numpy as np
import matplotlib as plt

x = np.arange(0,10.5,0.5)
y = np.arange(0,10.5,0.5)

class node:
    def __init__(self,x,y,cost,parent_index,index):
        self.x = x
        self.y = y
        self.cost = cost 
        self.parent_index = parent_index
        self.index = index

a = 0
b = a
c = 0
d = 0

#Number of nodes per unit distance
n = 2

M = np.zeros((len(y),len(x)))

while a < len(y):
    while b < len(x):
        M[a,b] = b + n*a*(max(x))+a
        b += 1
    a += 1
    b = 0
    if a >= len(x):
        a = len(y)+1


Unvisit = dict()
Visit = dict()
Obstacles = (([1,1],[4,4],[3,4],[5,0],[5,1],[1,7],[2,7],[3,7]))

def distance(temp,current):
    z = np.sqrt((current.x-temp.x)**2+(current.y-temp.y)**2)
    print(z)
    return z
def inflation(temp,Obstacle):
    z = np.sqrt((temp.x-Obstacle[0])**2+(temp.y-Obstacle[1])**2)
    return z
def calc_index(node,xmax,ymax,xmin,ymin,grid_size):
    return((node.y - ymin)/grid_size * (xmax-xmin)/grid_size + (node.x-xmin)/grid_size)

def collision_check(current_location):
    if [current_location.x,current_location.y] in Obstacles:
        return False
    elif current_location.index in Visit:
        return False
    elif current_location.x < 0.5 or current_location.x > 9.5:
        return False
    elif current_location.y < 0.5 or current_location.y > 9.5:
        return False
    else:
        for i in range(len(Obstacles)):
            if inflation(temp,Obstacles[i]) < 1:
                return False
        return True


dd = 0
#Zip function
N = M.astype('int')
N = np.transpose(N.astype('str'))


goal_node = node(8,9,1,0,394)
current_node = node(2,2,0,-1,0)
calc_index(current_node,10.5,10.5,0,0,0.5)

Unvisit[current_node.index] = current_node

current_index = min(Unvisit, key = lambda x: Unvisit[x].cost)

current = Unvisit[current_index]

while current.index != goal_node.index:
    current_index = min(Unvisit, key = lambda x: Unvisit[x].cost)
    current = Unvisit[current_index]
    Visit[current_index] = current
    
    del Unvisit[current_index]
    
    for i in range(-1,2):
        for j in range(-1,2):
            ii = i/2
            jj = j/2
            temp = node(current.x+ii,current.y+jj,10000000,0,0)
            temp.index = calc_index(temp,10.5,10.5,0,0,0.5)
            temp.cost = current.cost + distance(temp,current)
            temp.parent_index = current.index
            if collision_check(temp) is False:
                continue
            if temp.index == current_index:
                continue
            if temp.index in Unvisit:
                if temp.cost <= Unvisit[temp.index].cost:
                    Unvisit[temp.index] = temp
            else:
                Unvisit[temp.index] = temp
    
    
goal = current
path = [goal.index]
pathx = []
pathy = []
while current.parent_index != -1:
    goal = current
    path.append(current.parent_index)
    pathx.append(current.x)
    pathy.append(current.y)
    current = Visit[goal.parent_index]


while c < 21:
    while d < 21:    
        plt.pyplot.xlim([0,10.5])
        plt.pyplot.ylim([0,10.5])
        plt.pyplot.text(x[d],y[c],N[d,c],color="red",fontsize=8)
        d += 1
    d = 0
    c += 1

while dd < len(Obstacles):
    plt.pyplot.xlim([-0.2,10.5])
    plt.pyplot.ylim([-0.2,10.5])
    obs = Obstacles[dd]
    plt.pyplot.text(obs[0],obs[1],obs[1]*len(y)*n+obs[0]*n,color="green",fontsize=8)
    dd += 1

    
plt.pyplot.plot(pathx,pathy)