"""
This file is used to run the ising model simulation for a single temperature and
for batches of temperatures which reuse spin configurations from previous calculations.
This file require the existence of the /Data/Glauber and /Data/Kawasaki directories in the same directory
to store calculated data and run error analysis. The directory names are spelling and case sensitive.

This file must be run through terminal with the input arguments as follows:

'python run.ising.simulation.py N kT, model, BatchRun'

A full explanation of the parameters can be found in the README.txt file
"""


import Functions as func
import numpy as np
import time
import sys
import pandas as pd


def main():

    N, p, BatchRun = func.initialise_simulation()

    

    if (BatchRun=='Single'):

        lattice = np.random.choice([0,1], size=[N,N])

        infected_sites, sweep_times = func.Run_infection(N, p, lattice)
        np.savetxt(f'Infected_Data_{BatchRun}Run_{p}p.txt', np.array([infected_sites, sweep_times]).T)


    elif(BatchRun=='Phase'):


        # varience plots p1 --> 0.55 to 0.7 in increments of 0.001
        p1_list = np.linspace(0.55, 0.7, 31)
        # p1_list = np.linspace(0.55, 0.59, 5)
        lattice = np.random.choice([0,1], size=[N,N])

        new_lattice = lattice.copy()

        data=open(f'Infected_p0.55-0.7_{BatchRun}.txt','w')
        for i, p1 in enumerate(p1_list):

                p1 = np.round(p1, 2)

                infected_sites, sweep_times = func.Run_infection(N, p1, new_lattice)
                averge_infected = np.mean(infected_sites)
                varience_infected = np.var(infected_sites)
                var_err = func.BootstrapError(infected_sites, N)

                new_lattice = lattice.copy()

                print(f'Complete Simulation @ p={p1}')

                data.write('{0:5.5e} {1:5.5e} {2:5.5e} {3:5.5e}\n'.format(averge_infected/(N*N), varience_infected/(N*N), var_err, p1))

        data.close()

    elif(BatchRun=='Survival'):
        
        # lattice full of heathly cells
        lattice = np.random.choice([0], size=[N,N])
        new_lattice = lattice.copy()

        
        for run in range(50):

            # placing a random infected cell somewhere
            rand_idx = np.random.choice([N**2], size=[1])[0]
            new_lattice[rand_idx] = 1

            infected_sites, sweep_times = func.Run_infection(N, p, new_lattice, nstep=300)

            data=open(f'Survival\p{p}\Infected_p{p}_{run}.txt','w')
            data.write('{0:5.5e} {1:5.5e} {2:5.5e} {3:5.5e}\n'.format(run, p, infected_sites[-1], sweep_times[-1]))
            new_lattice = lattice.copy()

            print(f'Completed Run {run}\n')

        data.close()



main()