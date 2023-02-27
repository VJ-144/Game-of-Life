import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def BootstrapError(infected_sites):
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
        sample_idx = np.random.randint(0, data_size, size=(int(data_size/Nsplit)))

        # calculating energy and magnetism subsets
        infected_subset = infected_sites[sample_idx]

        # calculating heat capacity and susceptability from subset data
        var_infected = np.var(infected_subset)/len(infected_subset)

        # adding calculated subset data to list
        infected_samples.append(var_infected)

    # taking standard deviation of sampled heat capacity and susceptability calculated from subsets
    infected_var_err = np.std(infected_samples)

    # returning errors for heat capacity and susceptability
    return infected_var_err

def plotContour(All_p1, All_p3, All_infected_avergs, err_infected_avergs):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax[0].set_title('Average Infected Sites', pad=10)
    ax[0].contour(All_p1, All_p3, All_infected_avergs, marker='o', markersize = 4, linestyle='--', color='black', capsize=3)
    ax[0].set_xlabel('Proability of Infection [%]')
    ax[0].set_ylabel('Average Infection [-]')

    return 0

def plotVar(All_p1, All_infected_var, err_infected_var):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax[1].set_title('Infected Sites Varience', pad=10)
    ax[1].errorbar(All_p1, All_infected_var, yerr=err_infected_var, marker='o', markersize = 4, linestyle='--', color='black', capsize=3)
    ax[1].set_xlabel('Proability of Infection [%]')
    ax[1].set_ylabel('Varience of Infection [-]')




def main():
    # reads data from directory with raw data of 50x50 spin configuration previously simulated
    pathToFile = os.getcwd() + f'/SIRS_Data/'
    directory = os.fsencode(pathToFile)

    All_infected_avergs = []
    All_infected_var = []
    All_p1 = []
    All_p3 = []

    err_infected_avergs = []
    err_infected_var = []

    # loops over data files in the Raw_Submission_Results directory to read results (1 loop == 1 kT simulation)
    for file in os.listdir(directory):

        # finds the path to data files
        filename = os.fsdecode(file)
        directory = os.fsdecode(directory)
        path = os.path.join(directory, filename)

        p1 = float(filename[20:23])
        p3 = float(filename[27:30])

        # reads in stored energy and magnetism data from file
        rawData = np.loadtxt(path)
        Infected_sites = rawData

        # calculates average energy and magnetism
        aver_Infected = np.mean(Infected_sites)
        var_Infected = np.var(Infected_sites)/len(Infected_sites)

        # calculating errors
        infected_var_err = BootstrapError(infected_sites)
        infected_averg_err = np.std(Infected_sites)

        # averaged data per simulation
        All_p1.append(p1)
        All_p3.append(p3)
        All_infected_avergs.append(aver_Infected)
        All_infected_var.append(var_Infected)

        # average errors per simulation
        err_infected_avergs.append(infected_averg_err)
        err_infected_var.append(infected_var_err)


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