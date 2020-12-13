# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:10:56 2020

@author: boucher
"""

from class_free import *


# (self, liste_agent,trail_map,SA,RA,SO,SW,depT,decayT) 
L = 100
l = 100
 # (self, liste_agent,trail_map,SA,RA,SO,SW,SS,depT,decayT):
trail_map = np.zeros([L+2*l,L+2*l])
s=100
for i in range((L+2*l)//4):
    trail_map[4*i]=s
    trail_map[:,4*i]=s
    
board = data_map([],trail_map,22.5*np.pi/180,np.pi/4,9,1,1,5,0.1)
board.initialise(0.4,L,l)

import time
a = time.time()
n = 10000
data = np.empty(n, dtype=object)

for i in range(n):
    #board.plot_free_place()
#    print(i)
    #board.plot_free_place()
    #board.plot_trail_map()
    
    board.motor_step()
    board.sensory_step()
    #board.trail_map = board.diffusion_mean(0.1,0.1)
    #board.trail_map = board.diffusion_eq(board.trail_map,0.1,0.1)
    board.trail_map = board.decay(board.trail_map,0.9)
    data[i] = board.trail_map
#    m = n//10
#    if float(i//m)==i/m :
#        print(i)
#        board.plot_trail_map()
#        board.plot_free_place()

######################################### ANIMATION #########################################

import matplotlib.animation as animation


fig = plt.figure()
plot = plt.imshow(data[0],cmap=plt.cm.bone)

def init():
    plot.set_data(data[0])
    return plot

def update(j):
    plot.set_data(data[j])
    return [plot]


anim = animation.FuncAnimation(fig, update, init_func = init, frames=n, interval = 30)

plt.show()
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#anim.save('lines.mp4', writer=writer)
b = time.time()
print(b-a,' sec')