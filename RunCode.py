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
        frac_infected = np.asarray(infected_sites)/(N*N)
        np.savetxt(f'Infected_Data_{BatchRun}Run_{p}p.txt', np.array([frac_infected, sweep_times]).T)


    elif(BatchRun=='Phase'):


        # varience plots p1 --> 0.55 to 0.7 in increments of 0.005
        p1_list = np.linspace(0.55, 0.7, 31)

        lattice = np.random.choice([0,1], size=[N,N])

        new_lattice = lattice.copy()

        data=open(f'Infected_p0.55-0.7_{BatchRun}.txt','w')
        for i, p1 in enumerate(p1_list):

                p1 = np.round(p1, 3)

                infected_sites, sweep_times = func.Run_infection(N, p1, new_lattice)
                averge_infected = np.mean(infected_sites)/(N*N)
                varience_infected = np.var(infected_sites)/(N*N)
                var_err = func.BootstrapError(infected_sites, N)/(N*N)

                new_lattice = lattice.copy()

                print(f'Complete Simulation @ p={p1}')

                data.write('{0:5.5e} {1:5.5e} {2:5.5e} {3:5.5e}\n'.format(averge_infected, varience_infected, var_err, p1))

        data.close()

    elif(BatchRun=='Survival'):
        
        # lattice full of heathly cells
        lattice = np.random.choice([0], size=[N,N])
        new_lattice = lattice.copy()

        active = []

        NumOfRuns = 200

        # placing a random infected cell somewhere
        xx_idx1 = np.random.randint(low=0, high=N-1, size=NumOfRuns)
        yy_idx1 = np.random.randint(low=0, high=N-1, size=NumOfRuns)
        
        for run in range(NumOfRuns):

            # # placing a random infected cell somewhere
            xx_idx = xx_idx1[run]
            yy_idx = yy_idx1[run]

            new_lattice[xx_idx, yy_idx] = 1

            infected_sites, sweep_times = func.Run_infection(N, p, new_lattice, nstep=300)
            infected_sites = np.asarray(infected_sites)
            # sets infected matrix at time step sweep equal to 1
            infected_sites[infected_sites>0] = 1

            active.append(infected_sites)
            # print(active)

            new_lattice = lattice.copy()

            print(f'Completed Run {run}')

        proabilites = np.sum(active, axis=0)
        np.savetxt(f'SurvivalProabilites_p{p}.txt', proabilites)



main()