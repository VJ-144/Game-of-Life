import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def plotContour(SIRS_matrix):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Average Infected Sites for {N}x{N} Matrix', pad=10)
    ax.set_xlabel('Proability of Infection P1 [%]')
    ax.set_ylabel('Proability of Infection P3 [%]')
    im = ax.imshow(SIRS_matrix/(N**2), origin='lower', extent=[0,1,0,1], cmap='gnuplot')
    fig.colorbar(im, ax=ax, orientation='vertical')
    plt.savefig(f'SIRS_{50}x{50}_HeatPlot.png')

    return 0

def plotWave(AllData):

    All_p1 = AllData[:,0]
    All_infected_var = AllData[:,5]
    ver_err = AllData[:,6]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Infected Sites Wave/Variance for {N}x{N} Matrix', pad=10)
    ax.errorbar(All_p1, All_infected_var/(N**2), yerr=ver_err, marker='o', markersize = 4, linestyle='--', color='black', capsize=3)  # , yerr=err_infected_var  taking this out as errors are not yet calculated
    ax.set_xlabel('Proability of Infection P1 [%]')
    ax.set_ylabel('Variance of Infection [-]')
    plt.savefig(f'SIRS_{50}x{50}_Wave.png')


def plotImmune(AllData):

    p_Imm = AllData[:,3]
    All_infected_var = AllData[:,5]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Infected Sites Immunity Variation for {N}x{N} Matrix', pad=10)
    ax.errorbar(p_Imm, All_infected_var/(N**2), marker='o', markersize = 4, linestyle='--', color='black', capsize=3)  # , yerr=err_infected_var  taking this out as errors are not yet calculated
    ax.set_xlabel('Percentage of Immune Population [%]')
    ax.set_ylabel('Number of Infected Sites [-]')
    plt.savefig(f'SIRS_{50}x{50}_Immunity.png')


def main():
 
    path = 'C:\\Users\\Vijay\\OneDrive\\Documents\\Univeristy Work\\Year 5\\MVP\\Checkpoint2\\Game of Life\\GoodData\\'

    global N
    N = 50

    # SIRS_HeatMap = np.loadtxt(path + 'HeatMap\\SIRS_Proability_Matrix_VariedP1P3_Imm0.txt')
    SIRS_Wave = np.loadtxt(path + 'Variance_Wave\\SIRS_Model_TotalData_VarWave.txt')
    # SIRS_Imm = np.loadtxt(path + 'SIRS_Proability_Matrix_VariedP1P3_Imm0.txt')

    # plotContour(SIRS_matrix, N)
    plotWave(SIRS_Wave)
    # plotImmune(SIRS_Imm)
    

main()