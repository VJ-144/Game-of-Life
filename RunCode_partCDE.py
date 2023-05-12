"""
This file is used to run the ising model simulation for a single temperature and
for batches of temperatures which reuse spin configurations from previous calculations.
This file require the existence of the /Data/Glauber and /Data/Kawasaki directories in the same directory
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

This file must be run through terminal with the input arguments as follows:

'python run.ising.simulation.py N kT, model, BatchRun'

A full explanation of the parameters can be found in the README.txt file
"""

import Functions_partCDE as func
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


    N, condition = func.initialise_simulation()

    if (condition=='partD'):

        p11 = 0.5
        p22 = 0.5


        NumOfRun = 1
        for Run in range(NumOfRun):

            # 1 = rock
            # 2 = paper
            # 3 = scissors

            lattice = getLattice(N)

            p3_list = np.linspace(0, 0.1, 11)

            # print(p3_list)

            data=open(f'Varying_p3_Data_partD.txt','w')

            for i, p3_new in enumerate(p3_list):

                p3_new = np.round(p3_new, 2)

                p_new = (p11, p22, p3_new)

                avg, var, err = func.update_SIRS(N, lattice, p_new)

                data.write('{0:5.5e} {1:5.5e} {2:5.5e}\n'.format(p3_new, avg, var))


                print(f'Complete p3={p3_new}')


    elif (condition=='partE'):

        p1 = 0.5
        p2_list = np.linspace(0, 0.1, 11)
        p3_list = np.linspace(0, 0.1, 11)

        new_lattice = lattice.copy()
        mat = np.zeros([len(p1_list), len(p3_list)])

        data=open(f'Data_partE.txt','w')

        for i, p2 in enumerate(p2_list):
                for j, p3 in enumerate(p3_list):

                    p2 = np.round(p1, 2)
                    p3 = np.round(p3, 2)
                    p_new = (p1, p2, p3)

                    avg, var, err = SIRS.update_SIRS(N, p_new, new_lattice, immune)
                    new_lattice = lattice.copy()

                    # adding the average value calculated using p2, p3 to a matrix for plotting
                    mat[i,j] += avg
                    print(f'completed @ P1-{p1} P2-{p2} P3-{p3}\n')

                    data.write('{0:5.5e} {1:5.5e} {2:5.5e} {3:5.5e} {4:5.5e} {5:5.5e} {6:5.5e}\n'.format(p1, p2, p3, avg, var, err))

        data.close()


        np.savetxt('Varied_p2_p3_Matrix.txt', mat)


main()

