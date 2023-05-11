import string
import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def plotInfected(data, p):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    # p=0.6
    infected = data[:,0]
    sweeps = data[:,1]

    ax.set_title(f'Infected Sites for {N}N P={p} Simulation', pad=10)
    ax.set_xlabel('Time [sweeps]')
    ax.set_ylabel('Number of Infected Sites [-]')
    ax.plot(sweeps, infected, marker='o', markersize = 4, linestyle='--', color='black')
    plt.savefig(f'Infected_Plot_{N}x{N}N_{p}p.png')


def plotSurvival_Hist(data, p):

    infected = data[:,0]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    ax.set_title(f'Infected Sites at p={p} for {N}x{N} Matrix', pad=10)
    ax.set_xlabel('Infected Sites at time 300 sweeps')
    ax.set_ylabel('Normalised Probability [-]')
    ax.hist(hist_data, bins=30, density=True,  facecolor = '#2ab0ff', edgecolor='#169acf', linewidth=0.5)

    plt.savefig(f'Survival_{N}x{N}N_{p}p_Hist.png')


def plotSurvival_Log(prob1, prob2, prob3):

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))

    time = np.linspace(0, 300, 301)[1:]


    ax.set_title(f'Survival Proability for Infected Sites', pad=10)
    ax.set_xlabel('Log Time [sweeps]')
    ax.set_ylabel('Log Survival Proabilities [-]')
    ax.plot(np.log10(time), np.log10(prob1), marker='', markersize = 4, linestyle='--', color='red', label='p=0.6')
    ax.plot(np.log10(time), np.log10(prob2), marker='', markersize = 4, linestyle='--', color='blue', label='p=0.625')
    ax.plot(np.log10(time), np.log10(prob3), marker='', markersize = 4, linestyle='--', color='limegreen', label='p=0.65')


    plt.legend()

    plt.savefig(f'Survival_{N}x{N}N_Log.png')
    plt.show()



def plotPhase(AllData):

    average_inf = AllData[:,0]
    varience_inf = AllData[:,1]
    var_err = AllData[:,2]
    p = AllData[:,3]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.set_title(f'Average Infected Sites for {N}x{N} Matrix', pad=10)
    ax1.plot(p, average_inf, marker='o', markersize = 4, linestyle='--', color='black')  
    ax1.set_xlabel('Proability of Infection P [-]')
    ax1.set_ylabel('Average Infection per Site [-]')


    ax2.set_title(f'Infected Sites Variance for {N}x{N} Matrix', pad=10)
    ax2.errorbar(p, varience_inf, yerr=var_err, marker='o', markersize = 4, linestyle='--', color='black', capsize=3)
    ax2.set_xlabel('Proability of Infection P [-]')
    ax2.set_ylabel('Variance of Infection per Site [-]')


    plt.savefig(f'Phase_trans_{N}x{N}_Wave.png')
    plt.show()


def main():
    global N
    N = 50

    # single_run = np.loadtxt('Infected_Data_SingleRun_0.7p.txt')
    # Phase = np.loadtxt('Infected_p0.55-0.7_Phase_good.txt')
    prob1 = np.loadtxt('SurvivalProabilites_p0.6.txt')
    prob2 = np.loadtxt('SurvivalProabilites_p0.625.txt')
    prob3 = np.loadtxt('SurvivalProabilites_p0.65.txt')

    # plotInfected(single_run, p=0.7)
    # plotPhase(Phase)    
    plotSurvival_Log(prob1, prob2, prob3)

    

main()