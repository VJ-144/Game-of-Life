import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

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

    # list to store sampled heat capacities and suseptabilites
    infected_samples = []

    # looping over number of groups
    for i in range(Nsplit):

        # generating random indices to sample subsets
        sample_idx = np.random.randint(0, data_size, size=Nsplit)

        # calculating energy and magnetism subsets
        infected_subset = infected_sites[sample_idx]

        # calculating heat capacity and susceptability from subset data
        var_infected = np.var(infected_subset)/(N**2)

        # adding calculated subset data to list
        infected_samples.append(var_infected)

    # taking standard deviation of sampled heat capacity and susceptability calculated from subsets
    infected_var_err = np.std(infected_samples)

    # returning errors for heat capacity and susceptability
    return infected_var_err

def plotContour(SIRS_matrix, N):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Average Infected Sites for {N}x{N} Matrix', pad=10)
    ax.set_xlabel('Proability of Infection p3 [%]')
    ax.set_ylabel('Proability of Infection p1 [%]')
    ax.imshow(SIRS_matrix/(N**2))
    plt.show()

    return 0

def plotVar(AllData, N):


    All_infected_var = AllData[:,5]
    All_p1 = np.linspace(0, 1, 21)

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title('Infected Sites Varience', pad=10)
    ax.errorbar(All_p1, All_infected_var/(N**2), marker='o', markersize = 4, linestyle='--', color='black', capsize=3)  # , yerr=err_infected_var  taking this out as errors are not yet calculated
    ax.set_ylabel('Proability of Infection [%]')
    ax.set_xlabel('Varience of Infection [-]')
    plt.show()




def main():
 
    AllData = np.loadtxt('SIRS_Model_Varience_20N.txt')
    SIRS_matrix = np.loadtxt('SIRS_Proability_Matrix_20N.txt')

    N = 20

    plotContour(SIRS_matrix, N)
    plotVar(AllData, N)

    # fig, ax = plt.subplots(2, 2, figsize=(7, 5))

    # # setting figure title
    # fig.suptitle(f'{model} Model {N}x{N}N at Varied Temperature', fontsize=16)
    # fig.subplots_adjust(top=0.8, hspace=0.55, wspace=0.4)

    # # plotting susceptibility
    # ax[0,0].set_title('Susceptibility', pad=16)
    # ax[0,0].errorbar(tot_kT, tot_sus, marker='o', markersize = 4, linestyle='--', yerr=tot_suscept_err, color='black', capsize=3)
    # ax[0,0].set_xlabel('kT [K]')
    # ax[0,0].set_ylabel('$\chi(M)$ [-]')
    


main()