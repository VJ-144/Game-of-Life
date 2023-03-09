import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def plotContour(SIRS_matrix, N):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Average Infected Sites for {N}x{N} Matrix', pad=10)
    ax.set_xlabel('Proability of Infection p1 [%]')
    ax.set_ylabel('Proability of Infection p3 [%]')
    ax.imshow(SIRS_matrix/(N**2), origin='lower', extent=[0,1,0,1])
    plt.show()

    return 0

def plotVar(AllData, N):

    All_p1 = AllData[:,0]
    All_infected_var = AllData[:,5]
    ver_err = AllData[:,6]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title('Infected Sites Varience', pad=10)
    ax.errorbar(All_p1, All_infected_var/(N**2), yerr=ver_err, marker='o', markersize = 4, linestyle='--', color='black', capsize=3)  # , yerr=err_infected_var  taking this out as errors are not yet calculated
    ax.set_ylabel('Proability of Infection [%]')
    ax.set_xlabel('Varience of Infection [-]')
    plt.show()


def main():
 
    path = 'C:\\Users\\Vijay\\OneDrive\\Documents\\Univeristy Work\\Year 5\\MVP\\Checkpoint2\\Game of Life\\GoodData\\'

    AllData = np.loadtxt(path + 'SIRS_ModelAllData_VariedP1P3_Imm0.txt')
    SIRS_matrix = np.loadtxt(path + 'SIRS_Proability_Matrix_VariedP1P3_Imm0.txt')

    N = 50

    plotContour(SIRS_matrix, N )
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