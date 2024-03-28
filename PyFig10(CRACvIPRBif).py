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
# sys.path.append(parentPath)
# latexPath = Path(os.getcwd()).parent/'Latex'
# from PyContFunctions import parChange
from auto import *
from auto import run, load, save, merge, relabel, cl, klb
from numpy import e, log, sqrt
from myOptions import *
from PyModels import parFullOpenCell, getIVP, getnewICS, fullOpenCell, icsFullOpenCell
matplotlib.rcParams.update(myRcParams())
#%% TwoPar Ct-Vplc - fullOpenCell
# region 
"""
Data - Low delta - normal Ke
"""
file = "AUTOfullOpenCell"
model = load(file) 
eqN = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3},
    PAR={'delta': 0.01}
)
cycleN = run(
    eqN('HB'), 
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
"""
Data - High delta - normal Ke
"""
file = "AUTOfullOpenCell"
model = load(file) 
# run(
#     model, 
#     IPS=-2, 
#     ICP=['TIME'], 
#     NMX=40000,
# )
eqH = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3},
    PAR={'delta': 2}
)
cycleH = run(
    eqH('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11, 'MIN c'], 
    NMX=5000,
    NTST=1200,
    DS=1e-2,
    DSMAX=1e-2,
    SP=['LP1', 'TR0', 'PD2', 'BP0'],
    # UZSTOP={'Vplc': 0.1575}, 
    UZR={'Vplc': 0.1}
)
cl()
#%%
"""
Data Simulation - High delta
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
model = fullOpenCell
tini, talpha, tf = [0, 10, 120]
par['Vplc']=0.1
par['delta']=2.2
dataH = getIVP(model, par, ics, tini=tini, tf=500)
ics = getnewICS(dataH)
dataH = getIVP(model, par, ics, tini=tini, tf=tf)


"""
Data Simulation - low delta
"""
par = parFullOpenCell()
ics = icsFullOpenCell()
model = fullOpenCell
tini, talpha, tf = [0, 10, 20]
par['Vplc']=0.1
par['delta']=0.01
dataN = getIVP(model, par, ics, tini=tini, tf=500)
ics = getnewICS(dataN)
dataN = getIVP(model, par, ics, tini=tini, tf=tf)
#%%
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=2, figure=fig)
fig_width,fig_height = set_figsize(1, (1,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])

"""
Ax settings Vplc Diag - Full Open Cell
"""
ax = fig.add_subplot(spec[0,0])
# Data extraction
eqCurve = eqH.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleH.data[0]
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
            [point['Vplc']+0.001,
            max(point['c'])*0.8],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C2', 
            markersize =5,
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
Ax settings - Data Simulation - High delta
"""
ax = fig.add_subplot(spec[0, 1])
ax.plot(dataH[0], dataH[1], color = 'C2', label = r'$c$')
ax2 = ax.twinx()
ax2.plot(dataH[0], dataH[2], color = 'C2', ls = 'dashed', label = r'$c_e$')
# Ax limits 
xlim = [0, 120]
ylim = [0.1, 0.24]
y2lim = [780, 830]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
ax.set_ylabel(r'$c$', rotation='vertical', labelpad=-15, ma='center')
ax2.set_ylabel(r'$c_e$', rotation='vertical', labelpad=-15, ma='center')
ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_title('B', loc='left')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
"""
Ax settings Vplc Diag - Low delta
"""
ax = fig.add_subplot(spec[1,0])
# Data extraction
eqCurve = eqN.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleN.data[0]
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
# Limit cycle curve
ax.plot(cyCurve['Vplc'], cyCurve['MAX c'], 'C3')
ax.plot(cyCurve['Vplc'], cyCurve['MIN c'], 'C3')
# HB points 
for i in [2,3]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB',
            [point['Vplc']+0.001,
            max(point['c'])*1.1],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )
        ax.plot(
            point['Vplc'],
            max(point['c']), 
            marker = 'o', 
            color = 'C3', 
            markersize =5,
        )
# Ax limits 
xlim = [0,0.15]
ylim = [0.05, 0.25]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('C', loc='left')

"""
Ax settings Simulation - Narrow Spike - low delta
"""
ax = fig.add_subplot(spec[1,1])
ax.plot(dataN[0], dataN[1], color = 'red', label = r'$c$')
ax2 = ax.twinx()
ax2.plot(dataN[0], dataN[2], color = 'red', ls = 'dashed', label = r'$c_e$')
# Ax limits 
xlim = [0,20]
ylim = [0.1, 0.24]
y2lim = [780, 830]
# ax.set_xlim(xlim)
# ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
ax2.set_yticks(y2lim)
ax.spines.right.set_visible(True)
# ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax2.set_ylabel(r'$c_e$', labelpad=-10)
ax.set_xlabel(r'Time (seconds)', labelpad=-10)
ax.set_title('D', loc='left')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# fig.savefig(latexPath/'Fig10.pdf')
fig.savefig('Figures/Fig10.pdf')
# endregion