import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plotHist():

    condition = 'Random'


    pathToFile = os.getcwd() + f'/Data/{condition}/'
    directory = os.fsencode(pathToFile)

    hist_data = []

    for file in os.listdir(directory):

        # finds the path to data files
        filename = os.fsdecode(file)
        directory = os.fsdecode(directory)
        path = os.path.join(directory, filename)


        # reads in stored energy and magnetism data from file
        rawData = np.loadtxt(path)
        equilibrium_time = rawData[:,0]
        active_sites = rawData[:,1]

        counter = 0
        # find equilibrium_time using counter
        for i in range(len(active_sites)):

            active_site1 = active_sites[i]
            active_site2 = active_sites[i+1]
            
            if (active_site1==active_site2): 
                counter+=1
            else:
                counter=0

            if(counter>=10):
                hist_data.append(equilibrium_time[i])
                break


    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # plotting histogram
    ax.set_title('Absorbing States Equlibrium Time Histogram', pad=16)
    ax.hist(hist_data, bins=8, density=True)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Proability [%]')
    plt.show()




def SingleEquilibrium():


    filename = 'RandomDynamics_50N_Run37.dat'
    condition = f'Random'

    pathToFile = os.getcwd() + f'/Data/{condition}/'
    path = os.path.join(pathToFile, filename)

    rawData = np.loadtxt(path)
    time = rawData[:,0]
    active_sites = rawData[:,1]

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # setting figure title
    ax.set_title('Active Sites', pad=16)
    ax.errorbar(time, active_sites, marker='o', markersize = 4, linestyle='--', color='black')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Number of Active Sites [-]')
    plt.show()

    return 0

def line(m, x, c):
    return m*x + c

def COM_velocity():


    filename = 'gliderDynamics_50N_Run0-Good.dat'
    condition = f'glider'

    pathToFile = os.getcwd() + f'/Data/{condition}/'
    path = os.path.join(pathToFile, filename)

    rawData = np.loadtxt(path)
    time = rawData[:,0]
    xcm = rawData[:,1]
    ycm = rawData[:,2]
    
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    fig.suptitle(f'Glider Center of Mass', fontsize=16)
    fig.subplots_adjust(top=0.8, hspace=0.55, wspace=0.4)

    xx = np.arange(7)

    params1, pcov1 = curve_fit(line, time[2:10], xcm[2:10])
    params2, pcov2 = curve_fit(line, time[2:10], ycm[2:10])

    mx, cx = params1
    my, cy = params2

    # setting figure title
    ax[0].set_title('X-Component', pad=10)
    ax[0].errorbar(time, xcm, marker='o', markersize = 3, linestyle='', color='black', label='Glider COM')
    ax[0].errorbar(xx[2:10], line(xx[2:10], mx, cx), linestyle='-', color='r', label=f'Gradient={np.round(mx,2)}\nY-Intercept={np.round(cx,2)}')
    ax[0].set_xlabel('Time [s]')
    ax[0].set_ylabel('Center of Mass [-]')
    ax[0].legend(loc=0, prop={'size': 6})

    ax[1].set_title('Y-Component', pad=10)
    ax[1].errorbar(time, ycm, marker='o', markersize = 3, linestyle='', color='black', label='Glider COM')
    ax[1].errorbar(xx[2:10], line(xx[2:10], my, cy), linestyle='-', color='r', label=f'Gradient={np.round(my,2)}\nY-Intercept={np.round(cy,2)}')
    ax[1].set_xlabel('Time [s]')
    ax[1].set_ylabel('Center of Mass [-]')
    ax[1].legend(loc=2, prop={'size': 6})

    plt.show()

    return 0


def main():
    # SingleEquilibrium()
    # plotHist()
    COM_velocity()
    return 0

main()