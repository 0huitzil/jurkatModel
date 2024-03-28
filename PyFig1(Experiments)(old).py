#%% Libraries
"""
This file contains all the information necessary to create fig #1
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pathlib as pth
import pandas as pd
auto_directory = "/home/huitzil/auto/07p/python" #Update with your own AUTO directory
sys.path.append(auto_directory)
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
sys.path.append(parentPath)
latexPath = Path(os.getcwd()).parent/'Latex'
from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import fullOpenCell, icsFullOpenCell, parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS
matplotlib.rcParams.update(myRcParams())
#%% Data collection 
"""
Data 2nM Oscillations
"""
mypath = pth.Path(os.getcwd())
mypath = mypath/'dataExamples/2nMWideSOCE.csv'
dataW = pd.read_csv(mypath, index_col=0)
"""
Data 0nM Oscillations - Narrow Spikes
"""
mypath = pth.Path(os.getcwd())
mypath = mypath/'dataExamples/0nMNarrowSpikes.csv'
dataN = pd.read_csv(mypath, index_col=0)
"""
Data 0nM Oscillations - Broad Spikes
"""
mypath = pth.Path(os.getcwd())
mypath = mypath/'dataExamples/0nMBroadSpikes.csv'
dataB = pd.read_csv(mypath, index_col=0)
"""
Data 0nM Oscillations - Burst Spikes
"""
mypath = pth.Path(os.getcwd())
mypath = mypath/'dataExamples/0nMBroadSpikes-Plateau.csv'
dataBr = pd.read_csv(mypath, index_col=0)
#%% Figure creation 
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 4, nrows=3, figure=fig)
fig_width,fig_height = set_figsize(1, (1.2,1), export=True) 
fig.set_size_inches([fig_width,fig_height])
"""
Ax settings 2nM Oscillations
"""
ax = fig.add_subplot(spec[0, 0])
dataW[dataW.columns[0]].plot(ax = ax, legend=None, color = 'C2')
# Ax limits 
xlim = [0, 450]
ylim = [0, 0.8]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)
ax.set_title('A', loc='left')

ax = fig.add_subplot(spec[1, 0])
dataW[dataW.columns[1]].plot(ax = ax, legend=None, color = 'C2')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)
ax.set_ylabel(r'F$_{340}$/F$_{380}$', rotation='vertical', labelpad=0, ma='center')

ax = fig.add_subplot(spec[2, 0])
dataW[dataW.columns[2]].plot(ax = ax, legend=None, color = 'C2')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xlabel(r'Time (seconds)')
ax.set_yticks(ylim)
"""
Ax settings 0nM Oscillations - Narrow Spikes
"""
ax = fig.add_subplot(spec[0, 1])
dataN[dataN.columns[0]].plot(ax = ax, legend=None, color = 'C3')
# Ax limits 
xlim = [0, 450]
ylim = [0, 0.6]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)
ax.set_title('B', loc='left')


ax = fig.add_subplot(spec[1, 1])
dataN[dataN.columns[1]].plot(ax = ax, legend=None, color = 'C3')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)

ax = fig.add_subplot(spec[2, 1])
dataN[dataN.columns[2]].plot(ax = ax, legend=None, color = 'C3')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xlabel(r'Time (seconds)')
ax.set_yticks(ylim)
"""
Ax settings 0nM Oscillations - Broad Spikes
"""
ax = fig.add_subplot(spec[0, 2])
dataB[dataB.columns[0]].plot(ax = ax, legend=None, color = 'salmon')
# Ax limits 
xlim = [0, 450]
ylim = [0, 0.6]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)
ax.set_title('C', loc='left')


ax = fig.add_subplot(spec[1, 2])
dataB[dataB.columns[1]].plot(ax = ax, legend=None, color = 'salmon')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)

ax = fig.add_subplot(spec[2, 2])
dataB[dataB.columns[2]].plot(ax = ax, legend=None, color = 'salmon')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xlabel(r'Time (seconds)')
ax.set_yticks(ylim)
"""
Ax settings 0nM Oscillations - Burst Spikes
"""
ax = fig.add_subplot(spec[0, 3])
dataBr[dataBr.columns[0]].plot(ax = ax, legend=None, color = 'orangered')
# Ax limits 
xlim = [0, 450]
ylim = [0, 0.5]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)
ax.set_title('D', loc='left')


ax = fig.add_subplot(spec[1, 3])
dataBr[dataBr.columns[1]].plot(ax = ax, legend=None, color = 'orangered')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_xticklabels([])
ax.set_yticks(ylim)

ax = fig.add_subplot(spec[2, 3])
dataBr[dataBr.columns[2]].plot(ax = ax, legend=None, color = 'orangered')
# Ax limits 
xlim = [0, 450]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_xlabel(r'Time (seconds)')
"""
Figure saving
"""
# fig.savefig(latexPath/'Fig1.pdf')
fig.savefig('Figures/Fig1.pdf')
