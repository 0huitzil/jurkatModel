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
# parentPath = str(Path(os.getcwd()).parent)
# sys.path.append(parentPath)
# latexPath = Path(os.getcwd()).parent/'Latex'

from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import fullOpenCell, icsFullOpenCell, parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS, getSOCE
matplotlib.rcParams.update(myRcParams())
#%% Data Collection
"""
Data - Low ER
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
model = fullOpenCell
tini, talpha, tf = [0, 10, 120]
par['Vplc']=0.1
dataL = getIVP(model, par, ics, tini=tini, tf=tf)

"""
Data - High ER
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
ics['c']=0.085
ics['ce']=850
ics['s']=0
model = fullOpenCell
tini, talpha, tf = [0, 10, 120]
par['Vplc']=0.1
dataH = getIVP(model, par, ics, tini=tini, tf=tf)
"""
Data - SOCE activation curve
"""
ce = np.linspace(700, 900, 60)
var = [0, ce, 0, 0, 0] #To get in the required format for the getSOCE function
Jsoce = getSOCE(var, par)

#%% Figure creation
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=2, figure=fig)
fig_width,fig_height = set_figsize(1, (1,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
# fig.suptitle('Experimental traces')

"""
Ax settings - Low ER Time Series
"""
ax = fig.add_subplot(spec[0,0])
ax.plot(dataL[0], dataL[1], color = 'C2')
xlim = [0,tf]
ylim = [0, 0.4]
#Ax limits
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('A', loc='left')

"""
Ax settings - High ER Phase plane
"""
ax = fig.add_subplot(spec[0,1])
ax.plot(dataL[2], dataL[5], color = 'C2',)
ax.plot(ce, Jsoce, color = 'k',)
# ax.plot(dataL[1] + dataL[2]/par['gamma'], getSOCE(dataL[1:], par), 'C1', label = 'SOCE \nsignal') 
#Ax limits
xlim = [730, 870]
ylim = [0, 3]
ax.set_xlim(xlim)
ax.set_ylim([0, 3.2])
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'$c_e$', labelpad=-10)
ax.set_ylabel(r'$s$', labelpad=-10)
ax.set_title('B', loc='left')
# ax.legend()

"""
Ax settings - High ER Time Series
"""
ax = fig.add_subplot(spec[1,0])
ax.plot(dataH[0], dataH[1], color = 'C2')
xlim = [0,tf]
ylim = [0, 0.4]
#Ax limits
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('C', loc='left')

"""
Ax settings - High ER Phase plane
"""
ax = fig.add_subplot(spec[1,1])
ax.plot(dataH[2], dataH[5], color = 'C2' )
ax.plot(ce, Jsoce, color = 'k', label = r'$J_\mathrm{SOCE}$')
#Ax limits
xlim = [730, 870]
ylim = [0, 3]
ax.set_xlim(xlim)
ax.set_ylim([0, 3.2])
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'$c_e$', labelpad=-10)
ax.set_ylabel(r'$s$', labelpad=-10)
ax.set_title('D', loc='left')
ax.legend()
fig.savefig(latexPath/'Fig7.pdf')
# fig.savefig('Figures/Fig7.pdf')
# %%
