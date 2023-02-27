"""
This file is used to run the ising model simulation for a single temperature and
for batches of temperatures which reuse spin configurations from previous calculations.
This file require the existence of the /Data/Glauber and /Data/Kawasaki directories in the same directory
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

This file must be run through terminal with the input arguments as follows:

'python run.ising.simulation.py N kT, model, BatchRun'

A full explanation of the parameters can be found in the README.txt file
"""


import SIRS_Functions as SIRS
import numpy as np
import time
import sys


def main():

    N, p, BatchRun = SIRS.initialise_simulation()

    lattice = np.random.choice([-1,0,1], size=[N,N])

    if (BatchRun=='True'):

        p2 = 0.5
        p1_list = np.linspace(0, 1, 101)
        p3_list = np.linspace(0, 1, 101)

        for i, p1 in enumerate(p1_list):
                for j, p3 in enumerate(p1_list):

                    p_new = (p1, p2, p3)
                    new_lattice = SIRS.update_SIRS(N, p_new, lattice)
                    print(f'completed @ P1-{p1} P2-{p2} P3-{p3}')
                    lattice = new_lattice

    elif (BatchRun=='False'):
        SIRS.update_SIRS(N, p, lattice)


main()