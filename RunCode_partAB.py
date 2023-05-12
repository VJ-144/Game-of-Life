"""
This file is used to run the ising model simulation for a single temperature and
for batches of temperatures which reuse spin configurations from previous calculations.
This file require the existence of the /Data/Glauber and /Data/Kawasaki directories in the same directory
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

This file must be run through terminal with the input arguments as follows:

'python run.ising.simulation.py N kT, model, BatchRun'

A full explanation of the parameters can be found in the README.txt file
"""


import Functions_partAB as func
import numpy as np
import time
import sys
import itertools

def getLattice(N):

    lattice = np.zeros(shape=(N,N))

    slice_1 = N/3
    slice_2 = N/3 + N/3
    slice_3 = N/3 + N/3 + N/3

    for ij in itertools.product(range(N), repeat=2):

        i,j = ij


        if (i+1>j):
            if (i>=N/2+1):
                lattice[i,j] = 1

        if (j>i):
            if (j>=N/2+1):
                lattice[i,j] = 2

    lattice[lattice==0] = 3

    # print(lattice)

    return lattice

def main():

    NumOfRun = 1

    N = func.initialise_simulation()

    for Run in range(NumOfRun):

        # 1 = rock
        # 2 = paper
        # 3 = scissors

        lattice = getLattice(N)
        # print(lattice)

        func.update_Game(N, lattice, Run)


main()