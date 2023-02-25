"""
This file is used to run the ising model simulation for a single temperature and
for batches of temperatures which reuse spin configurations from previous calculations.
This file require the existence of the /Data/Glauber and /Data/Kawasaki directories in the same directory
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

This file must be run through terminal with the input arguments as follows:

'python run.ising.simulation.py N kT, model, BatchRun'

A full explanation of the parameters can be found in the README.txt file
"""


import GameOfLife_functions as gom
import numpy as np
import time
import sys


def main():

    N, condition = gom.initialise_simulation()

    if (condition=='blinker' or condition=='glider'):
        lattice = np.zeros([N,N])
    else:
        lattice = np.random.choice([0,1], size=[N,N])

    NumOfRun = 3

    for Run in range(NumOfRun):
        gom.update_Game(N, condition, lattice, Run)


main()