import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

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
        equilibrium_time = rawData[:,0][-1]
        hist_data.append(equilibrium_time)


    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    # plotting histogram
    ax.set_title('Active Sites Equlibrium ', pad=16)
    ax.hist(hist_data, density=True)
    ax.set_xlabel('Time to Steady State [sweeps]')
    ax.set_ylabel('Proability [%]')
    plt.show()




def SingleEquilibrium():


    filename = 'RandomDynamics_10N_Run2.dat'
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


def main():
    SingleEquilibrium()
    # plotHist()
    return 0

main()