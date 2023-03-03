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


def Infected_neighbors(idx, lattice, N):

    i, j = idx
    center = lattice[i,j]

    T = lattice[(i-1)%N, j]
    B = lattice[(i+1)%N, j]
    R = lattice[i, (j+1)%N]
    L = lattice[i, (j-1)%N]

    neighbors = [T, B, R, L]

    if -1 in neighbors:
        return True
    else:
        return False


def initialise_simulation():

    # checks command line arguments are correct otherwise stops simulation
    if (len(sys.argv) < 6):
        print("Error Input Usage: python ising.animation.py N p1 p2 p3 --optional BatchRun [True/False]")
        sys.exit()
    
    N=int(sys.argv[1])
    p1=float(sys.argv[2])
    p2=float(sys.argv[3])
    p3=float(sys.argv[4])
    BatchRun = str(sys.argv[5])
    imm_percent = float(sys.argv[6])

    p = (p1, p2, p3)

    return N, p, BatchRun, imm_percent

def GenerateRandom_Idx(N):
    """
    Generates random number which act as the indices to sample the spin configuration for a complete sweep
    of the Glauber or Kawasaki method

    Parameters:
    N (int) - length of one axis of the spin matrix configuration

    Returns:
    i (1D array) - array of random indices to be used in sampling 1 axes (x-axes) of the spin configuration
    j (1D array) - array of random indices to be used in sampling 1 axes (y-axes) of the spin configuration
    """

    # array of random i and j indices to be used for sampling the spin matrix per sweep 
    i = np.random.choice(N, N*N)
    j = np.random.choice(N, N*N)

    # returns tuple of indice i and j arrays to sample the spin configuration 
    return (i, j)

def update_SIRS(N, p, lattice, imm_percent):
  
    p1, p2, p3 = p


    if (imm_percent!=0):
        imm_size = int(imm_percent*(N*N))
        imm_x = np.random.choice(N, imm_size)
        imm_y = np.random.choice(N, imm_size)
        lattice[imm_x, imm_y] = -2
        cmap = ListedColormap(['r', 'limegreen', 'yellow', 'dodgerblue'])
        vmin = -2
        vmax = 1
    else:
        cmap = ListedColormap(['limegreen', 'yellow', 'dodgerblue'])
        vmin = -1
        vmax = 1


    # setting up animantion figure
    fig = plt.figure()
    im=plt.imshow(lattice, animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
    fig.colorbar(im)

    # number of sweeps for simulation
    nstep=10100

    # sweeps counter
    sweeps = 0


    outFilePath = os.getcwd() + f'/SIRS_Data/SIRS_{N}N_P1-{p1}_P2-{p2}_P3-{p3}.dat'
    data=open( outFilePath,'w')


    start_time= datetime.datetime.now()

    for n in range(nstep):

        i_list, j_list = GenerateRandom_Idx(N)

        # p1_threshold = random.random()
        # p2_threshold = random.random()
        # p3_threshold = random.random()   

        for k in itertools.product(range(N*N)):

            i = i_list[k]
            j = j_list[k]

            cell = lattice[i,j]

            # infected == -1
            # susceptabile == 0
            # recovered == 1
            # immune ==-2

            p1_threshold = np.random.random()
            p2_threshold = np.random.random()
            p3_threshold = np.random.random()

            # rule 1 - becoming infected
            Infected_N = Infected_neighbors((i,j), lattice, N)
            if (cell == 0 and p1 > p1_threshold):
                if (Infected_N): lattice[i,j] = -1

            # rule 2 - becoming recovered
            if (cell == -1 and p2 > p2_threshold): lattice[i,j] = 1

            # rule 3 - becoming susceptabile
            if (cell == 1 and p3 > p3_threshold): lattice[i,j] = 0



        if(n%10==0):

            # count the number of infected states
            infected_MatTrue = lattice[lattice==-1]
            Num_infected_sites = np.count_nonzero(infected_MatTrue)             

            # prints current number of sweep to terminal
            sweeps +=10
            print(f'sweeps={sweeps}', end='\r')

            data.write('{0:5.5e}\n'.format(Num_infected_sites))

            # animates spin configuration 
            plt.cla()
            im=plt.imshow(lattice, animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
            plt.draw()
            plt.pause(0.0001) 

    data.close()

    # returns updated spin matrix after 10100 sweeps
    return lattice
