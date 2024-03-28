#%% Libraries
"""
This file contains all the scripts necessary to create fig #1
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
# from pathlib import Path
# parentPath = str(Path(os.getcwd()).parent)
# sys.path.append(parentPath)
# latexPath = Path(os.getcwd()).parent/'Latex'
from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import fullOpenCell, icsFullOpenCell, parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS
matplotlib.rcParams.update(myRcParams())
#%% Data collection 
"""
Data Simulation - Wide SOCE
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
ics['c']=0.085
ics['ce']=850
ics['s']=0
model = fullOpenCell
tini, talpha, tf = [0, 10, 240]
par['Vplc']=0.1
dataSW = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Narrow Spike
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, tsim, tf = [0, 200, 40]
par['Ct']=140
par['Vplc']=0.0
dataSN = getIVP(model, par, ics, tini=tini, tf=tsim)
ics = getnewICS(dataSN)
par['Vplc']=0.1
dataSN = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Simulation - Broad Spike
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, tsim, tf = [0, 200, 40]
par['Vplc']=0.0
par['Ct']=75
dataSB = getIVP(model, par, ics, tini=tini, tf=tsim)
ics = getnewICS(dataSB)
par['Vplc']=0.1
dataSB = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data Broad Spike w/ Plateau
"""
par = parFullOpenCell()
ics = icsFullClosedCell()
model = fullClosedCell
tini, tsim, tf = [0, 200, 80]
par['Vplc']=0.0
par['Ct']=95
dataSBr = getIVP(model, par, ics, tini=tini, tf=tsim)
ics = getnewICS(dataSBr)
par['Vplc']=0.195
dataSBr = getIVP(model, par, ics, tini=tini, tf=tf)
#%% Figure creation 
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 4, nrows=1, figure=fig)
fig_width,fig_height = set_figsize(1, (0.6,1), export=True) 
fig.set_size_inches([fig_width,fig_height])
"""
Ax settings Simulation - Wide SOCE
"""
ax = fig.add_subplot(spec[0, 0])
ax.plot(dataSW[0], dataSW[1], color = 'C2')
# Ax limits 
xlim = [0, 240]
ylim = [0, 0.4]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'c', rotation='vertical', labelpad=-10, ma='center')
ax.set_xlabel(r'Time (seconds)')
ax.set_title('A', loc='left')

"""
Ax settings Simulation - Narrow Spike
"""
ax = fig.add_subplot(spec[0,1])
ax.plot(dataSN[0], dataSN[1], color = 'C3')
# Ax limits 
xlim = [0, 40]
ylim = [0, 0.4]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_xlabel(r'Time (seconds)')
ax.set_title('B', loc='left')

"""
Ax settings Simulation - Broad Spike
"""
ax = fig.add_subplot(spec[0,2])
ax.plot(dataSB[0], dataSB[1], color = 'salmon')
# Ax limits 
xlim = [0, 40]
ylim = [0, 0.4]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
# ax.set_ylabel(r'Cytoplasmic [Ca$^{2+}$]', rotation='vertical', labelpad=0, ma='center')
ax.set_xlabel(r'Time (seconds)')
ax.set_title('C', loc='left')

"""
Ax settings Simulation - Broad Spike w/ Plateau
"""
ax = fig.add_subplot(spec[0, 3])
ax.plot(dataSBr[0], dataSBr[1], color = 'orangered')
# Ax limits 
xlim = [0, 80]
ylim = [0, 0.4]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
# ax.set_ylabel(r'Cytoplasmic [Ca$^{2+}$]', rotation='vertical', labelpad=0, ma='center')
ax.set_xlabel(r'Time (seconds)')
ax.set_title('D', loc='left')

"""
Figure saving
"""
# fig.savefig(latexPath/'Fig3.pdf', facecolor='w')
fig.savefig('Figures/Fig3.pdf', facecolor='w')
# %%
