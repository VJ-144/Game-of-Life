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


def BootstrapError(infected_sites, N):
    """
    Calculates the errors for the specific heat capacity and susceptability using the 
    bootstrap method

    Parameters:
    energy (1D array) - All simulated energy data for a specified temperature kT per 10 sweeps when sweeps>100
    mag (1D array) - All simulated magnetism data for a specified temperature kT per 10 sweeps when sweeps>100
    N (int) - length of one axis of the spin matrix configuration
    kT (float) - initialised temperature of the simulation

    Returns:
    h_capa_err (float) - Error on the heat capacity run at the specified temperature kT
    suscept_err (float) - Error on the susceptability run at the specified temperature kT
    """
    
    # number of groups the data will be split into for sampling
    Nsplit = 10
    data_size = len(infected_sites)
    infected_sites = np.asarray(infected_sites)
    # list to store sampled heat capacities and suseptabilites
    infected_samples = []

    # looping over number of groups
    for i in range(Nsplit):

        # generating random indices to sample subsets
        sample_idx = np.random.randint(low=0, high=data_size-1, size=data_size, dtype=int)
        

        # if (np.sum(infected_sites)==0 or np.sum(infected_sites)==1): return 0

        # print(len(sample_idx))
        # print(len(infected_sites))
        # print(sample_idx)
        # print(infected_sites)

        infected_subset = infected_sites[sample_idx]
        
        # calculating heat capacity and susceptability from subset data
        var_infected = np.var(infected_subset)/(N**2)

        # adding calculated subset data to list
        infected_samples.append(var_infected)

    # taking standard deviation of sampled heat capacity and susceptability calculated from subsets
    infected_var_err = np.std(infected_samples)

    # returning errors for heat capacity and susceptability
    return infected_var_err


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


def initialise_simulation():

    # checks command line arguments are correct otherwise stops simulation
    # if (len(sys.argv) < 6):
    #     print("Error Input Usage: python ising.animation.py N p1 p2 p3 --optional BatchRun [True/False]")
    #     sys.exit()
    
    N=int(sys.argv[1])


    return N

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

def update_SIRS(N, lattice, p):

    p1, p2, p3 = p

    cmap = ListedColormap([ 'red', 'green', 'dodgerblue'])
    vmin = 1
    vmax = 4

    # setting up animantion figure
    fig = plt.figure()
    im=plt.imshow(lattice, animated=True, vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar()


    # number of sweeps for simulation
    nstep=1000
    sweeps = 0

    new_lattice = lattice.copy()
    
    
    fracR_list = []
    fracP_list = []
    fracS_list = []
    sweeps_list = []

    counter=0
    for n in range(nstep):

        i_list, j_list = GenerateRandom_Idx(N)
    
        for k in itertools.product(range(N*N)):

            i = i_list[k]
            j = j_list[k]

            cell = lattice[i,j]

            # i,j = ij
            cell = lattice[i,j]
            NumR, NumP, NumS = neighbors((i,j), lattice, N)

            # 1 = rock
            # 2 = paper
            # 3 = scissors

            p1_threshold = np.random.random()
            p2_threshold = np.random.random()
            p3_threshold = np.random.random()

            # rock to paper
            if (cell == 1):
                if (NumP>1 and p1 > p1_threshold):
                    #changing R to P
                    lattice[i,j] = 2
  
            # paper to scissors
            if (cell == 2):
                if (NumS>1 and p2 > p2_threshold):
                    lattice[i,j] = 3

            # scissors to rock
            if (cell==3):
                if (NumR>1 and p2 > p2_threshold):
                    lattice[i,j] = 1


        new_lattice = lattice.copy()

        if(n%10==0 and n>500):      

            # prints current number of sweep to terminal
            sweeps +=10
            print(f'sweeps={sweeps}', end='\r')

            Mat_R = lattice[lattice==1]
            Number_R = np.count_nonzero(Mat_R)
            frac_R = Number_R/(N*N)

            Mat_P = lattice[lattice==2]
            Number_P = np.count_nonzero(Mat_P)
            frac_P = Number_P/(N*N)

            Mat_S = lattice[lattice==3]
            Number_S = np.count_nonzero(Mat_S)
            frac_S = Number_S/(N*N)  


            fracR_list.append(frac_R)
            fracP_list.append(frac_P)
            fracS_list.append(frac_S)
            sweeps_list.append(sweeps)
 

            # animates spin configuration 
            plt.cla()
            im=plt.imshow(lattice, animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
            plt.draw()
            plt.pause(0.0001) 



    allData = np.array([fracR_list, fracR_list, fracR_list])

    min_frac = np.min(allData, axis=0)

    minFrac_avg = np.mean(min_frac)
    minFrac_var = np.var(min_frac)
    minFrac_err = BootstrapError(min_frac, N)


    return minFrac_avg, minFrac_var, minFrac_err
    
