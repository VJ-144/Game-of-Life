import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plotHist():

    condition = 'Random'


    pathToFile = os.getcwd() + f'/GoM_Data/{condition}/'
    directory = os.fsencode(pathToFile)

    hist_data = []

    for file in os.listdir(directory):

        # finds the path to data files
        filename = os.fsdecode(file)
        directory = os.fsdecode(directory)
        path = os.path.join(directory, filename)

        rawData = np.loadtxt(path)
        equilibrium_time = rawData[:,0]
        active_sites = rawData[:,1]

        # manually check if data has converged, prints filename if not
        # if (len(equilibrium_time)==1200): print(filename)

        # already check in simulation if last data points converge with counter
        hist_data.append(equilibrium_time[-1])

    fig, ax = plt.subplots(1, 1, figsize=(6, 5), layout="constrained")

    # plotting histogram
    ax.set_title(f'Absorbing States Equlibrium Time {N}x{N} Matrix', pad=16)
    ax.hist(hist_data, bins=30, density=True,  facecolor = '#2ab0ff', edgecolor='#169acf', linewidth=0.5)
    ax.set_xlabel('Sweeps [-]')
    ax.set_ylabel('Normalised Probability [%]')
    plt.savefig(f'GOM_Equlibrium_Time_Hist_{N}N.png')




def SingleEquilibrium():


    filename = 'RandomDynamics_50N_Run38.dat'
    condition = f'Random'

    pathToFile = os.getcwd() + f'/GoM_Data/{condition}/'
    path = os.path.join(pathToFile, filename)

    rawData = np.loadtxt(path)
    time = rawData[:,0]
    active_sites = rawData[:,1]

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # setting figure title
    ax.set_title('Active Sites', pad=16)
    ax.errorbar(time[1:200], active_sites[1:200], marker='o', markersize = 4, linestyle='--', color='black')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Number of Active Sites [-]')
    plt.show()

    return 0

def line(m, x, c):
    return m*x + c

def COM_velocity():


    filename = '50N_gliderDynamics_GoMRun0.dat'
    condition = f'glider'

    pathToFile = os.getcwd() + f'/GoM_Data/{condition}/'
    path = os.path.join(pathToFile, filename)

    rawData = np.loadtxt(path)
    time = rawData[:,0]
    xcm = rawData[:,1]
    ycm = rawData[:,2]
    
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    fig.subplots_adjust(top=0.8, hspace=0.55, wspace=0.4)

    xx = np.arange(200)

    params1, pcov1 = curve_fit(line, time[2:10], xcm[2:10])
    params2, pcov2 = curve_fit(line, time[2:10], ycm[2:10])

    mx, cx = params1
    my, cy = params2

    # setting figure title
    ax[0].set_title(f'COM X-Component Position', pad=10)
    ax[0].errorbar(time, xcm, marker='o', markersize = 3, linestyle='', color='black', label='Glider X-Comp. COM')
    ax[0].errorbar(xx[20:80], line(xx[20:80], mx, cx), linestyle='-', color='r', label=f'Gradient={np.round(mx,2)}\nY-Intercept={np.round(cx,2)}')
    ax[0].set_xlabel('Sweeps [-]')
    ax[0].set_ylabel('X-Component Position [-]')
    ax[0].legend(loc=0, prop={'size': 6})

    ax[1].set_title('COM Y-Component Position', pad=10)
    ax[1].errorbar(time, ycm, marker='o', markersize = 3, linestyle='', color='black', label='Glider Y-Comp. COM')
    ax[1].errorbar(xx[20:80], line(xx[20:80], my, cy), linestyle='-', color='r', label=f'Gradient={np.round(my,2)}\nY-Intercept={np.round(cy,2)}')
    ax[1].set_xlabel('Sweeps [-]')
    ax[1].set_ylabel('X-Component Position [-]')
    ax[1].legend(loc=2, prop={'size': 6})

    fig.suptitle(f'Glider Center of Mass Velocity-{np.round(np.sqrt(my**2 + mx**2), 2)} pixels/sweep', fontsize=16)

    # ax[0].text(0, 0, f'COM velocity {np.round(np.sqrt(my**2 + mx**2), 2)}')

    plt.savefig(f'GOM_CoM_{N}N.png')

    return 0


def main():

    global N
    N=50
    # SingleEquilibrium()
    # plotHist()
    COM_velocity()
    return 0

main()