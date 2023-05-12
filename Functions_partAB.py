"""
This file contains all the functions required to run and visualise an implmentation of the Ising Model
using both Glauber and Kawasaki dynamics. These functions are used to run the simulation in 
the run.ising.simulation.py file.

The functions require the existence of the /Data/Glauber and /Data/Kawasaki directories
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

"""

import datetime
import os
import sys
import math
import time
import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


def neighbors(idx, lattice, N):

    i, j = idx
    center = lattice[i,j]

    T = lattice[(i-1)%N, j]
    B = lattice[(i+1)%N, j]
    R = lattice[i, (j+1)%N]
    L = lattice[i, (j-1)%N]

    TR = lattice[(i-1)%N, (j+1)%N]
    BR = lattice[(i+1)%N, (j+1)%N]
    TL = lattice[(i-1)%N, (j-1)%N]
    BL = lattice[(i+1)%N, (j-1)%N]

    num_neighbors = np.array([T, B, R, L, TR, BR, TL, BL])


    R_neighbors = num_neighbors[num_neighbors==1]
    R_neighbors_sum = np.count_nonzero(R_neighbors)

    P_neighbors = num_neighbors[num_neighbors==2]
    P_neighbors_sum = np.count_nonzero(P_neighbors) 

    S_neighbors = num_neighbors[num_neighbors==3]
    S_neighbors_sum = np.count_nonzero(S_neighbors) 

    return R_neighbors_sum, P_neighbors_sum, S_neighbors_sum



def setCondition(N, condition, lattice):

    i, j = int(N/2), int(N/2)

    if (condition=='blinker'):

        lattice[(i+1)%N, j] = 1
        lattice[i,j] = 1
        lattice[(i-1)%N, j] = 1

    elif(condition=='glider'):

        lattice[i,j] = 1
        lattice[i,j+1] = 1
        lattice[i-1,j+2] = 1
        lattice[i-1,j] = 1
        lattice[i-2,j] = 1

    return lattice



def initialise_simulation():

    # checks command line arguments are correct otherwise stops simulation
    if (len(sys.argv) < 2 or len(sys.argv) > 3):
        print("Error Input Usage: python ising.animation.py N -optional [glider/blinker]")
        sys.exit()

    
    N=int(sys.argv[1]) 
    condition = 'Random'

    # if (len(sys.argv) == 3): condition=str(sys.argv[2])

    return N



def update_Game(N, lattice, Run):

    # lattice = setCondition(N, condition, lattice)    
    new_lattice = lattice.copy()



    cmap = ListedColormap([ 'red', 'green', 'dodgerblue'])
    vmin = 1
    vmax = 4

    # setting up animantion figure
    fig = plt.figure()
    im=plt.imshow(new_lattice, animated=True, vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar()

    # number of sweeps for simulation
    nstep=200

    # sweeps counter
    sweeps = 0

    data=open(f'NumberR_States.txt','w')

    R_states = 0

    counter=0
    for n in range(nstep):
        xcm_top = 0
        ycm_top = 0
        for ij in itertools.product(range(N), repeat=2):

            i,j = ij
            cell = lattice[i,j]
            NumR, NumP, NumS = neighbors(ij, lattice, N)

            # 1 = rock
            # 2 = paper
            # 3 = scissors

            # rock to paper
            if (cell == 1):
                if (NumP>2):
                    #changing R to P
                    new_lattice[i,j] = 2
  
            # paper to scissors
            if (cell == 2):
                if (NumS > 2):
                    new_lattice[i,j] = 3

            # scissors to rock
            if (cell==3):
                if (NumR>2):
                    new_lattice[i,j] = 1



        # active_site1 = np.sum(lattice)
        # active_site2 = np.sum(new_lattice)
            
        # # stops simulation if number of active counts are the same for 10 counts, i.e. equlibrium
        # if (condition=='Random'):
        #     if (active_site1==active_site2): 
        #         counter+=1
        #     else:
        #         counter=0
        #     if(counter>20):
        #         print('Simulation Converged Early')
        #         break



        lattice = new_lattice.copy()

        if(n%10==0): 

            # prints current number of sweep to terminal
            sweeps +=10
            print(f'sweeps={sweeps}', end='\r')


            # point to record how many R states have occured
            center_idx=int(N/4)
            point1 = lattice[center_idx, center_idx]

            if (point1==1):
                R_states+=1

                # R_states_mat = lattice[lattice==1]
                # Num_R_states = np.count_nonzero(R_states_mat)

            data.write('{0:5.5e} {1:5.5e}\n'.format(sweeps, R_states))
        


            # animates spin configuration 
            plt.cla()
            im=plt.imshow(lattice, animated=True, vmin=vmin, vmax=vmax, cmap=cmap)
            plt.draw()
            plt.pause(0.0001) 


    data.close()

    # returns updated spin matrix after 10100 sweeps
    return lattice
