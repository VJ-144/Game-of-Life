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
import pandas as pd


def main():

    N, p, BatchRun, immune = SIRS.initialise_simulation()

    # if (len(params)== 3): N, p, BatchRun = params
    # elif(len(params)== 4): N, p, BatchRun, immune = params

    lattice = np.random.choice([-1,0,1], size=[N,N])

    if (BatchRun=='True'):

        p2 = 0.5
        p1_list = np.linspace(0, 1, 21)
        p3_list = np.linspace(0, 1, 21)

        # p1_list = np.linspace(0.5, 1, 11)
        # p3_list = np.linspace(0.5, 1, 11)
        # print(p1_list)

        new_lattice = lattice.copy()


        mat = np.zeros([len(p1_list), len(p3_list)])

        data2=open( 'SIRS_Model_Varience','w')
        for i in range(len(p1_list)):
                for j in range(len(p1_list)):

                    p1 = p1_list[i]
                    p3 = p3_list[j]

                    # p1 = np.round(p1, 2)
                    # p3 = np.round(p3, 2)
                    
                    
                    p_new = (p1, p2, p3)
                    # print(new_lattice)

                    # print(p_new)
                    averageInfected, varience_infected = SIRS.update_SIRS(N, p_new, new_lattice, immune)
                    new_lattice = lattice.copy()
                    # print(averageInfected)
                    mat[i,j] += averageInfected 
                    print(f'completed @ P1-{p1} P2-{p2} P3-{p3}\n')
                    # print(mat)

                    data2.write('{0:5.5e} {1:5.5e} {2:5.5e} {3:5.5e} {4:5.5e} {5:5.5e}\n'.format(p1, p2, p3, immune, averageInfected, varience_infected))
                    
                    # observables = np.array([p1, p2, p3, immune, averageInfected, varience_infected])
                    # df2 = pd.DataFrame(data=observables.astype(float))
                    # df2.to_csv('SIRS_Model_Varience', sep=' ', header=False, float_format='%.5f', index=False)
                    # ['p1', 'p2', 'p2', 'Immune Prob', 'Avg. Infected', 'Var Infected']

        data2.close()


        df = pd.DataFrame(data=mat.astype(float))
        df.to_csv(f'SIRS_Proability_Matrix_Immune{immune}', sep=' ', header=False, float_format='%.2f', index=False)


    elif (BatchRun=='False'):
        print(SIRS.update_SIRS(N, p, lattice, immune))


main()