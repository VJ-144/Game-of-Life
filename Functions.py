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
        
        infected_subset = infected_sites[sample_idx]
        
        # calculating heat capacity and susceptability from subset data
        var_infected = np.var(infected_subset)/(N**2)

        # adding calculated subset data to list
        infected_samples.append(var_infected)

    # taking standard deviation of sampled heat capacity and susceptability calculated from subsets
    infected_var_err = np.std(infected_samples)

    # returning errors for heat capacity and susceptability
    return infected_var_err


def Infect_neighbors(idx, lattice, N):

    i, j = idx

    # center = lattice[i,j]
    # T = lattice[(i-1)%N, j]
    # B = lattice[(i+1)%N, j]
    # R = lattice[i, (j+1)%N]
    # L = lattice[i, (j-1)%N]

    # setting neighbor to infected based off random prability once the cell being infected is known

    rand_neighbor = np.random.choice([1,2,3,4], size=[1])[0]

    if (rand_neighbor==1): lattice[(i-1)%N, j] = 1
    elif (rand_neighbor==2): lattice[i, (j+1)%N] = 1
    elif (rand_neighbor==3): lattice[(i+1)%N, j] = 1
    elif (rand_neighbor==4): lattice[i, (j-1)%N] = 1

    return lattice


def initialise_simulation():

    # checks command line arguments are correct otherwise stops simulation
    if (len(sys.argv) < 3):
        print("Error Input Usage: python RunCode.py N BatchRun")
        print('BatchRun Parameter Options:\n1 -- Single\n2 -- Phase\n3-- Survival')
        sys.exit()
    
    N=int(sys.argv[1])
    p=float(sys.argv[2])
    BatchRun = str(sys.argv[3])

    return N, p, BatchRun 

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

def Run_infection(N, p, lattice, nstep=10500):

    # setting up animantion figure
    fig = plt.figure()
    cmap = ListedColormap(['dodgerblue', 'red'])
    im=plt.imshow(lattice, animated=True, cmap=cmap, vmin=-1, vmax=2)
    fig.colorbar(im)

    # number of sweeps for simulation
    # nstep=10500
    sweeps = 0

    new_lattice = lattice.copy()
    infected_sites=[]
    sweep_times = []

    counter=0
    for n in range(nstep):

        i_list, j_list = GenerateRandom_Idx(N)
    
        for k in itertools.product(range(N*N)):

            i = i_list[k]
            j = j_list[k]

            cell = lattice[i,j]

            # infected == 1
            # healthy == 0

            # skip iteration if cell is healthy
            if (cell == 0): continue

            # infection spreading/recovery conditions for infected cell
            if (cell == 1):

                p1_threshold = np.random.random()
                p2_threshold = np.random.random()

                # makes healthy if passes check
                if (1-p > p1_threshold): lattice[i,j] = 0

                # infects neighbours
                if (p > p2_threshold): lattice = Infect_neighbors((i,j), lattice, N)
                    

        # count the number of infected states
        # stops simulation if number of active counts are the same for 10 counts, i.e. equlibrium
        infected_MatTrue1 = lattice[lattice==1]
        Num_infected_sites1 = np.count_nonzero(infected_MatTrue1) 

        infected_MatTrue2 = new_lattice[new_lattice==1]
        Num_infected_sites2 = np.count_nonzero(infected_MatTrue2)  

        new_lattice = lattice.copy()

        if(n%10==0):      

            # prints current number of sweep to terminal
            sweeps +=10
            print(f'sweeps={sweeps}', end='\r')

            infected_sites.append(Num_infected_sites1)
            sweep_times.append(sweeps)

            if (Num_infected_sites1==Num_infected_sites2): 
                counter+=1
            else:
                counter=0

            if(counter>=10):

                print('Simulation Converged Early')
                # print(f'Avg. Number of Infected Sites = {averge_infected}')

                return infected_sites, sweep_times

            # animates spin configuration 
            plt.cla()
            im=plt.imshow(lattice, animated=True, cmap=cmap, vmin=-1, vmax=2)
            plt.draw()
            plt.pause(0.0001) 

    return infected_sites, sweep_times
