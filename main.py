# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:10:56 2020

@author: boucher
"""


#cd Documents/LCBOB/Physarum_Transport_Network

from class_free import *


# (self, liste_agent,trail_map,SA,RA,SO,SW,depT,decayT)
L = 200  
l = 50
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
n = 100
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
b = time.time()
print(b-a,' sec')
######################################### ANIMATION V2  #########################################

scale = np.max(data[0])
data_rgb = np.array([[[ [k,k,k] for k in j]for j in i] for i in data])
from array2gif import write_gif
write_gif(data_rgb, 'rgbbgr.gif', fps=30)


######################################### ANIMATION #########################################

"""
import matplotlib.animation as animation


fig = plt.figure(figsize=[0.5,0.5],dpi=500,frameon="False",)

#remove axis and tetc
fig.subplots_adjust(0,0,1,1)
plt.axis("off")

plot = plt.imshow(data[0],cmap=plt.cm.bone)

def init():
    plot.set_data(data[0])
    return(plot)

def update(j):
    plot.set_data(data[j])
    return(plot)


anim = animation.FuncAnimation(fig, update, init_func = init, frames=n, interval = 30)
b = time.time()
print(b-a,' sec')

#Writer = animation.writers['imagemagick']
#writer = Writer(fps=24, metadata=dict(artist='Me'), bitrate=3600)
anim.save('lines.gif', writer='imagemagick')
"""