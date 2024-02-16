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
from PyModels import parFullOpenCell, getIVP, getnewICS, fullOpenCell, icsFullOpenCell
matplotlib.rcParams.update(myRcParams())
#%% TwoPar Ct-Vplc - fullOpenCell
# region 
"""
Data - Two Par - Normal  Ke
"""
# Hopf bifurcations 
file = "AUTOfullOpenCell"
model = load(file) 
parTwo = 'delta'
parTwoLim = [0.0001, 3]
# eq = run(
#     model, 
#     IPS=1, 
#     ICP=['Ke'], 
#     NMX=5000,
#     DS=-1e-2,
#     DSMAX=1e-1,
#     UZSTOP={'Ke': 660}
# )
eq = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-1,
    UZSTOP={'Vplc': 0.1}
)
eq = run(
    eq, 
    IPS=1, 
    ICP=['delta'], 
    NMX=5000,
    DS=-1e-3,
    DSMAX=1e-3,
    UZSTOP={parTwo: parTwoLim}
)
twoPar = run(model, NMX=1)
for sol in eq(['HB1', 'HB2']):
    fwd = run(
        sol, 
        ICP = ['Vplc',parTwo], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-1, 
        NMX=6000,
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc':[0.01, 1],parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ICP = ['Vplc',parTwo], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        DSMAX = 1e-1, 
        SP=['LP0', 'UZ', 'BP0'],
        UZSTOP={'Vplc':[0.01, 1], parTwo: parTwoLim},
    )
    twoPar = twoPar + merge(fwd+bwd)

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
Data - Mid delta - normal Ke
"""
file = "AUTOfullOpenCell"
model = load(file) 
# run(
#     model, 
#     IPS=-2, 
#     ICP=['TIME'], 
#     NMX=40000,
# )
eqM = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-2,
    UZSTOP={'Vplc': 0.3},
    PAR={'delta': 1}
)
# cycleM = run(
#     eqM('HB'), 
#     IPS=2,
#     # ISP=2, 
#     ICP=['Vplc', 11, 'MIN c'], 
#     NMX=5000,
#     NTST=1200,
#     DS=1e-2,
#     DSMAX=1e-2,
#     SP=['LP1', 'TR0', 'PD2', 'BP0'],
#     # UZSTOP={'Vplc': 0.1575}, 
#     UZR={'Vplc': 0.1}
# )
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
    PAR={'delta': 2.2}
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
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=3, figure=fig)
fig_width,fig_height = set_figsize(1, (1.5,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
# fig.suptitle('Experimental traces')
"""
Ax settings - Two Par - Normal Ke
"""
ax = fig.add_subplot(spec[0:3,0])
# Data extraction
soce = twoPar.data[1]
ipr = twoPar.data[2]
soce = soce[0::1]
ipr = ipr[0::1]

# soce curve 
ax.plot(soce['Vplc'], soce['delta'], 'C2', label = 'CRAC-mediated \n attractor')
# ipr curve
ax.plot(ipr['Vplc'], ipr['delta'], 'C3', label = r'IP$_3$R attractor')

ax.fill_between(
    soce['Vplc'], soce['delta'], 3, 
    alpha = 0.7, color = 'C2'
    )
ax.fill_between(
    ipr['Vplc'], ipr['delta'], 0, 
    alpha = 0.7, color = 'C3'
    )
# Ax limits 
xlim = [0.04, 0.15]
ylim = [0, 2]
ax.set_xticks(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
ax.set_ylabel(r'$\delta$', labelpad=-10)
ax.set_title('A', loc='left')
ax.legend()

"""
Ax settings Vplc Diag - Normal Ke - High delta
"""
ax = fig.add_subplot(spec[0,1])
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
# ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-20)
ax.set_title('B', loc='left')


"""
Ax settings Vplc Diag - Normal Ke - Mid delta
"""
ax = fig.add_subplot(spec[1,1])
# Data extraction
eqCurve = eqM.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)

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


# Ax limits 
xlim = [0,0.15]
ylim = [0.05, 0.25]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_yticks(ylim)
ax.set_xticks(xlim)
# ax.set_xlabel(r'$V_{\mathrm{PLC}}$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-20)
ax.set_title('C', loc='left')


"""
Ax settings Vplc Diag - Normal Ke - High delta
"""
ax = fig.add_subplot(spec[2,1])
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
#Limit cycle curve
ax.plot(cyCurve['Vplc'], cyCurve['MAX c'], 'C3')
ax.plot(cyCurve['Vplc'], cyCurve['MIN c'], 'C3')
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
ax.set_title('D', loc='left')
# fig.savefig(latexPath/'Fig11.pdf')
fig.savefig('Figures/Fig11.pdf')
