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
from pathlib import Path
parentPath = str(Path(os.getcwd()).parent)
sys.path.append(parentPath)
latexPath = Path(os.getcwd()).parent/'Latex'
from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import parFullOpenCell, getIVP, getnewICS, fullOpenCell, simpleOpenCell, icsFullOpenCell, icsSimpleOpenCell, parSimpleOpenCell
matplotlib.rcParams.update(myRcParams())

#%% Data Collection
"""
Data Vplc Diag - Full Open Cell
"""
file = "AUTOfullOpenCell"
model = load(file) 
eqF = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 1}
)

cycleF = run(
    eqF('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11, 'MIN c'], 
    NMX=5000,
    NTST=1200,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP2', 'TR0', 'PD2', 'BP0'],
    # UZSTOP={'Vplc': 0.1575}, 
    UZR={'Vplc': 0.1}
)
cl()
"""
Data Simulation - Full Open Cell
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
model = fullOpenCell
tini, talpha, tf = [0, 10, 120]
par['Vplc']=0.1
dataF = getIVP(model, par, ics, tini=tini, tf=500)
ics = getnewICS(dataF)
dataF = getIVP(model, par, ics, tini=tini, tf=tf)
#%% Figure creation
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=1, figure=fig)
fig_width,fig_height = set_figsize(1, (0.8,1), export=True, width=370) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
"""
Ax settings Vplc Diag - Full Open Cell
"""
ax = fig.add_subplot(spec[0,0])
# Data extraction
eqCurve = eqF.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleF.data[0]
cyCurve = cyCurve[0::2]
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
#Limit cycle curve
ax.plot(cyCurve['Vplc'], cyCurve['MAX c'], 'C2')
ax.plot(cyCurve['Vplc'], cyCurve['MIN c'], 'C2')
# HB points 
for i in [2,3]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB',
            [point['Vplc'],
            max(point['c'])*0.9],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )
# Ax limits 
xlim = [0,0.15]
ylim = [0.05, 0.25]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-20)
ax.set_title('A', loc='left')

"""
Ax settings - Data Simulation - Full Open Cell
"""
ax = fig.add_subplot(spec[0, 1])
ax.plot(dataF[0], dataF[5], color = 'C2')
ax2 = ax.twinx()
ax2.plot(dataF[0], dataF[2], color = 'C2', ls = 'dashed')
# Ax limits 
xlim = [0, 120]
ylim = [0.5, 1.6]
y2lim = [780, 820]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
ax.set_ylabel(r'$s$', rotation='vertical', labelpad=-15, ma='center')
ax2.set_ylabel(r'$c_e$', rotation='vertical', labelpad=-15, ma='center')
ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_title('B', loc='left')


# fig.savefig(latexPath/'Fig4.pdf')
fig.savefig('Figures/Fig4.pdf')
# %%
