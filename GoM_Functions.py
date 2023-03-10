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

    num_neighbors = np.sum([T, B, R, L, TR, BR, TL, BL])

    return num_neighbors



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

    if (len(sys.argv) == 3): condition=str(sys.argv[2])

    return N, condition



def update_Game(N, condition, lattice, Run):

    lattice = setCondition(N, condition, lattice)    
    new_lattice = lattice.copy()

    # setting up animantion figure
    # fig = plt.figure()
    # im=plt.imshow(new_lattice, animated=True)

    # number of sweeps for simulation
    nstep=12000

    # sweeps counter
    sweeps = 0

    outFilePath = os.getcwd() + f'/GoM_Data/{condition}/{N}N_{condition}Dynamics_GoMRun{Run}.dat'
    data=open( outFilePath,'w')

    start_time= datetime.datetime.now()
    counter=0
    for n in range(nstep):
        xcm_top = 0
        ycm_top = 0
        for ij in itertools.product(range(N), repeat=2):

            i,j = ij
            cell = lattice[i,j]
            AliveNeighbors = neighbors(ij, lattice, N)

            # update rules for alive cell
            if (cell == 1):
                if (AliveNeighbors<2 or AliveNeighbors>3):
                    new_lattice[i,j] = 0
                elif(AliveNeighbors==2 or AliveNeighbors==3):
                    new_lattice[i,j] = 1

            # updates rules for dead cell
            elif(cell == 0):
                if(AliveNeighbors==3):
                    new_lattice[i,j] = 1


            # calculating glider cm
            if (condition=='glider' and cell==1):

                xcm_idx = np.where(lattice == 1)[0]
                ycm_idx = np.where(lattice == 1)[1]
                
                xmin = np.min(xcm_idx)
                xmax = np.max(xcm_idx)

                ymin = np.min(ycm_idx)
                ymax = np.max(ycm_idx)

                deltaX = np.abs(xmax - xmin)
                deltaY = np.abs(ymax - ymin)

                if (deltaX > N/2 or deltaY > N/2): continue

                xcm_top += (i * cell )
                ycm_top += (j * cell )



        active_site1 = np.sum(lattice)
        active_site2 = np.sum(new_lattice)
            
        # stops simulation if number of active counts are the same for 10 counts, i.e. equlibrium
        if (condition=='Random'):
            if (active_site1==active_site2): 
                counter+=1
            else:
                counter=0
            if(counter>20):
                print('Simulation Converged Early')
                break

        lattice = new_lattice.copy()

        if(n%10==0): 

            # prints current number of sweep to terminal
            sweeps +=10
            print(f'sweeps={sweeps}', end='\r')


            # calculating number of active sites
            active_sites = np.sum(lattice)
        

            # storing center of mass data if glider simulation
            if (condition=='glider'):

                xcm = xcm_top/np.sum(lattice)
                ycm = ycm_top/np.sum(lattice)         

                if (deltaX > N/2 or deltaY > N/2): continue

                data.write('{0:5.5e} {1:5.5e} {2:5.5e}\n'.format(n, xcm, ycm))

            else:
                data.write('{0:5.5e} {1:5.5e}\n'.format(n, active_sites))


            # animates spin configuration 
            # plt.cla()
            # im=plt.imshow(lattice, animated=True)
            # plt.draw()
            # plt.pause(0.0001) 


    data.close()

    # returns updated spin matrix after 10100 sweeps
    return lattice
