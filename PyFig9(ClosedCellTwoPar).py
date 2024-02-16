#%% Libraries
"""
This file contains all the scripts necessary to create fig #2
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
from PyModels import parFullOpenCell, getIVP, fullClosedCell, icsFullClosedCell, getnewICS
matplotlib.rcParams.update(myRcParams())
#%% Data Collection 
"""
file = "AUTOfullClosedCell"
model = load(file) 
CtVal = 125
eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={
        'Ct': CtVal,
        # 'Ct': 100,
        }
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2,
    ICP=['Vplc', 11, 47], 
    NMX=5000,
    DS=2e-4,
    DSMAX=5e-3,
    NTST=400,
    DSMIN=1e-5,
    UZSTOP={'Vplc': 0.08, 11 : 0.01}, 
    UZR={'Vplc': 0.1, }, 
    SP=['LP', 'UZ', 'BP0', 'PD'],
)
# Number of positive floquet multipliers
stab = cycle['Floquet'] 
# Vplc values 
Vplc = cycle['Vplc']
# Index of values where the number of positive floquet multiplers change  by 2 (TR bifurcation)
# 0 is removed manually to account for the first step of continuation
index = np.where(np.abs(stab[:-1] - stab[1:]) == 2 )
# Return Vplc values 
TR = Vplc[index]
bif = np.zeros((len(TR),2))
bif[:,0] = TR
bif[:,1] = CtVal
print(bif)
"""
#%%
# TR bifurcations 
''' 
AUTO has a particularly bad time calculating torus type bifurcations 
on this system. Reasons unknown. However, the exact point at which the 
TR bifurcations happen can be obtained by looking at the number of stable
FLoquet multiplers. By obtaining the parameter values at which this happens
we can approximate the TR curve in two parameter space. 
'''
def eqStab(CtVal = 140):
    file = "AUTOfullClosedCell"
    model = load(file) 
    """
    Returns coordinates for Torus bifurcations on the closed-cell model
    """
    eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={
        'Ct': CtVal,
        # 'Ct': 100,
        }
    )
    eq = run(
        eq, 
        IPS=1, 
        ICP=['Vplc'], 
        NMX=5000,
        DS=1e-2,
        DSMAX=1e-2,
        UZSTOP={'Vplc': 1}
    )
    cycle = run(
        eq('HB2'), 
        IPS=2,
        ICP=['Vplc', 11, 47], 
        NMX=5000,
        DS=1e-4,
        DSMAX=5e-3,
        NTST=400,
        DSMIN=1e-5,
        UZSTOP={'Vplc': 0.1, 11 : 0.01}, 

        SP=['LP', 'UZ', 'BP0', 'PD'],
    )
    # Number of positive floquet multipliers
    stab = cycle['Floquet'] 
    # Vplc values 
    Vplc = cycle['Vplc']
    # Index of values where the number of positive floquet multiplers change  by 2 (TR bifurcation)
    # 0 is removed manually to account for the first step of continuation
    index = np.where(np.abs(stab[:-1] - stab[1:]) == 2 )
    # Return Vplc values 
    TR = Vplc[index]
    if len(TR) == 0:
        return 0
    else:
        bif = np.zeros((len(TR)*2))
        bif[::2] = TR
        bif[1::2] = CtVal
        return bif 
# Regime 1 - 2 TR bifurcations
l1 = np.linspace(125, 131.8, 20)
tr1 = np.zeros((20, 4))
for i in range(0,20):
    bif = eqStab(CtVal=l1[i])
    tr1[i, :] = bif
#
# Regime 2 - 1 TR bifurcation
l2 = np.linspace(106, 124, 20)
tr2 = np.zeros((20, 2))
for i in range(0,20):
    bif = eqStab(CtVal=l2[i])
    tr2[i, :] = bif
cl()
#%%
"""
Data - TwoPar Ct-Vplc
"""
# Hopf bifurcations 
file = "AUTOfullClosedCell"
model = load(file) 

eq = run(
    model, 
    IPS=1, 
    ICP=['Ct'], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={
        # 'Ct': 130,
        'Ct': 100,
        }
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 1}
)
cycle = run(
    eq('HB2'), 
    IPS=2,
    # ISP=2, 
    ICP=['Vplc', 11], 
    NMX=5000,
    DS=2e-3,
    DSMAX=1e-2,
    NTST=400,
    DSMIN=1e-5,
    UZSTOP={'Vplc': 1}, 
    UZR={'Vplc': 0.1},
    SP=['LP2', 'PD'],
)
twoPar = run(model, NMX=1)
for sol in eq(['HB1']):
    fwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=6000,
        SP=['LP', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    bwd = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-1, 
        SP=['LP', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    twoPar = twoPar + merge(fwd+bwd)
# PD and SNPO curve 
for sol in cycle(['LP1', 'PD2']):
    t = run(
        sol, 
        ICP = ['Vplc','Ct'], 
        ISW=2, 
        IPS=2,
        DS = 1e-2,
        DSMAX = 1e-0, 
        NMX=6000,
        NTST=1200,
        SP=['LP', 'UZ', 'BP0'],
        UZSTOP={'Vplc': [0, 2], 'Ct': [200, 10]},
    )
    fwd = run(t, DS=1e-2,)
    bwd = run(t, DS=-1e-2)
    twoPar = twoPar + merge(fwd+bwd)
cl()
#%% Figure creation
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 1, nrows=1, figure=fig)
fig_width,fig_height = set_figsize(1, (0.7,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
"""
Ax settings TwoPar Ct-Vplc
"""
ax = fig.add_subplot(spec[0:])
# Data extraction
hopf = twoPar.data[1]
snpo = twoPar.data[2]
pd = twoPar.data[3]
hopf = hopf[0::10]
snpo = snpo[0::10]
pdInterp = np.interp(hopf['Vplc'], pd['Vplc'], pd['Ct']) # For shading purposes
snpoInterp = np.interp(hopf['Vplc'], snpo['Vplc'], snpo['Ct']) # For shading purposes# Hopf curve 
ax.plot(hopf['Vplc'], hopf['Ct'], 'C7', lw=2, label = 'HB')
#SNPO curve
ax.plot(snpo['Vplc'], snpo['Ct'], 'salmon', lw=2, label = 'SNPO')
#PD curve
ax.plot(pd['Vplc'], pd['Ct'], 'red',lw=2, label = 'PD')
#TR curve 
ax.plot(tr1[:,0], tr1[:,1], 'C2', lw = 2, ls = 'dotted', label = 'TR')
ax.plot(tr1[:,2], tr1[:,3], 'C2', lw = 2, ls = 'dotted')
ax.plot(tr2[:,0], tr2[:,1], 'C2', lw = 2, ls = 'dotted')
# Broad spike w/ Plateau separatrix 
# maxVal = pd['Ct'].argmax()
# maxCt = pd['Ct'].max()*1.01
# ax.plot([pd['Vplc'][maxVal], snpo['Vplc'][0]], [maxCt, maxCt], 'C1', ls = 'dashed')

# # Narrow Spike Zone
# ax.fill_between(
#     hopf['Vplc'], hopf['Ct'], pdInterp, 
#     # where = np.arange(len(pdInterp)) <= np.argmax(pdInterp), 
#     alpha = 1, color = 'red'
#     )
ax.annotate(r'I', [0.08, 140])
# # Broad Spike zone w/ Plateau Zone
# ax.fill_between(
#     hopf['Vplc'], snpoInterp*0.99,
#     # where = np.logical_and(np.arange(len(pdInterp)) >= np.argmax(pdInterp), hopf['Vplc'] < 0.992*min(snpo['Vplc'])), 
#     where = hopf['Vplc'] > 0.14, 
#     alpha = 1, color = 'white'
#     )
# ax.fill_between(
#     hopf['Vplc'], snpoInterp*0.99,
#     # where = np.logical_and(np.arange(len(pdInterp)) >= np.argmax(pdInterp), hopf['Vplc'] < 0.992*min(snpo['Vplc'])), 
#     where = hopf['Vplc'] > 0.14, 
#     alpha = 0.7, color = 'orangered'
#     )
ax.annotate(r'III', [0.2,87])
# # Broad Spike  
# ax.fill_between(
#     pd['Vplc'], pd['Ct'], 
#     alpha = 1, color= 'salmon'
#     )
ax.annotate(r'II', [0.14,87])
# Null region 
ax.annotate(r'IV', [0.16,150])
# Ax limits 
xlim = [0,0.3]
ylim = [70,170]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=-5)
ax.set_ylabel(r'$C_t$', labelpad=-15)
# ax.set_title('A', loc='left')
ax.legend()

# fig.savefig(latexPath/'Fig9.pdf')
fig.savefig('Figures/Fig9.png')
# %%
