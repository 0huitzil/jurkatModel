#%%
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
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
sys.path.append(parentPath)
latexPath = Path(os.getcwd()).parent/'Latex'

from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import fullOpenCell, icsFullOpenCell, parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS, getIPR, getSERCA, getP0
matplotlib.rcParams.update(myRcParams())
#%% Simulation - Wide SOCE - C - low ER
# region 
"""
Data Simulation - Full Open Cell
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
model = fullOpenCell
tini, talpha, tf = [0, 10, 60]
par['Vplc']=0.1
dataF = getIVP(model, par, ics, tini=tini, tf=500)
ics = getnewICS(dataF)
dataF = getIVP(model, par, ics, tini=tini, tf=tf)
iprF = getIPR(dataF[1:], par)
p0f = getP0(dataF[1:], par)
sercaF = getSERCA(dataF[1:], par)
# Closed Cell data 
ics = icsFullOpenCell()
tini, talpha, tf = [0, 10, 60]
par['delta']=0
dataC = getIVP(model, par, ics, tini=tini, tf=500)
ics = getnewICS(dataC)
dataC = getIVP(model, par, ics, tini=tini, tf=tf)
iprC = getIPR(dataC[1:], par)
p0c = getP0(dataC[1:], par)
sercaC = getSERCA(dataC[1:], par)
#%%
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 1, nrows=1, figure=fig)
fig_width,fig_height = set_figsize(1, (1,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
# fig.suptitle('Experimental traces')
xlim = [0, tf]
ylim = [0, 0.4]
xticks = [0, tf/2, tf]
yticks = [0, 0.2, 0.4]
"""
Ax settings - IPR flux
"""
ax = fig.add_subplot(spec[0,0])

ax.plot(dataC[0], p0c, color = 'C3', alpha = 0.5, label ='Narrow spike')
ax.plot(dataF[0], p0f, color = 'C2', label ='CRAC-mediated')
# Ax limits 
xlim = [0, 60]
ylim = [0, 0.001]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'IP$_3$R open probability (P$_0$)', rotation='vertical', labelpad=-20, ma='center')
ax.set_xlabel(r'Time (seconds)', rotation='horizontal', labelpad=-10, ma='center')
ax.set_title('A', loc='left')
ax.legend()

# fig.savefig(latexPath/'Fig6.pdf')
fig.savefig('Figures/Fig6.pdf')
# endregion

# %%
