import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def PlotR():

    rawData = np.loadtxt('NumberR_States_good.txt')
    time = rawData[:,0]
    R_states = rawData[:,1]

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # setting figure title
    ax.set_title('Frequency of R States for Point for N=100', pad=16)
    ax.errorbar(time, R_states, marker='o', markersize = 4, linestyle='--', color='black')
    ax.set_xlabel('Time [sweeps]')
    ax.set_ylabel('Frequency of R States [-]')

    plt.savefig('R_States_Evolution.png')
    plt.show()

    return 0


def Plot_MinFrac():

    rawData = np.loadtxt('NumberR_States_good.txt')

    p3 = rawData[:,0]
    frac_mean = rawData[:,1]
    frac_var = rawData[:,2]

    # p3 = [1]
    # frac_mean = [1]
    # frac_var = [1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # setting figure title
    ax1.set_title('Average Min Frac', pad=16)
    ax1.errorbar(p3, frac_mean, marker='o', markersize = 4, linestyle='--', color='black')
    ax1.set_xlabel('Proability P3 [-]')
    ax1.set_ylabel('Average Min Frac [-]')

    ax2.set_title('Varience of Min Fac', pad=16)
    ax2.errorbar(p3, frac_var, marker='o', markersize = 4, linestyle='--', color='black')
    ax2.set_xlabel('Proability P3 [-]')
    ax2.set_ylabel('Varience of Min Fac [-]')

    plt.savefig('MinFrac_and_PhaseTransition.png')
    plt.show()

    return 0


def PlotContour():

    matrix = np.loadtxt('Varied_p2_p3_Matrix.txt.txt')

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Matrix of Min Frac', pad=10)
    ax.set_xlabel('Proability P2 [%]')
    ax.set_ylabel('Proability P3 [%]')
    im = ax.imshow(SIRS_matrix/(N**2), origin='lower', extent=[0,1,0,1], cmap='gnuplot')
    fig.colorbar(im, ax=ax, orientation='vertical')
    plt.savefig(f'partE_HeatPlot.png')

    return 0

def main():

    global N
    N=50

    # PlotR()
    Plot_MinFrac()


main()