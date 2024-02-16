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
from PyModels import parFullOpenCell, getSOCE
matplotlib.rcParams.update(myRcParams())

#%% Data Collection 
"""
Data - SOCE activation curve
"""
par = parFullOpenCell()
ce = np.linspace(700, 900, 60)
Ke = par['Ke']
Vsoce = par['Vsoce']
var = [0, ce, 0, 0, 0] #To get in the required format for the getSOCE function
Jsoce = getSOCE(var, par)
n = 100
Jhill = Vsoce *(Ke**n/(Ke**n + ce**n))
#%%
"""
Data S1 bifurcation
"""

file = "AUTOfullOpenCell"
model = load(file) 
parTwo = 's1'
parTwoLim = [0.01, 1]
eqS = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.1}
)
eqS = run(
    eqS, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
eqS = run(
    eqS, 
    IPS=1, 
    ICP=['s1'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
cycleS = run(
    eqS('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11, 'MIN c'], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [0.1, 0.3,0.5,0.8]}
)

"""
Data TwoPar s1 
"""
twoParS = run(eqS, NMX=1)
parTwo = 's1'
parTwoLim = [0.01, 1]
for sol in eqS(['HB1']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    twoParS = twoParS + merge(fwd+bwd)
twoParS = relabel(twoParS)

"""
Data TwoPar s1 - Ts
"""
twoParST = run(eqS, NMX=1)
parTwo = 's1'
parTwoLim = [0.01, 1]
for sol in eqS(['HB1']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Ts'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Ts': [0, 400], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Ts'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ'],
        UZSTOP={'Ts': [0, 400], parTwo: parTwoLim},
    )
    twoParST = twoParST + merge(fwd+bwd)
twoParST = relabel(twoParST)
"""
Data Ke bifurcation
"""
file = "AUTOfullOpenCell"
model = load(file) 
parTwo = 'Ke'
parTwoLim = [900, 600]
eqK = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.1}
)
eqK = run(
    eqK, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={parTwo: parTwoLim}
)
eqK = run(
    eqK, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={parTwo: parTwoLim}
)
cycleK = run(
    eqK('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11, 'MIN c'], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-0,
    SP=['LP4', 'TR0', 'PD2'],
    UZSTOP={parTwo: parTwoLim}, 
    UZR={parTwo: [697]}
)

"""
Data TwoPar Ke
"""
twoParK = run(eqK, NMX=1)
parTwo = 'Ke'
parTwoLim = [0.01, 1]
eqK = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.1}
)
eqK = run(
    eqK, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-0,
    UZSTOP={parTwo: parTwoLim}
)
eqK = run(
    eqK, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={parTwo: parTwoLim}
)
for sol in eqK(['LP2', 'HB1', 'LP1',]):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = 1e-2,
        NMX=6000,
        SP=['LP0', 'UZ', 'CP1'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    bwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = -1e-2, 
        NMX=6000,
        SP=['LP0', 'UZ', 'CP1'],
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    twoParK = twoParK + merge(fwd+bwd)
twoParK = relabel(twoParK)
#%
"""
Data Ts bifurcation
"""
file = "AUTOfullOpenCell"
model = load(file) 
parTwo = 'Ts'
parTwoLim = [200, 0.01]
eqT = run(
    model, 
    IPS=1, 
    ICP=['Vplc'], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-0,
    UZSTOP={'Vplc': 0.1}
)
eqT = run(
    eqT, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=-1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
eqT = run(
    eqT, 
    IPS=1, 
    ICP=[parTwo], 
    NMX=5000,
    DS=1e-2,
    DSMAX=1e-1,
    UZSTOP={parTwo: parTwoLim}
)
cycleT = run(
    eqT('HB'), 
    IPS=2,
    # ISP=2, 
    ICP=[parTwo, 11, 'MIN c'], 
    NMX=2000,
    NPR=400,
    DS=1e-2,
    DSMAX=1e-1,
    SP=['LP2', 'TR0', 'PD2'],
    UZSTOP={parTwo: [5.4846], }, 
    UZR={parTwo: [0.1, 0.3,0.5,0.8]}
)
#%
"""
Data TwoPar Ts
"""
twoParT = run(eqT, NMX=1)
parTwo = 'Ts'
parTwoLim = [0.01, 400]
for sol in eqT(['HB2']):
    fwd = run(
        sol, 
        ISP=2,
        ICP = [parTwo, 'Vplc'], 
        ISW=2, 
        DS = 1e-2,
        DSMAX = 1e-1,
        NMX=6000,
        SP=['LP3', 'UZ2'],
        UZR = {'Vplc': 0.1},
        UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    )
    # bwd = run(
    #     sol, 
    #     ISP=2,
    #     ICP = [parTwo, 'Vplc'], 
    #     ISW=2, 
    #     DS = -1e-2, 
    #     NMX=6000,
    #     SP=['LP1', 'UZ'],
    #     UZSTOP={'Vplc': [0, 2], parTwo: parTwoLim},
    # )
    twoParT = twoParT + merge(fwd)
twoParT = relabel(twoParT)

cl()
#%%
"""
Figure settings
"""
fig = plt.figure(constrained_layout = True)
spec = gridspec.GridSpec(ncols = 2, nrows=3, figure=fig)
fig_width,fig_height = set_figsize(1, (1.8,1), export=True) #184 is Beamer width
fig.set_size_inches([fig_width,fig_height])
# fig.suptitle('Experimental traces')
"""
Ax settings - s1 Bifurcation 
"""
ax = fig.add_subplot(spec[0,0])
# Data extraction
eqCurve = eqS.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleS.data[0]
cyCurve = cyCurve[0::2]
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            label='Equilibria'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
ax.plot(cyCurve['s1'], cyCurve['MAX c'], 'C2', label = 'Oscillation')
ax.plot(cyCurve['s1'], cyCurve['MIN c'], 'C2')
# HB points 
for i in [6]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB',
            [point['s1'],
            max(point['c'])*0.85],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )

# Ax limits 
xlim = [0, 1]
ylim = [0.05, 0.25]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_xlabel(r'$s_1$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('A', loc='left')
# ax.legend()
"""
Ax settings - TwoPar s1
"""
ax = fig.add_subplot(spec[0,1])
# Data extraction
eqCurve = twoParS.data[1]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            'k', 
            ls='solid', 
            alpha=1, 
            label='HB curve'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            'k',
            ls='solid',
            alpha=1,
            label='HB curve'
        )
ax.fill_between(
    eqCurve['Vplc'], eqCurve['s1'], 1, 
    alpha = 0.7, color = 'C2', label = 'Oscillations'
    )
# Ax limits 
xlim = [0, 0.5]
ylim = [0, 1]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'$s_1$', labelpad=-0)
ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=-10)
ax.set_title('B', loc='left')
ax.legend()
"""
Ax settings - s1 Bifurcation 
"""
ax = fig.add_subplot(spec[1,0])
# Data extraction
eqCurve = eqT.data[0]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
cyCurve = cycleT.data[0]
cyCurve = cyCurve[0::2]
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['c'], 
            'k',
            ls='dashed',
            alpha=1,
        )
ax.plot(cyCurve['Ts'], cyCurve['MAX c'], 'C2')
ax.plot(cyCurve['Ts'], cyCurve['MIN c'], 'C2')
# HB points 
for i in [6,7]: #I only care about two particular labels
    point = eqCurve.getLabel(i)
    if point.get('TY') not in ['UZ', 'EP']:
        ax.annotate(
            'HB',
            [point['Ts'],
            max(point['c'])*0.95],
            # 'C2',
            # marker='o', 
            # markersize=10,
        )


# Ax limits 
xlim = [0, 200]
ylim = [0.1, 0.2]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_xlabel(r'$\tau_s$', labelpad=-10)
ax.set_ylabel(r'$c$', labelpad=-10)
ax.set_title('C', loc='left')

"""
Ax settings - TwoPar s1
"""
ax = fig.add_subplot(spec[1,1])
# Data extraction
eqCurve = twoParT.data[1]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Vplc'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            'k',
            ls='solid',
            alpha=1,
        )
ax.fill(
    eqCurve['Vplc'], eqCurve['Ts'],
    alpha = 0.7, color = 'C2'
    )
# ax.fill_between(
#     eqCurve['Vplc'], 50, eqCurve['Ts'], 
#     alpha = 0.7, color = 'C2'
#     )
# ax.fill_between(
#     eqCurve['Vplc'], 0, 1.3*min(eqCurve['Ts']), 
#     alpha = 1, color = 'w'
#     )
# Ax limits 
xlim = [0, 0.2]
ylim = [0, 200]
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'$\tau_s$', labelpad=-10)
ax.set_xlabel(r'$V_\mathrm{PLC}$', labelpad=-10)
ax.set_title('D', loc='left')

"""
Ax settings - TwoPar s1-Ts
"""
ax = fig.add_subplot(spec[2,1])
# Data extraction
eqCurve = twoParST.data[1]
eqCurve = eqCurve[0::1]
eqStab = eqCurve.stability()
eqStab.insert(0,0)
#  Equilibrium line 
for i in range(1,len(eqStab)):
    if eqStab[i]< 0:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            'k', 
            ls='solid', 
            alpha=1, 
            # label='EQ points'
        )
    else:
        ax.plot(
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['s1'], 
            eqCurve[max(np.abs(eqStab[i-1])-1,0):np.abs(eqStab[i])]['Ts'], 
            'k',
            ls='solid',
            alpha=1,
        )
ax.fill_between(
    eqCurve['s1'], eqCurve['Ts'], 
    alpha = 0.7, color = 'C2'
    )
# Ax limits 
xlim = [0, 0.35]
ylim = [0, 300]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'$\tau_s$', labelpad=-10)
ax.set_xlabel(r'$s_1$', labelpad=-10)
ax.set_title('F', loc='left')

"""
Ax settings - Steepness curves 
"""
ax = fig.add_subplot(spec[2,0])
# Data extraction
ax.plot(ce, Jsoce, 'C2', label = r'$J_\mathrm{SOCE}$')
ax.plot(ce, Jhill, 'C1', label = 'Hill')
# Ax limits 
xlim = [700, 900]
ylim = [0, 3.1]
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xticks(xlim)
ax.set_yticks(ylim)
ax.set_ylabel(r'$s$', labelpad=-10)
ax.set_xlabel(r'$c_e$', labelpad=-10)
ax.set_title('E', loc='left')
ax.legend(loc = 'lower left')
# fig.savefig(latexPath/'Fig5.pdf')
fig.savefig('Figures/Fig5.pdf')
# %%
